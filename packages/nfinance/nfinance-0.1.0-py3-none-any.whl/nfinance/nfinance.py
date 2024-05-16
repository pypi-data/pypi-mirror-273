import datetime  # Add this line at the beginning of your file
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
        return df
