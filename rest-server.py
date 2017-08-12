#!/usr/bin/python3

import appflow.AppflowYaml as apyaml
import appflow.AppflowAnsible as apansible
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


@app.route("/appflow/get", methods=['GET'])
def get():
    file_name = request.args.get('file')
    key = request.args.get('key')
    return (apyaml.get(file_name, key))


@app.route("/appflow/set", methods=['PATCH'])
def set():
    file_name = request.args.get('file')
    key = request.args.get('key')
    value = request.args.get('value')
    return (apyaml.set(file_name, key, value))


@app.route("/appflow/add",  methods=['PUT'])
def add():
    file_name = request.args.get('file')
    key = request.args.get('key')
    value = request.args.get('value')
    return (apyaml.add(file_name, key, value))


@app.route("/appflow/rm",  methods=['DELETE'])
def rm():
    file_name = request.args.get('file')
    key = request.args.get('key')
    return (apyaml.rm(file_name, key))


@app.route("/appflow",  methods=['POST'])
def command():
    command = request.args.get('command', default='', type=str)
    tenant = request.args.get('tenant', default='', type=str)
    env = request.args.get('env', default='', type=str)
    tags = 'tags=' + request.args.get('tags', default='', type=str)
    skip_tags = 'skip_tags=' + \
        request.args.get('skip_tags', default='', type=str)
    limit = 'limit=' + request.args.get('limit', default='', type=str)
    ask_sudo_pass = 'ask_sudo_pass=' + \
        request.args.get('ask_sudo_pass', default='', type=str)
    user = 'user=' + request.args.get('user', default='', type=str)

    # apansible.provision(tenant, env, tags, skip_tags, limit, ask_sudo_pass, user)
    return 'Test'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
