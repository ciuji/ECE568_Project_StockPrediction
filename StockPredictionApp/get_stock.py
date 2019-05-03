from yahoofinancials2 import YahooFinancials
import requests
import pymongo
import csv
import datetime
import sys
import numpy as np

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
        collection_names = mydb.list_collection_names()
        if self.ticker+'_realtime' in collection_names:
            mydb[self.ticker + '_realtime'].drop()
        mycol = mydb[self.ticker + '_realtime']
        mycol.insert_many(data_db)
        # with open(self.ticker + "_realtime.csv", "w") as f:
        #     writer = csv.writer(f)
        #     writer.writerows(data_csv)

    def search(self, symbol):
        self.ticker = symbol.upper()
        self.yahoo_financials = YahooFinancials(self.ticker)
        self.url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+self.ticker+'&interval=1min&apikey=06JRP8S4736D1FE6&datatype=csv'
        nsdq_names = []
        with open('data/NSDQ.txt','r') as f:
            while True:
                nsdq_name = f.readline()
                if nsdq_name:
                    nsdq_names.append(nsdq_name[:-1])
                else:
                    break
        if self.ticker not in nsdq_names:
            return False
        myclient = pymongo.MongoClient('mongodb://localhost:27017/')
        mydb = myclient['stockdb']
        try:
            if self.is_update(self.ticker):
                historical_db, historical_csv = self.get_historical_data()
                self.save_historical_data(historical_db, historical_csv)
        except:
            print("Error: get stock data error")
            return False
        mycol = mydb[symbol]
        all_data = mycol.find().sort('date', pymongo.ASCENDING)
        # print(all_data.count())

        timestamp = []
        formatted_date = []
        open_data = []
        high_data = []
        low_data = []
        close_data = []
        volume_data = []

        for one_data in all_data:
            timestamp.append(one_data.get('date'))
            formatted_date.append(one_data.get('formatted_date'))
            open_data.append(one_data.get('open'))
            high_data.append(one_data.get('high'))
            low_data.append(one_data.get('low'))
            close_data.append(one_data.get('close'))
            volume_data.append(one_data.get('volume'))


        final_data = dict()
        final_data['timestamp'] = timestamp
        final_data['date'] = formatted_date
        final_data['open'] = open_data
        final_data['high'] = high_data
        final_data['low'] = low_data
        final_data['close'] = close_data
        final_data['volume'] = volume_data

        ema = self.calculate_ema(final_data)
        final_data['ema'] = ema

        return final_data

    def is_update(self, symbol):
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        self.currentTime = str(year) + '-' + str(month) + '-' + str(day)
        self.preTime = str(year - 1) + '-' + str(month) + '-' + str(day)
        myclient = pymongo.MongoClient('mongodb://localhost:27017/')
        mydb = myclient['stockdb']
        collection_names = mydb.list_collection_names()
        if symbol not in collection_names:
            return True
        mycol = mydb[symbol]
        all_data = mycol.find().sort('date', pymongo.DESCENDING)
        collection_date = all_data[0].get('formatted_date')
        if collection_date == self.currentTime:
            return False
        else:
            return True

    def search_realtime(self, symbol):
        self.ticker = symbol.upper()
        self.yahoo_financials = YahooFinancials(self.ticker)
        self.url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+self.ticker+'&interval=1min&apikey=06JRP8S4736D1FE6&datatype=csv'
        nsdq_names = []
        with open('data/NSDQ.txt','r') as f:
            while True:
                nsdq_name = f.readline()
                if nsdq_name:
                    nsdq_names.append(nsdq_name[:-1])
                else:
                    break
        if self.ticker not in nsdq_names:
            return False
        myclient = pymongo.MongoClient('mongodb://localhost:27017/')
        mydb = myclient['stockdb']
        try:
            historical_db, historical_csv = self.get_realtime_data()
            self.save_realtime_data(historical_db, historical_csv)
        except:
            print("Error: get stock data error")
            return False
        mycol = mydb[self.ticker + '_realtime']
        all_data = mycol.find().sort('timestamp', pymongo.ASCENDING)
        print(all_data[0])
        # print(all_data.count())

        date = []
        open_data = []
        high_data = []
        low_data = []
        close_data = []
        volume_data = []

        for one_data in all_data:
            date.append(one_data.get('timestamp'))
            open_data.append(float(one_data.get('open')))
            high_data.append(float(one_data.get('high')))
            low_data.append(float(one_data.get('low')))
            close_data.append(float(one_data.get('close')))
            volume_data.append(float(one_data.get('volume')))

        final_data = dict()
        final_data['date'] = date
        final_data['open'] = open_data
        final_data['high'] = high_data
        final_data['low'] = low_data
        final_data['close'] = close_data
        final_data['volume'] = volume_data

        ema = self.calculate_ema(final_data)
        final_data['ema'] = ema

        return final_data

    def calculate_ema(self, final_data):
        close_data = final_data.get('close')
        ema = []
        for i in range(len(close_data)):
            ema.append(EMA.value(close_data[:i + 1]))
        return ema

class EMA(object):
    '''
    receive a sequence of prices (num >= 10) as an ndarray, in time order
    return the EMA of it
    '''
    @staticmethod
    def MA(vals):
        ret = 0
        for x in vals:
            ret = ret + x
        return ret / len(vals)

    @staticmethod
    def value(vals):
        if len(vals) < 10:
            return EMA.MA(vals)
        ret = EMA.MA(vals[0:10])
        vals = vals[10:]
        multiplier = 2 / (10+1)
        for x in vals:
            ret = (x - ret) * multiplier + ret
        return ret
