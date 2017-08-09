#!/usr/bin/python3

import AppflowYaml as apyaml
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/appflow/get")
def get():
    appflowConfigurator = apyaml.AppFlow()
    file = request.args.get('file')
    key = request.args.get('key')
    return (appflowConfigurator.get(file, key))


@app.route("/appflow/set")
def set():
    appflowConfigurator = apyaml.AppFlow()
    file = request.args.get('file')
    key = request.args.get('key')
    value = request.args.get('value')
    return (appflowConfigurator.set(file, key, value))


@app.route("/appflow/add")
def add():
    appflowConfigurator = apyaml.AppFlow()
    file = request.args.get('file')
    key = request.args.get('key')
    value = request.args.get('value')
    return (appflowConfigurator.add(file, key, value))


@app.route("/appflow/rm")
def rm():
    appflowConfigurator = apyaml.AppFlow()
    file = request.args.get('file')
    key = request.args.get('key')
    return (appflowConfigurator.rm(file, key))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
