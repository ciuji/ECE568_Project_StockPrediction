import os
from flask import request,jsonify,render_template
from flask.views import MethodView
from app import app
from models import get_plot_data,getDailyData,getRealTime,getWeeklyData
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
        print(get_plot_data())
        return render_template('stock_chart.html',data=json.dumps(get_plot_data()),stock_name='AAPL')
    else:
        print('get homepage')
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

