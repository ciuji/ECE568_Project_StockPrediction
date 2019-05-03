import pandas as pd
import random
from get_stock import *
from werkzeug.datastructures import ImmutableMultiDict
from typing import List, Dict, Union
from datetime import datetime
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