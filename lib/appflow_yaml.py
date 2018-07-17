"""
Appflow Yaml utilities.
This contains all the functions needed to manipulate yaml files.
Handy for configs and for tenant setups.
"""
import json
import os

import operator
from functools import reduce
import yaml

import lib.appflow_utils as utils

# List of extensions that must be threated as special
# cases in the obj->path conversion.
EXCLUDED_EXTENSIONS = ('yml', 'yaml')


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
    extension = ''
    file_name = ''

    if _file != 'config':
        if any(_file.split('.')[-1] in extensions
               for extensions in EXCLUDED_EXTENSIONS):
            extension = '.' + _file.split('.')[-1]
            _file = '.'.join(_file.split('.')[:-1])

        file_name = os.getenv("HOME") + "/.appflow/tenant/" + \
            '/'.join(_file.split('.')) + extension
    else:
        file_name = os.getenv("HOME") + "/.appflow/" + _file + ".yml"

    if not os.path.exists(file_name):
        return 'Error: No such File or Directory'
    elif os.path.isdir(file_name):
        return os.listdir(file_name)
    elif _file.split('/').pop() == 'inventory':
        return 'Error: Invalid Request'
    elif utils.check_string_in_file(file_name, 'AES256'):
        return 'Error: Files are Encrypted'
    else:
        with open(file_name, 'r') as stream:
            conf = yaml.safe_load(stream)
            if key is not None:
                key = key.split('.')
                conf = reduce(operator.getitem, key, conf)
            return json.dumps(conf, allow_nan=True, indent=4)


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
    key = key.split('.')
    extension = ''
    file_name = ''

    if _file != 'config':
        if any(_file.split('.')[-1] in extensions
               for extensions in EXCLUDED_EXTENSIONS):
            extension = '.' + _file.split('.')[-1]
            _file = '.'.join(_file.split('.')[:-1])

        file_name = os.getenv("HOME") + "/.appflow/tenant/" + \
            '/'.join(_file.split('.')) + extension
    else:
        file_name = os.getenv("HOME") + "/.appflow/" + _file + ".yml"

    if not os.path.exists(file_name):
        return 'Error: No such File or Directory'
    elif _file.split('/').pop() == 'inventory':
        return 'Error: Invalid Request'
    elif utils.check_string_in_file(file_name, 'AES256'):
        return 'Error: Files are Encrypted'

    with open(file_name, 'r') as stream:
        conf = yaml.safe_load(stream)
        conf = set_in_dict(conf, key, value)
    with open(file_name, 'w') as outfile:
        yaml.safe_dump(conf, outfile, default_flow_style=False,
                       indent=4, default_style='')
    return json.dumps(conf, ensure_ascii=False, indent=4)


def add_value(_file, _key, value):
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
    extension = ''
    file_name = ''

    if _file != 'config':
        if any(_file.split('.')[-1] in extensions
               for extensions in EXCLUDED_EXTENSIONS):
            extension = '.' + _file.split('.')[-1]
            _file = '.'.join(_file.split('.')[:-1])

        file_name = os.getenv("HOME") + "/.appflow/tenant/" + \
            '/'.join(_file.split('.')) + extension
    else:
        file_name = os.getenv("HOME") + "/.appflow/" + _file + ".yml"
    if not os.path.exists(file_name):
        return 'Error: No such File or Directory'
    if _file.split('/').pop() == 'inventory':
        return 'Error: Invalid Request'
    with open(file_name, 'r') as stream:
        conf = yaml.safe_load(stream)

    key = _key.split('.')
    dictionary = {}
    # create nested dict with the value we want to add
    dictionary = add_in_dict(dictionary, key, value)
    # merge the two dicts
    result = merge(conf, dictionary)

    with open(file_name, 'w') as outfile:
        yaml.safe_dump(result, outfile, default_flow_style=False,
                       indent=4, default_style='')
    return json.dumps(result, ensure_ascii=False, indent=4)


def delete_value(_file, key):
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
    key = key.split('.')
    extension = ''
    file_name = ''

    if _file != 'config':
        if any(_file.split('.')[-1] in extensions
               for extensions in EXCLUDED_EXTENSIONS):
            extension = '.' + _file.split('.')[-1]
            _file = '.'.join(_file.split('.')[:-1])

        file_name = os.getenv("HOME") + "/.appflow/tenant/" + \
            '/'.join(_file.split('.')) + extension
    else:
        file_name = os.getenv("HOME") + "/.appflow/" + _file + ".yml"
    if not os.path.exists(file_name):
        return 'Error: No such File or Directory'
    if _file.split('/').pop() == 'inventory':
        return 'Error: Invalid Request'
    with open(file_name, 'r') as stream:
        conf = yaml.safe_load(stream)
        rm_in_dict(conf, key)

    with open(file_name, 'w') as outfile:
        yaml.safe_dump(conf, outfile, default_flow_style=False,
                       indent=4, default_style='')
    return json.dumps(conf, ensure_ascii=False, indent=4)


def set_in_dict(data_dict, key, value):
    """
    Set key-value in dictionary

    :type  data_dict: dict
    :param data_dict: The dictionary where to search the key.

    :type  key: string
    :param key: The key to search.

    :type  value: string
    :param value: The value to set.

    :rtype:   dict
    :return:  the function returns the modified data dictionary.
    """
    # This will get called for every path/value in the structure
    def transformer(path, base_value):
        """
        Set the new value for the corresponding key.
        """
        if path == key:
            return value
        else:
            return base_value

    return walk_dict(data_dict, callback=transformer)


def rm_in_dict(data_dict, key):
    """
    Remove keys from dictionary

    :type  data_dict: dict
    :param data_dict: The dictionary where to search the key.

    :type  key: string
    :param key: The key to search.

    :rtype:   dict
    :return:  the function returns the dictionary with the deleted the
                key searched.
    """
    if len(key) > 1:
        empty = rm_in_dict(data_dict[key[0]], key[1:])
        if empty:
            del data_dict[key[0]]
    else:
        del data_dict[key[0]]
    return len(data_dict) == 0


def add_in_dict(data_dict, key, value=None):
    """
    Add keys to dictionary (set also value if specified)

    :type  data_dict: dict
    :param data_dict: The dictionary where to search the key.

    :type  key: string
    :param key: The key to search.

    :type  value: string
    :param value: The value to set. (default None)

    :rtype:   dict
    :return:  the function returns the modified data dictionary.
    """
    if len(key) > 1:
        data_dict[key[0]] = {}
        data_dict[key[0]] = data_dict.get(key[0], {})
        add_in_dict(data_dict[key[0]], key[1:], value)
    else:
        data_dict[key[0]] = value
    return data_dict


def merge(source, target, path=None):
    """
    Merges dictionary b into dictionary a

    :type  source: dict
    :param source: The base dictionary where to merge the second one.

    :type  target: dict
    :param target: The dictionary to merge.

    :type  path: str
    :param path: The path to follow.

    :rtype:   dict
    :return:  the function returns the modified data dictionary.
    """
    if path is None:
        path = []
    for key in target:
        if key in source:
            if isinstance(source[key], dict) and isinstance(target[key], dict):
                merge(source[key], target[key], path + [str(key)])
            elif source[key] == target[key]:
                pass  # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            source[key] = target[key]
    return source


def walk_dict(obj, path=None, callback=None):
    """
    Walk dictionary and apply function or return value to corresponding key.
    """
    if path is None:
        path = []

    if isinstance(obj, dict):
        value = {k: walk_dict(v, path + [k], callback)
                 for k, v in obj.items()}
    elif isinstance(obj, list):
        value = [walk_dict(elem, path + [[]], callback)
                 for elem in obj]
    else:
        value = obj
    # if a callback is provided, call it to get the new value
    if callback is None:
        return value
    else:
        return callback(path, value)
