import json
import os
import yaml
import appflow.AppflowUtils as utils


def get(file, key=None):
    file = file.replace('.', '/', 3)
    if (file != 'config'):
        fileName = os.getenv("HOME") + "/.appflow/tenant/" + file
    else:
        fileName = os.getenv("HOME") + "/.appflow/" + file
    ##
    # print(fileName)
    if not os.path.exists(fileName):
        return ('No such File or Directory')
    if file.split('/').pop() == 'inventory':
        return
    if (os.path.isdir(fileName)):
        for subfile in os.listdir(fileName):
            self.get(file.replace('/', '.', 3) + '.' + subfile)
    else:
        with open(fileName, 'r') as stream:
            conf = yaml.safe_load(stream)
            if (key != None and type(key) != 'NoneType'):
                key = key.split('.')
                return (json.dumps(utils.getFromDict(conf, key),
                                   ensure_ascii=False, indent=4))
            else:
                return (json.dumps(conf, ensure_ascii=False, indent=4))


def set(file, key, value):
    file = file.replace('.', '/', 3)
    key = key.split('.')
    if (file != 'config'):
        fileName = os.getenv("HOME") + "/.appflow/tenant/" + file
    else:
        fileName = os.getenv("HOME") + "/.appflow/" + file
    with open(fileName, 'r') as stream:
        conf = yaml.safe_load(stream)
        utils.setInDict(conf, key, value)
    with open(fileName, 'w') as outfile:
        yaml.dump(conf, outfile, default_flow_style=False,
                  indent=4, default_style='')
    return json.dumps(conf, ensure_ascii=False, indent=4)


def rm(file, key):
    file = file.replace('.', '/', 3)
    key = key.split('.')
    if (file != 'config'):
        fileName = os.getenv("HOME") + "/.appflow/tenant/" + file
    else:
        fileName = os.getenv("HOME") + "/.appflow/" + file
    with open(fileName, 'r') as stream:
        conf = yaml.safe_load(stream)
        utils.rmInDict(conf, key)
    with open(fileName, 'w') as outfile:
        yaml.dump(conf, outfile, default_flow_style=False,
                  indent=4, default_style='')
    return json.dumps(conf, ensure_ascii=False, indent=4)


def add(file, key, value):
    file = file.replace('.', '/', 3)
    key = key.split('.')
    if (file != 'config'):
        fileName = os.getenv("HOME") + "/.appflow/tenant/" + file
    else:
        fileName = os.getenv("HOME") + "/.appflow/" + file
    with open(fileName, 'r') as stream:
        conf = yaml.safe_load(stream)
    d = {}
    utils.add_keys(d, key, value)
    myDicts = [conf, d]
    for a in myDicts:
        for k, v in a.items():
            conf[k].update(v)
    with open(fileName, 'w') as outfile:
        yaml.dump(conf, outfile, default_flow_style=False,
                  indent=4, default_style='')
    return (json.dumps(conf, ensure_ascii=False, indent=4))
