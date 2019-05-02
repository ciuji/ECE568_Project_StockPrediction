import pandas as pd
import random

def get_data():
    df=pd.read_csv('data/AAPL.csv')
    #data=df.T.values.tolist()
    data=dict()
    data['date']=list(df['formatted_date'])
    data['open'] = list(df['open'])
    data['high'] = list(df['high'])
    data['low'] =list( df['low'])
    data['close'] = list(df['close'])
    return data

