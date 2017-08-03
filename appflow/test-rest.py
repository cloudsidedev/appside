#!/usr/bin/python3

import apconf as apconf
from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/appflow")
def appflow():
    appflowConfigurator = apconf.AppFlow()
    return (appflowConfigurator.get('config'))
    #print(type(appflowConfigurator.get('config', 'tenant.ttss')))
    #return "test1"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
