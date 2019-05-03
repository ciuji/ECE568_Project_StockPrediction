import os
from flask import request,jsonify,render_template,redirect,url_for
from flask.views import MethodView
from app import app
from models import *
import json
import time

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
        print(search_symbol)
        search_data=GetStock.search(search_symbol)
        print("historical post: "+search_symbol)
        return redirect(url_for('homepage',stockTicker=search_symbol))
    else:
        if (request.args.get('stockTicker')):
            search_symbol = request.args.get('stockTicker')
            print("historical get: " + search_symbol)
            search_data = GetStock.search(search_symbol)
        else:
            return render_template('stock_chart.html', tickerList=json.dumps(getTickerList()))
    if (search_symbol == ''):
        print('no query')
        return render_template('stock_chart.html', tickerList=json.dumps(getTickerList()))
    if search_data:
        return render_template('stock_chart.html', data=json.dumps(search_data), stock_name=search_symbol,
                               tickerList=json.dumps(getTickerList()))
    else:
        return render_template('stock_chart.html', sign='no such stock: ' + search_symbol,
                               tickerList=json.dumps(getTickerList()))

@app.route('/realTimeStock',methods=['POST','GET'])
def realTimeStock():
    if(request.method=='POST'):
        search_symbol=request.form['search']
        print(search_symbol)
        print("real time post: "+search_symbol)
        return redirect(url_for('realTimeStock',stockTicker=search_symbol))
    else:
        if (request.args.get('stockTicker')):
            search_symbol = request.args.get('stockTicker')
            print("real time get: " + search_symbol)
            search_data = GetStock.search_realtime(search_symbol)
        else:
            return render_template('real_time.html', tickerList=json.dumps(getTickerList()))
    if(search_symbol==''):
        print('no query')
        return render_template('real_time.html',tickerList=json.dumps(getTickerList()))
    if search_data:
        return render_template('real_time.html', real_time_data=json.dumps(search_data),stock_name=search_symbol,tickerList=json.dumps(getTickerList()))
    else:
        return render_template('real_time.html',sign='no such stock: '+search_symbol,tickerList=json.dumps(getTickerList()))


@app.route('/stockInfo',methods=['GET'])
def getStockInfo():
    check_result=checkReqeustParams(args=request.args,parametersList=['stockTicker','infoType'],requestName='stockInfo')
    if check_result:
        return jsonify(check_result)
    else:
        s_type=request.args.get('infoType')
        '''do return by infoType'''
        print('get stock infomation:'+request.args.get('infoType')+' of '+request.args.get('stockTicker'))
        s_Ticker = request.args.get('stockTicker')
        if s_type == 'high':
            highest = get_stock_highest(s_Ticker)
            return jsonify(float(highest))
        if s_type == 'low':
            lowest = get_stock_lowest(s_Ticker)
            return jsonify(float(lowest))
        if s_type == 'average':
            average = get_stock_average(s_Ticker)
            return jsonify(float(average))
        else:
            return typeErrorResponse(s_type)


@app.route('/stockPrediction',methods=['GET'])
def getStockPredicition():
    check_result=checkReqeustParams(args=request.args,parametersList=['stockTicker','predType','predPeriod'],requestName='stockPredicition')

    if check_result:
        return jsonify(check_result)
    else:
        predType = request.args.get('predType')
        s_Ticker = request.args.get('stockTicker')
        predPeriod = request.args.get('predPeriod')

        predict_data = GetStock.search(s_Ticker)
        print('get stock infomation:' + request.args.get('predType') + ' of ' + request.args.get('stockTicker'))
        if predPeriod == 'longTerm':
            if predType == 'dnn':
                res = predictDNN(predict_data, 250)
                return jsonify(float(res))
            elif predType == 'svr':
                res = predictSVR(predict_data, 250)
                return jsonify(float(res))
            elif predType == 'bayes':
                res = predictBayes(predict_data, 250)
                return jsonify(float(res))
            else:
                return typeErrorResponse(predType)
        elif predPeriod == 'shortTerm':
            if predType == 'dnn':
                res = predictDNN(predict_data, 50)
                return jsonify(float(res))
            elif predType == 'svr':
                res = predictSVR(predict_data, 50)
                return jsonify(float(res))
            elif predType == 'bayes':
                res = predictBayes(predict_data, 50)
                return jsonify(float(res))
            else:
                return typeErrorResponse(predType)
        else:
            return typeErrorResponse(predPeriod)
