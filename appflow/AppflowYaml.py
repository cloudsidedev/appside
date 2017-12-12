import json
import os
# import re

import yaml

import appflow.AppflowUtils as utils


def get_value(my_file, key=None):
    # pattern = re.compile("^[a-zA-Z\.-]*$")
    # if not (pattern.match(my_file)):
    #     return 'Error: Bad Syntax'
    # if not (pattern.match(key)):
    #     return 'Error: Bad Syntax'
    my_file = my_file.replace('.', '/', 3)
    if my_file != 'config':
        file_name = os.getenv("HOME") + "/.appflow/tenant/" + my_file
    else:
        file_name = os.getenv("HOME") + "/.appflow/" + my_file + ".yml"

    if not os.path.exists(file_name):
        return 'Error: No such File or Directory'
    if my_file.split('/').pop() == 'inventory':
        return 'Error: Invalid Request'
    if os.path.isdir(file_name):
        for subfile in os.listdir(file_name):
            get_value(my_file.replace('/', '.', 3) + '.' + subfile)
    else:
        with open(file_name, 'r') as stream:
            conf = yaml.safe_load(stream)
            if key is not None:
                key = key.split('.')
                return json.dumps(utils.get_from_dict(conf, key),
                                  ensure_ascii=False, indent=4)
            else:
                return json.dumps(conf, ensure_ascii=False, indent=4)


def set_value(my_file, key, value):
    # pattern = re.compile("^[a-zA-Z\._-]*$")
    # if not (pattern.match(my_file)):
    #     return 'Error: Bad Syntax'
    # if not (pattern.match(key)):
    #     return 'Error: Bad Syntax'
    my_file = my_file.replace('.', '/', 3)
    key = key.split('.')
    if my_file != 'config':
        file_name = os.getenv("HOME") + "/.appflow/tenant/" + my_file
    else:
        file_name = os.getenv("HOME") + "/.appflow/" + my_file
    if not os.path.exists(file_name):
        return 'Error: No such File or Directory'
    if my_file.split('/').pop() == 'inventory':
        return 'Error: Invalid Request'
    with open(file_name, 'r') as stream:
        conf = yaml.safe_load(stream)
        utils.set_in_dict(conf, key, value)
    with open(file_name, 'w') as outfile:
        yaml.dump(conf, outfile, default_flow_style=False,
                  indent=4, default_style='')
    return json.dumps(conf, ensure_ascii=False, indent=4)


def rm_value(my_file, key):
    # pattern = re.compile("^[a-zA-Z\._-]*$")
    # if not (pattern.match(my_file)):
    #     return 'Error: Bad Syntax'
    # if not (pattern.match(key)):
    #     return 'Error: Bad Syntax'
    my_file = my_file.replace('.', '/', 3)
    key = key.split('.')
    if my_file != 'config':
        file_name = os.getenv("HOME") + "/.appflow/tenant/" + my_file
    else:
        file_name = os.getenv("HOME") + "/.appflow/" + my_file
    if not os.path.exists(file_name):
        return 'Error: No such File or Directory'
    if my_file.split('/').pop() == 'inventory':
        return 'Error: Invalid Request'
    with open(file_name, 'r') as stream:
        conf = yaml.safe_load(stream)
        utils.rm_in_dict(conf, key)
    with open(file_name, 'w') as outfile:
        yaml.dump(conf, outfile, default_flow_style=False,
                  indent=4, default_style='')
    return json.dumps(conf, ensure_ascii=False, indent=4)


def add_value(my_file, _key, _value):
    # pattern = re.compile("^[a-zA-Z\._-]*$")
    # if not (pattern.match(my_file)):
    #     return 'Error: Bad Syntax'
    # if not (pattern.match(key)):
    #     return 'Error: Bad Syntax'
    my_file = my_file.replace('.', '/', 3)
    _key = _key.split('.')
    if my_file != 'config':
        file_name = os.getenv("HOME") + "/.appflow/tenant/" + my_file
    else:
        file_name = os.getenv("HOME") + "/.appflow/" + my_file
    if not os.path.exists(file_name):
        return 'Error: No such File or Directory'
    if my_file.split('/').pop() == 'inventory':
        return 'Error: Invalid Request'
    with open(file_name, 'r') as stream:
        conf = yaml.safe_load(stream)
    dictionary = {}
    utils.add_keys(dictionary, _key, _value)
    my_dicts = [conf, dictionary]
    for item in my_dicts:
        for _key, _value in item.items():
            conf[_key].update(_value)
    with open(file_name, 'w') as outfile:
        yaml.dump(conf, outfile, default_flow_style=False,
                  indent=4, default_style='')
    return json.dumps(conf, ensure_ascii=False, indent=4)
