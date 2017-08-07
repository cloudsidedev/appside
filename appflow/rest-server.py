#!/usr/bin/python3

import apconf as apconf
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/appflow/get")
def get():
    appflowConfigurator = apconf.AppFlow()
    file = request.args.get('file')
    key = request.args.get('key')
    return (appflowConfigurator.get(file, key))


@app.route("/appflow/set")
def set():
    appflowConfigurator = apconf.AppFlow()
    file = request.args.get('file')
    key = request.args.get('key')
    value = request.args.get('value')
    return (appflowConfigurator.set(file, key, value))


@app.route("/appflow/add")
def add():
    appflowConfigurator = apconf.AppFlow()
    file = request.args.get('file')
    key = request.args.get('key')
    value = request.args.get('value')
    return (appflowConfigurator.add(file, key, value))


@app.route("/appflow/rm")
def rm():
    appflowConfigurator = apconf.AppFlow()
    file = request.args.get('file')
    key = request.args.get('key')
    return (appflowConfigurator.rm(file, key))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
