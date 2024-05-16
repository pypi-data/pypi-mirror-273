import datetime
import requests
import pandas as pd

class nfinance:
    base_url = "https://api.stock.naver.com/chart/domestic/item/"

    @classmethod
    def download(cls, ticker, start_date, end_date, interval='day'):
        start_datetime = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        start_str = start_datetime.strftime('%Y%m%d') + "0000"
        end_str = end_datetime.strftime('%Y%m%d') + "2359"

        url = f"{cls.base_url}{ticker}/{interval}?startDateTime={start_str}&endDateTime={end_str}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return cls.parse_data(data)
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")

    @staticmethod
    def parse_data(data):
        df = pd.DataFrame(data)
        df['localDate'] = pd.to_datetime(df['localDate'])
        df.set_index('localDate', inplace=True)
        df.rename(columns={
            'closePrice': 'Close',
            'openPrice': 'Open',
            'highPrice': 'High',
            'lowPrice': 'Low',
            'accumulatedTradingVolume': 'Volume',
            'foreignRetentionRate': 'ForeignHold'
        }, inplace=True)
        # Convert relevant columns to numeric
        df[['Close', 'Open', 'High', 'Low', 'Volume']] = df[['Close', 'Open', 'High', 'Low', 'Volume']].apply(pd.to_numeric)
        df['ForeignHold'] = df['ForeignHold'].astype(float)
        return df

# Test module
import unittest
from unittest.mock import patch

class TestNFinance(unittest.TestCase):
    @patch('requests.get')
    def test_download_successful(self, mock_get):
        # Setup
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            'localDate': '2022-01-01',
            'closePrice': '70000',
            'openPrice': '69000',
            'highPrice': '70500',
            'lowPrice': '68800',
            'accumulatedTradingVolume': '123456',
            'foreignRetentionRate': '53.4'
        }]

        # Action
        result = nfinance.download(ticker="005930", start_date="2022-01-01", end_date="2022-01-31")

        # Assert
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.loc[pd.Timestamp('2022-01-01')]['Close'], 70000)
        self.assertEqual(result.loc[pd.Timestamp('2022-01-01')]['Open'], 69000)

    @patch('requests.get')
    def test_download_failure(self, mock_get):
        # Setup
        mock_response = mock_get.return_value
        mock_response.status_code = 404

        # Action & Assert
        with self.assertRaises(Exception) as context:
            nfinance.download(ticker="005930", start_date="2022-01-01", end_date="2022-01-31")

        self.assertIn('Failed to fetch data', str(context.exception))

if __name__ == '__main__':
    unittest.main()
