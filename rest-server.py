#!/usr/bin/python3

import appflow.AppflowYaml as apyaml
import appflow.AppflowAnsible as apansible
import appflow.AppflowTools as tools
import appflow.AppflowUtils as utils
import appflow.AppflowSQL as sql
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

# GET -> get
# POST -> all provision commands
# PUT   -> add
# PATCH -> set
# DELETE -> rm

# 204 NO CONTENT – [DELETE/POST/PUT/PATCH]
# 400 INVALID REQUEST – [DELETE/POST/PUT/PATCH]
# 400 MISSING ARGUMENTS [maybe for the registration/signin]
# 401 UNAUTHORIZED -> Maybe if we use api tokens???
# 403 FORBIDDEN -> Maybe if we use api tokens???
# 404 NOT FOUND -> Invalid Command or syntax
# 405 METHOD NOT ALLOWED -> Invalid Command or syntax
# 500 INTERNAL SERVER ERROR

# use db;
# select * from users \G;
# CREATE TABLE users(username TEXT, mail TEXT, password TEXT, salt TEXT, tenant TEXT, api_key TEXT, api_quota INT, user_enc TEXT, mail_enc TEXT, api_key_enc TEXT);

# https://blog.miguelgrinberg.com/post/restful-authentication-with-flask
# https://github.com/miguelgrinberg/REST-auth
# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask --> Securing a RESTful web service
# https://www.owasp.org/index.php/REST_Security_Cheat_Sheet#Access_Control

@app.route("/appflow/get", methods=['GET'])
def get():
    try:
        file_name = request.args.get('file')
        key = request.args.get('key')

        response = apyaml.get(file_name, key)
        if 'Error' in response:
            if 'Invalid' in response:
                status_code = 400
            elif 'Bad Syntax' in response:
                status_code = 404
            elif 'Not Found' in response:
                status_code = 204
            else:
                status_code = 500
        else:
            status_code = 200
        return make_response(response, status_code)
    except Exception as exception:
        return make_response(str(exception), 500)


@app.route("/appflow/set", methods=['PATCH'])
def set():
    try:
        file_name = request.args.get('file')
        key = request.args.get('key')
        value = request.args.get('value')
        response = apyaml.set(file_name, key, value)
        if 'Error' in response:
            if 'Invalid' in response:
                status_code = 400
            elif 'Bad Syntax' in response:
                status_code = 404
            elif 'Not Found' in response:
                status_code = 204
            else:
                status_code = 500
        else:
            status_code = 200
        return make_response(response, status_code)

    except Exception as exception:
        return make_response(str(exception), 500)


@app.route("/appflow/add",  methods=['PUT'])
def add():
    try:
        file_name = request.args.get('file')
        key = request.args.get('key')
        value = request.args.get('value')
        response = apyaml.add(file_name, key, value)
        if 'Error' in response:
            if 'Invalid' in response:
                status_code = 400
            elif 'Bad Syntax' in response:
                status_code = 404
            elif 'Not Found' in response:
                status_code = 204
            else:
                status_code = 500
        else:
            status_code = 200
        return make_response(response, status_code)

    except Exception as exception:
        return make_response(str(exception), 500)


@app.route("/appflow/rm",  methods=['DELETE'])
def rm():
    try:
        file_name = request.args.get('file')
        key = request.args.get('key')
        response = apyaml.rm(file_name, key)
        if 'Error' in response:
            if 'Invalid' in response:
                status_code = 400
            elif 'Bad Syntax' in response:
                status_code = 404
            elif 'Not Found' in response:
                status_code = 204
            else:
                status_code = 500
        else:
            status_code = 200
        return make_response(response, status_code)

    except Exception as exception:
        return make_response(str(exception), 500)


@app.route("/appflow",  methods=['POST'])
def command():
    try:
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

        return {
            'reset': tools.git_reset(tenant, env),
            'status': tools.git_status(tenant, env),
            'checkin': tools.git_checkin(tenant, env),
            'checkout': tools.git_checkOut(tenant, env),
            'encrypt': apansible.encrypt(tenant, env),
            'decrypt': apansible.decrypt(tenant, env),
            'tags': apansible.tags(tenant, env),
            'provision': apansible.provision(tenant, env, tags, skip_tags, limit, ask_sudo_pass, user)
        }.get(env, 'development')
    except Exception as exception:
        return make_response(str(exception), 500)


@app.route("/appflow/signin",  methods=['POST'])
@app.route("/appflow/signup/get/get_user_data",  methods=['POST'])
@app.route("/appflow/signin/get/recover_mail",  methods=['POST'])
@app.route("/appflow/signin/get/recover_username",  methods=['POST'])
@app.route("/appflow/signin/get/recover_api_key",  methods=['POST'])
@app.route("/appflow/signin/change_pass",  methods=['POST'])
@app.route("/appflow/signin/change_mail",  methods=['POST'])
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
