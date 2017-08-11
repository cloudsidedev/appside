#!/usr/bin/python3

import appflow.AppflowYaml as apyaml
from flask import Flask
from flask import request

app = Flask(__name__)

# GET -> get
# POST -> all provision commands
# PUT   -> add
# PATCH -> set
# DELETE -> rm

# 204 NO CONTENT – [DELETE]
# 304 NOT MODIFIED
# 400 INVALID REQUEST – [POST/PUT/PATCH]
# 401 UNAUTHORIZED
# 403 FORBIDDEN
# 404 NOT FOUND
# 500 INTERNAL SERVER ERROR


@app.route("/appflow/get")
def get():
    file_name = request.args.get('file')
    key = request.args.get('key')
    return (apyaml.get(file_name, key))


@app.route("/appflow/set")
def set():
    file_name = request.args.get('file')
    key = request.args.get('key')
    value = request.args.get('value')
    return (apyaml.set(file_name, key, value))


@app.route("/appflow/add")
def add():
    file_name = request.args.get('file')
    key = request.args.get('key')
    value = request.args.get('value')
    return (apyaml.add(file_name, key, value))


@app.route("/appflow/rm")
def rm():
    file_name = request.args.get('file')
    key = request.args.get('key')
    return (apyaml.rm(file_name, key))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
