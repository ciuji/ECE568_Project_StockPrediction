import os
from flask import request,jsonify,render_template
from flask.views import MethodView
from app import app
from models import  get_data
import json

class GetStockData(MethodView):
    def get(self,interval,symbol):
        if interval=='daily':
            return jsonify({'name':interval+symbol})
        if interval=='weekly':
            return jsonify({'name': interval+symbol})

app.add_url_rule('/stockdata/<interval>/symbol', view_func=GetStockData.as_view('stockdata'))

@app.route('/',methods=['POST','GET'])
def homepage():
    print('homepage')
    print(get_data())
    return render_template('index.html',data=json.dumps(get_data()),stock_name='AAPL')

@app.route('/getData',methods=['GET'])
def render_data():
    print('getData')
    #return json.dumps(get_data())

    return json.dumps(get_data())
