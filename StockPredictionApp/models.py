import pandas as pd
import numpy as np
import random
from get_stock import *
from werkzeug.datastructures import ImmutableMultiDict
from typing import List, Dict, Union
from datetime import datetime
import pymongo
from prediction_engine.dnn import DNN
from prediction_engine.bayes import Bayes
from prediction_engine.svr import SupportVectorRegression
GetStock=Stock_data()

def get_plot_data():
    df=pd.read_csv('data/AAPL.csv')
    #data=df.T.values.tolist()
    data=dict()
    data['date']=list(df['formatted_date'])
    data['open'] = list(df['open'])
    data['high'] = list(df['high'])
    data['low'] =list( df['low'])
    data['close'] = list(df['close'])
    return data

def getDailyData(symbol):
    return {'time slot':'daily'}

def getWeeklyData(symbol):
    return {'time slot':'weekly'}

def getRealTime(symbol):
    return {'time slot':'RealTime'}

def checkReqeustParams(
        args:ImmutableMultiDict,
        parametersList: List[str],
        requestName:str):
    missing_parameter=[]
    for parameter in parametersList:
        if parameter not in args:
            missing_parameter.append(parameter)
    if missing_parameter:
        return {
            'type': 'error',
            'time': datetime.now(),
            'error': {
                'requestName':requestName,
                'errorInfo': 'Missing parameters',
                'missingParameters': missing_parameter
            }
        }
    else:
        return False

def typeErrorResponse(ReqType:str):
    return {
        'type': 'error',
        'time': datetime.now(),
        'error': {
            'WrongType': ReqType,
            'errorInfo': 'Invalid value',
        }
    }

def termErrorResponse(ReqTerm:str):
    return {
        'type': 'error',
        'time': datetime.now(),
        'error': {
            'WrongType': ReqTerm,
            'errorInfo': 'Invalid value',
        }
    }

def get_stock_highest(symbol):
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['stockdb']
    mycol = mydb[symbol]
    all_data = mycol.find().sort('high', pymongo.DESCENDING)
    return all_data[0].get('high')

def get_stock_lowest(symbol):
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['stockdb']
    mycol = mydb[symbol]
    all_data = mycol.find().sort('low', pymongo.ASCENDING)
    return all_data[0].get('low')

def get_stock_average(symbol):
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['stockdb']
    mycol = mydb[symbol]
    all_data = mycol.find()
    all_price = 0
    for one_data in all_data:
        all_price += one_data.get('close')
    return all_price / all_data.count()


def predictBayes(dict, period = 50):
    price = np.array(dict['close'][-period:])
    time = np.array(dict['timestamp'][-period:])
    predict_time = time[-1]

    time = time.reshape(-1, 1)
    bayes = Bayes.predict(time, price, np.array(predict_time).reshape(-1,1))

    return bayes[0]

def predictDNN(dict, period = 50):
    price = np.array(dict['close'][-period:])
    time = np.array(dict['timestamp'][-period:])
    predict_time = time[-1]

    dnn = DNN.predict(time, price, np.array(predict_time).reshape(-1, 1))

    return dnn

def predictSVR(dict, period = 50):
    price = np.array(dict['close'][-period:])
    time = np.array(dict['timestamp'][-period:])
    predict_time = time[-1]

    time = time.reshape(-1,1)
    svr = SupportVectorRegression.predict(time, price, np.array(predict_time).reshape(-1, 1))

    return svr[0]

def getTickerList():
    tickerList = []
    file_object = open('data/NSDQ.txt', 'rU')
    try:
        for line in file_object:
            tickerList.append(line.strip().split('\t')[0])
    finally:
        file_object.close()
    return tickerList
