from flask import Flask
from flask import make_response
from flask import request
from flask import url_for, jsonify
import os
import lib.appflow_tools as tools
import lib.appflow_yaml as apyaml
import lib.appflow_ansible as apansible
from celery import Celery
import time

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


@app.route("/appflow", methods=['PATCH'])
def set():
    try:
        resource_name = request.args.get('resource')
        key = request.args.get('key')
        value = request.args.get('value')
        response = apyaml.set_value(resource_name, key, value)
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


@app.route("/appflow",  methods=['PUT'])
def add():
    try:
        resource_name = request.args.get('resource')
        key = request.args.get('key')
        value = request.args.get('value')
        response = apyaml.add_value(resource_name, key, value)
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


@app.route("/appflow",  methods=['DELETE'])
def delete():
    try:
        resource_name = request.args.get('resource')
        key = request.args.get('key')
        response = apyaml.delete_value(resource_name, key)
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
        exec_command = request.args.get('command', default=None)
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
        response = {
            "status": output
        }
        return jsonify(response)
    except Exception as exception:
        return make_response(str(exception), 500)


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
                    'Status': 'Starting...'})


@CELERY.task(bind=True)
def provision_task(self, tenant: str, env: str, limit: str, tags: str,
                   skip_tags: str, firstrun: bool, local: bool,
                   debug: bool, user: str = None):

    print((tenant, env, limit, tags, skip_tags,
           firstrun, local, debug, user))

    self.update_state(state='PROGRESS',
                      meta={'status': 'running...'})
    response = apansible.provision(tenant, env, limit, tags, skip_tags,
                                   firstrun, local, debug, user)
    if response > 0:
        return {'status': 'Task Failed!'}
    else:
        return {'status': 'Task Completed!'}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = provision_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'status': task.info.get('status', '')
        }
    else:
        # something went wrong in the background job
        response = {
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


# @app.route("/appflow/signin",  methods=['POST'])
# @app.route("/appflow/signup/get/get_user_data",  methods=['POST'])
# @app.route("/appflow/signin/get/recover_mail",  methods=['POST'])
# @app.route("/appflow/signin/get/recover_username",  methods=['POST'])
# @app.route("/appflow/signin/get/recover_api_key",  methods=['POST'])
# @app.route("/appflow/signin/change_pass",  methods=['POST'])
# @app.route("/appflow/signin/change_mail",  methods=['POST'])
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8980)
