#!/usr/bin/env python
#-*- coding:utf-8 -*-

from bottle import run,get, route, request, default_app
import requests

#http://45.77.233.131:8080/okex/api/v1/future_tiker.do?symbol=
@get("/okex/api/v1/future_ticker.do")
def okex_future_ticker():
    symbol = request.query.symbol
    contract_type = request.query.contract_type
    url = 'https://www.okex.com/api/v1/future_ticker.do?symbol=%s&contract_type=%s' % (symbol, contract_type)
    js = requests.get(url)
    return js.json()


@get("/okex/api/v1/future_kline.do")
def okex_future_kline():
    symbol = request.query.symbol
    contract_type = request.query.contract_type
    type = request.query.type
    size = request.query.size
    since = request.query.since
    url = 'https://www.okex.com/api/v1/future_kline.do?symbol=%s&contract_type=%s&type=%s&size=%s' % (symbol, contract_type,type, size)
    js = requests.get(url)
    return js.json()
    


@route('/')
def hello_world():
    return "hellokitty"

run(host="0.0.0.0")