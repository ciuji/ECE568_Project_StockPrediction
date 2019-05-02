from yahoofinancials2 import YahooFinancials
import pandas as pd
import requests
import pymongo
import json
import urllib.request
import csv
import datetime


''' requirement
real-time data:
    contain the price, time** and volume. (time slice between two points no more than one minute)
historical data:
    time, open, high, low, close, volume.
'''
#06JRP8S4736D1FE6

class Stock_data:
    def __init__(self):
        self.ticker = None
        self.yahoo_financials = None
        self.currentTime = ''
        self.preTime = ''
        self.url = ''

    def get_historical_data(self):
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        self.currentTime = str(year) + '-' + str(month) + '-' + str(day)
        self.preTime = str(year - 1) + '-' + str(month) + '-' + str(day)
        raw_historical_data = self.yahoo_financials.get_historical_price_data(self.preTime, self.currentTime,'daily')
        historical_db = raw_historical_data[self.ticker]['prices']
        historical_csv = []
        header = list(historical_db[0].keys())
        historical_csv.append(header)
        #print(header)
        for i in range(len(historical_db)):
            historical_csv.append(list(historical_db[i].values()))

        #historical_data_df=pd.DataFrame.from_dict(historical_price_data)
        return historical_db, historical_csv

    def get_realtime_data(self):
        #resp_json = requests.get(self.url)
        #print(type(resp_json.text))
        '''
        data = pd.read_csv(self.url, header = 0)
        print(type(data))
        realtime_data = data.to_dict(orient = 'dict')
        print(realtime_data)
        '''
        with requests.Session() as s:
            download = s.get(self.url)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            realtime_csv = list(cr)

            header = realtime_csv[0]
            realtime_db = []
            for i in range(len(realtime_csv)-1):
                my_dict = {}
                for j in range(len(header)):
                    my_dict[header[j]] = realtime_csv[i+1][j]
                realtime_db.append(my_dict)
            return realtime_db, realtime_csv
        #realtime_data = json.loads(resp_json)
        #realtime_data_df=pd.DataFrame.from_dict(resp_json['Time Series (1min)'],orient='index')
        #realtime_data_df = pd.DataFrame(resp_json)

    def save_historical_data(self, data_db, data_csv):
        myclient = pymongo.MongoClient('mongodb://localhost:27017/')
        mydb = myclient['stockdb']
        collection_names = mydb.list_collection_names()
        if self.ticker in collection_names:
            mydb[self.ticker].drop()
        mycol = mydb[self.ticker]
        mycol.insert_many(data_db)
        # with open(self.ticker + ".csv", "w") as f:
        #     writer = csv.writer(f)
        #     writer.writerows(data_csv)

    def save_realtime_data(self, data_db, data_csv):
        myclient = pymongo.MongoClient('mongodb://localhost:27017/')
        mydb = myclient['stockdb']
        mycol = mydb[ticker + '_realtime']
        mycol.insert_many(data_db)
        with open(self.ticker + "_realtime.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(data_csv)

    def search(self, symbol):
        myclient = pymongo.MongoClient('mongodb://localhost:27017/')
        mydb = myclient['stockdb']
        collection_names = mydb.list_collection_names()
        if symbol not in collection_names:
            self.ticker = symbol
            self.yahoo_financials = YahooFinancials(self.ticker)
            self.url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+self.ticker+'&interval=1min&apikey=06JRP8S4736D1FE6&datatype=csv'
            historical_db, historical_csv = self.get_historical_data()
            self.save_historical_data(historical_db, historical_csv)
        mycol = mydb[symbol]
        all_data = mycol.find().sort('date', pymongo.ASCENDING)
        print(all_data.count())

        formatted_date = []
        open_data = []
        high_data = []
        low_data = []
        close_data = []

        for one_data in all_data:
            formatted_date.append(one_data.get('formatted_date'))
            open_data.append(one_data.get('open'))
            high_data.append(one_data.get('high'))
            low_data.append(one_data.get('low'))
            close_data.append(one_data.get('close'))


        final_data = dict()
        final_data['date'] = formatted_date
        final_data['open'] = open_data
        final_data['high'] = high_data
        final_data['low'] = low_data
        final_data['close'] = close_data

        return final_data

# tickers = ['AAPL']#, 'GOOGL', 'FB', 'AMZN', 'NFLX', 'TSLA', 'DELL', 'JPM', 'AMD', 'V']
# for ticker in tickers:
#     stock_dt = stock_data(ticker)
#     historical_db, historical_csv = stock_dt.get_historical_data()
#     stock_dt.save_historical_data(historical_db, historical_csv)
    # realtime_db, realtime_csv = stock_dt.get_realtime_data()
    # stock_dt.save_realtime_data(realtime_db, realtime_csv)
