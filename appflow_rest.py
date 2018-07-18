import numbers
import os
import time
import asyncio

from celery import Celery
from flask import Flask, jsonify, make_response, request, url_for
from flask_sqlalchemy import SQLAlchemy
from asyncio.subprocess import PIPE

import lib.appflow_ansible as apansible
import lib.appflow_tools as tools
import lib.appflow_utils as utils
import lib.appflow_yaml as apyaml


# redis-server
# celery worker -A appflow_rest.CELERY --loglevel=info
# python3 ./appflow_rest.py

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
CELERY = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
CELERY.conf.update(app.config)


# TODO: devo mettere i giusti exit status
# i giusti check di autenticazione
# creare le funzioni di registrazione, login e recupero dati utente

# 202 ACCEPTED - appflow provision
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


@app.route("/appflow", methods=['GET'])
def get():
    try:
        resource_name = request.args.get('resource')
        key = request.args.get('key')

        response = apyaml.get_value(resource_name, key)
        return make_response(response, utils.get_status_code(response))
    except Exception as exception:
        return make_response(str(exception), utils.INTERNAL_ERROR)


@app.route("/appflow", methods=['PATCH'])
def set():
    try:
        resource_name = request.args.get('resource')
        key = request.args.get('key')
        value = request.args.get('value')
        response = apyaml.set_value(resource_name, key, value)
        return make_response(response, utils.get_status_code(response))
    except Exception as exception:
        return make_response(str(exception), utils.INTERNAL_ERROR)


@app.route("/appflow",  methods=['PUT'])
def add():
    try:
        resource_name = request.args.get('resource')
        key = request.args.get('key')
        value = request.args.get('value')
        response = apyaml.add_value(resource_name, key, value)
        return make_response(response, utils.get_status_code(response))
    except Exception as exception:
        return make_response(str(exception), utils.INTERNAL_ERROR)


@app.route("/appflow",  methods=['DELETE'])
def delete():
    try:
        resource_name = request.args.get('resource')
        key = request.args.get('key')
        response = apyaml.delete_value(resource_name, key)
        return make_response(response, utils.get_status_code(response))
    except Exception as exception:
        return make_response(str(exception), utils.INTERNAL_ERROR)


@app.route("/appflow/<exec_command>",  methods=['POST'])
def command(exec_command):
    try:
        # exec_command = request.args.get('command', default=None)
        tenant = request.args.get('tenant', default=None)
        env = request.args.get('env', default=None)
        repo = request.args.get('repo', default=None)

        switcher = {
            'init': lambda: tools.initialize(tenant, env, repo),
            'reset': lambda: tools.git_reset(tenant, env),
            'status': lambda: tools.git_status(tenant, env),
            'checkin': lambda: tools.git_check_in(tenant, env, 'Auto Commit'),
            'checkout': lambda: tools.git_check_out(tenant, env),
            'encrypt': lambda: apansible.encrypt(tenant, env),
            'decrypt': lambda: apansible.decrypt(tenant, env),
            'tags': lambda: apansible.list_tags(tenant, env)
        }
        func = switcher.get(exec_command, lambda: "Invalid Command")
        output = func()
        if isinstance(output, numbers.Number):
            output = utils.TASK_SUCCESS if output is 0 else utils.TASK_FAIL
        response = {
            "status": output
        }
        return jsonify(response)
    except Exception as exception:
        return make_response(str(exception), utils.INTERNAL_ERROR)


@app.route("/appflow/provision", methods=['POST'])
def provision():
    tenant = request.args.get('tenant', default=None)
    env = request.args.get('env', default=None)
    tags = request.args.get('tags', default=None)
    skip_tags = request.args.get('skip_tags', default=None)
    limit = request.args.get('limit', default=None)
    first_run = request.args.get('first_run', default=False)
    user = request.args.get('user', default=None)
    debug = request.args.get('debug', default=False)

    task = provision_task.apply_async(args=[tenant, env, limit, tags, skip_tags,
                                            first_run, False, debug, user])

    return jsonify({'Response': 202,
                    'Location': url_for('taskstatus', task_id=task.id),
                    'Status': utils.TASK_START})


@CELERY.task(bind=True)
def provision_task(self, tenant: str, env: str, limit: str, tags: str,
                   skip_tags: str, firstrun: bool, local: bool,
                   debug: bool, user: str = None):

    print(type(self))
    print((tenant, env, limit, tags, skip_tags,
           firstrun, local, debug, user))

    self.update_state(state='PROGRESS',
                      meta={'status': utils.TASK_START, 'output': ""})

    tags_argument = apansible.provision(tenant, env, limit, tags,
                                        skip_tags, firstrun, local,
                                        debug, user, remote=True)

    loop = asyncio.get_event_loop()
    # Pass self as argument to do continuous update_state
    rc, *output = loop.run_until_complete(
        utils.read_and_display(loop, *tags_argument, task=self))
    loop.close()

    if rc > 0:
        return {'status': utils.TASK_FAIL, 'output': output}
    else:
        return {'status': utils.TASK_SUCCESS, 'output': output}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = provision_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'status': utils.TASK_START
        }
    elif task.state != 'FAILURE':
        response = {
            'status': task.info.get('status', ''),
            'output': task.info.get('output', '')
        }
    else:
        # something went wrong in the background job
        response = {
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


@app.route("/appflow/signup",  methods=['POST'])
def prova():
    import lib.appflow_sql as apsql
    apsql.init_db()
    user1 = apsql.query_user('luca')
    tenant1 = apsql.query_tenant('TTSS')
    # apsql.insert_key('123', 12, '123=', user1, tenant1)
    # apsql.insert_tenant('TTSS', 'secret', 'TTSS-recover')
    # apsql.insert_user('Luca', 'luca@mail.com', 'password', 'salt', 'luca-recover', 'mail_recover', 'TTSS')
    apsql.get_users()
    return 'ok'

# @app.route("/appflow/login",  methods=['POST'])
# def signin():

# @app.route("/appflow/user",  methods=['POST'])
# def signin():


# @app.route("/appflow/signup/get/get_user_data",  methods=['POST'])
# @app.route("/appflow/signin/get/recover_mail",  methods=['POST'])
# @app.route("/appflow/signin/get/recover_username",  methods=['POST'])
# @app.route("/appflow/signin/get/recover_api_key",  methods=['POST'])
# @app.route("/appflow/signin/change_pass",  methods=['POST'])
# @app.route("/appflow/signin/change_mail",  methods=['POST'])
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8980)
