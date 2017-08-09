#!/usr/bin/python3

import AppflowYaml as apyaml
from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/appflow/get")
def get():
    file = request.args.get('file')
    key = request.args.get('key')
    return (apyaml.get(file, key))


@app.route("/appflow/set")
def set():
    file = request.args.get('file')
    key = request.args.get('key')
    value = request.args.get('value')
    return (apyaml.set(file, key, value))


@app.route("/appflow/add")
def add():
    file = request.args.get('file')
    key = request.args.get('key')
    value = request.args.get('value')
    return (apyaml.add(file, key, value))


@app.route("/appflow/rm")
def rm():
    file = request.args.get('file')
    key = request.args.get('key')
    return (apyaml.rm(file, key))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
