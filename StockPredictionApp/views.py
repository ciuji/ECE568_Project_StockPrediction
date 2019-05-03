import os

import numpy as np
from prediction_engine.bayes import Bayes
from prediction_engine.dnn import DNN
from prediction_engine.svr_zhu import SupportVectorRegression

from flask import request,jsonify,render_template
from flask.views import MethodView
from app import app
from models import get_plot_data,getDailyData,getRealTime,getWeeklyData,GetStock
import json


api_version='/api/v0'
class GetStockData(MethodView):
    def get(self,interval,symbol):
        if interval=='daily':
            return jsonify({'name':interval+symbol})
        if interval=='weekly':
            return jsonify({'name': interval+symbol})

app.add_url_rule(api_version+'/stockdata/<interval>/<symbol>', view_func=GetStockData.as_view('stockdata'))

@app.route('/',methods=['POST','GET'])
def homepage():
    if(request.method=='POST'):
        search_symbol=request.form['search']
        search_data=GetStock.search(search_symbol)
        print("user searching symbol: "+search_symbol)
        if(search_symbol==''):
            print('no query')
            return render_template('stock_chart.html')
        print(search_data)
        if search_data:
            return render_template('stock_chart.html',data=json.dumps(search_data),stock_name=search_symbol)
        else:
            return render_template('stock_chart.html',sign='no such stock: '+search_symbol)
    else:
        print('GET homepage')
        return render_template('stock_chart.html')

@app.route('/mytest',methods=['GET'])
def testfunc():
    return 'mystring'


@app.route('/mystring')
def mystring():
    return 'my string'

@app.route('/dataFromAjax')
def dataFromAjax():
    test = request.args.get('mydata')
    print(test)
    return 'dataFromAjax'

@app.route('/mydict', methods=['GET', 'POST'])
def mydict():
    d = {'name': 'xmr', 'age': 18}
    return jsonify(d)

@app.route('/mylist')
def mylist():
    l = ['xmr', 18]
    return jsonify(l)

@app.route('/predict')
def predict(dict):
    price = dict.get('close')
    time = dict.get('date')
    predict_time = time[0]

    bayes = Bayes.predict(time, price, np.array(predict_time).reshape(-1, 1))
    svr = SupportVectorRegression.predict(time, price, np.array(predict_time).reshape(-1, 1))
    dnn = DNN.predict(time, price, np.array(predict_time).reshape(-1, 1))

    # r = getDailyData(request.args['symbol'], request.args['timestamp'], 252)
    # time = np.array(r['timestamp']).reshape(-1, 1)
    # price = np.array(r['open'])
    #
    # predict_time = arrow.get(request.args['timestamp']).timestamp
    #
    # bayes = Bayes.predict(time, price, np.array(predict_time).reshape(-1, 1))
    # svr = SupportVectorRegression.predict(time, price, np.array(predict_time).reshape(-1, 1))
    # dnn = DNN.predict(time, price, np.array(predict_time).reshape(-1, 1))

    # dnn = svr[0]

    res = {
        'result': [
            {'name': 'Bayes', 'price': bayes[0]},
            {'name': 'Support Vector Regression', 'price': svr[0]},
            {'name': 'Deep Neural Network', 'price': dnn}
        ]
    }
    return jsonify(res)



