#!/usr/bin/env python
#-*- coding:utf-8 -*-

from bottle import get, route, request, default_app
import requests


@get("/okex/api/v1/future_ticker.do")
def okex_future_ticker():
    request.query.get('a', 'default')
    symbol = request.query.symbol
    contract_type = request.query.contract_type
    url = 'https://www.okex.com/api/v1/future_ticker.do?symbol=%s&contract_type=%s' % (symbol, contract_type)
    js = requests.get(url)
    return js.json()


@get("/okex/api/v1/future_")
def okex_ ():
    pass


@route('/')
def hello_world():
    return "hellokitty"

application = default_app()
