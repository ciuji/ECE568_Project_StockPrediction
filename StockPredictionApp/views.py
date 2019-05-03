import os
from flask import request,jsonify,render_template
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
        search_data=GetStock.search(search_symbol)
        print("user searching symbol: "+search_symbol)
        if(search_symbol==''):
            print('no query')
            return render_template('stock_chart.html')
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

@app.route('/stockInfo',methods=['GET'])
def getStockInfo():
    check_result=checkReqeustParams(args=request.args,parametersList=['stockTicker','infoType'],requestName='stockInfo')
    if check_result:
        return jsonify(check_result)
    else:
        s_type=request.args.get('infoType')
        '''do return by infoType'''
        print('get stock infomation:'+request.args.get('infoType')+' of '+request.args.get('stockTicker'))
        print(request.args.get('stockTicker'))
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
    check_result=checkReqeustParams(args=request.args,parametersList=['stockTicker','predType'],requestName='stockPredicition')
    if check_result:
        return jsonify(check_result)
    else:
        s_Ticker=request.args.get('stockTicker')
        predict_data=GetStock.search(s_Ticker)
        print('get stock infomation:'+request.args.get('predType')+' of '+request.args.get('stockTicker'))
        '''do predicition'''
        time.sleep(5)
        return jsonify(float(33.134))
