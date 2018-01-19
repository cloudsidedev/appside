"""
Appflow Yaml utilities.
This contains all the functions needed to manipulate yaml files.
Handy for configs and for tenant setups.
"""
import json
import os

import yaml

import lib.appflow_utils as utils


def get_value(_file, key=None):
    """
    Returns key-value for searched key in file.
    If key is not specified, returns the whole file.
    Returns string in json format.

    :type  _file: string
    :param _file: path.to.file (dot encoded) where to search the key.

    :type  key: string
    :param key: The key to search.

    :rtype:   json
    :return:  the function returns a json containing the
                key-value searched.
    """
    _file = _file.replace('.', '/', 3)
    if _file != 'config':
        file_name = os.getenv("HOME") + "/.appflow/tenant/" + _file
    else:
        file_name = os.getenv("HOME") + "/.appflow/" + _file + ".yml"

    if not os.path.exists(file_name):
        return 'Error: No such File or Directory'
    if _file.split('/').pop() == 'inventory':
        return 'Error: Invalid Request'
    if os.path.isdir(file_name):
        for subfile in os.listdir(file_name):
            get_value(_file.replace('/', '.', 3) + '.' + subfile)
    else:
        with open(file_name, 'r') as stream:
            conf = yaml.safe_load(stream)
            if key is not None:
                key = key.split('.')
                conf = utils.get_from_dict(conf, key)
            return json.dumps(conf, ensure_ascii=False, indent=4)


def set_value(_file, key, value):
    """
    Returns key-value for searched key in file.
    Searched key will be set with the value specified.
    Data is written to file.
    Returns string in json format.

    :type  _file: string
    :param _file: path.to.file (dot encoded) where to set the key.

    :type  key: string
    :param key: The key to search.

    :type  value: T
    :param value: the value to set.

    :rtype:   json
    :return:  the function returns a json containing the updated file content.
    """
    _file = _file.replace('.', '/', 3)
    key = key.split('.')
    if _file != 'config':
        file_name = os.getenv("HOME") + "/.appflow/tenant/" + _file
    else:
        file_name = os.getenv("HOME") + "/.appflow/" + _file
    if not os.path.exists(file_name):
        return 'Error: No such File or Directory'
    if _file.split('/').pop() == 'inventory':
        return 'Error: Invalid Request'
    with open(file_name, 'r') as stream:
        conf = yaml.safe_load(stream)
        utils.set_in_dict(conf, key, value)
    with open(file_name, 'w') as outfile:
        yaml.dump(conf, outfile, default_flow_style=False,
                  indent=4, default_style='')
    return json.dumps(conf, ensure_ascii=False, indent=4)


def rm_value(_file, key):
    """
    Returns key-value for searched key in file.
    Searched key will be removed.
    Data is written to file.
    Returns string in json format.

    :type  _file: string
    :param _file: path.to.file (dot encoded) where to remove the key.

    :type  key: string
    :param key: The key to search.

    :rtype:   json
    :return:  the function returns a json containing the updated file content.
    """
    _file = _file.replace('.', '/', 3)
    key = key.split('.')
    if _file != 'config':
        file_name = os.getenv("HOME") + "/.appflow/tenant/" + _file
    else:
        file_name = os.getenv("HOME") + "/.appflow/" + _file
    if not os.path.exists(file_name):
        return 'Error: No such File or Directory'
    if _file.split('/').pop() == 'inventory':
        return 'Error: Invalid Request'
    with open(file_name, 'r') as stream:
        conf = yaml.safe_load(stream)
        utils.rm_in_dict(conf, key)
    with open(file_name, 'w') as outfile:
        yaml.dump(conf, outfile, default_flow_style=False,
                  indent=4, default_style='')
    return json.dumps(conf, ensure_ascii=False, indent=4)


def add_value(orig_file, orig_key, value):
    """
    Returns key-value for searched key in file.
    Key will be created with the value specified.
    Data is written to file.
    Returns string in json format.

    :type  _file: string
    :param _file: path.to.file (dot encoded) where to set the key.

    :type  key: string
    :param key: The key to search. (this function will add it if not found.)

    :type  value: T
    :param value: the value to set.

    :rtype:   json
    :return:  the function returns a json containing the updated file content.
    """
    _file = orig_file.replace('.', '/', 3)

    key = orig_key.split('.')
    if _file != 'config':
        file_name = os.getenv("HOME") + "/.appflow/tenant/" + _file
    else:
        file_name = os.getenv("HOME") + "/.appflow/" + _file
    if not os.path.exists(file_name):
        return 'Error: No such File or Directory'
    if _file.split('/').pop() == 'inventory':
        return 'Error: Invalid Request'
    with open(file_name, 'r') as stream:
        conf = yaml.safe_load(stream)
    dictionary = {}
    utils.add_keys(dictionary, key, value)
    my_dicts = [conf, dictionary]

    for _k, _v in dictionary.items():
        if not isinstance(dictionary[_k], dict):
            print(orig_file, orig_key, value)
            return set_value(orig_file, key, value)

    for item in my_dicts:
        for _k, _v in item.items():
            print("***", _k, type(conf[_k]), type(_v))
            if isinstance(conf[_k], dict):
                conf[_k].update(_v)

    with open(file_name, 'w') as outfile:
        yaml.dump(conf, outfile, default_flow_style=False,
                  indent=4, default_style='')
    return json.dumps(conf, ensure_ascii=False, indent=4)
