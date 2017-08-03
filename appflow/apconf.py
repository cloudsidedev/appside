#!/usr/bin/python3

import json
import operator
import os
from functools import reduce

import fire
import yaml

# To exec script from shell
# os.system('echo ttsstest ; ./test.sh ' + ' '.join(args))


def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)


def setInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value


def rmInDict(branch, keys):
    if len(keys) > 1:
        empty = rmInDict(branch[keys[0]], keys[1:])
        if empty:
            del branch[keys[0]]
    else:
        del branch[keys[0]]
    return len(branch) == 0


def add_keys(d, l, c=None):
    if len(l) > 1:
        d[l[0]] = _d = {}
        d[l[0]] = d.get(l[0], {})
        add_keys(d[l[0]], l[1:], c)
    else:
        d[l[0]] = c


class AppFlow(object):
    def get(self, file, key='none'):
        file = file.replace('.', '/', 3)
        if (file != 'config'):
            fileName = os.getenv("HOME") + "/.appflow/tenant/" + file
        else:
            fileName = os.getenv("HOME") + "/.appflow/" + file
        ##
        print(fileName)
        if not os.path.exists(fileName):
            print('No such File or Directory')
            return
        if file.split('/').pop() == 'inventory':
            return
        if (os.path.isdir(fileName)):
            for subfile in os.listdir(fileName):
                self.get(file.replace('/', '.', 3) + '.' + subfile)
        else:
            with open(fileName, 'r') as stream:
                conf = yaml.safe_load(stream)
                if (key != 'none'):
                    key = key.split('.')
                    return (json.dumps(getFromDict(conf, key),
                                     ensure_ascii=False, indent=4))
                else:
                    return (json.dumps(conf, ensure_ascii=False, indent=4))

    def set(self, file, key, value):
        file = file.replace('.', '/', 3)
        key = key.split('.')
        if (file != 'config'):
            fileName = os.getenv("HOME") + "/.appflow/tenant/" + file
        else:
            fileName = os.getenv("HOME") + "/.appflow/" + file
        with open(fileName, 'r') as stream:
            conf = yaml.safe_load(stream)
            setInDict(conf, key, value)
        with open(fileName, 'w') as outfile:
            yaml.dump(conf, outfile, default_flow_style=False,
                      indent=4, default_style='')
        print(json.dumps(conf, ensure_ascii=False, indent=4))

    def rm(self, file, key):
        file = file.replace('.', '/', 3)
        key = key.split('.')
        if (file != 'config'):
            fileName = os.getenv("HOME") + "/.appflow/tenant/" + file
        else:
            fileName = os.getenv("HOME") + "/.appflow/" + file
        with open(fileName, 'r') as stream:
            conf = yaml.safe_load(stream)
            rmInDict(conf, key)
        with open(fileName, 'w') as outfile:
            yaml.dump(conf, outfile, default_flow_style=False,
                      indent=4, default_style='')
        print(json.dumps(conf, ensure_ascii=False, indent=4))

    def add(self, file, key, value):
        file = file.replace('.', '/', 3)
        key = key.split('.')
        if (file != 'config'):
            fileName = os.getenv("HOME") + "/.appflow/tenant/" + file
        else:
            fileName = os.getenv("HOME") + "/.appflow/" + file
        with open(fileName, 'r') as stream:
            conf = yaml.safe_load(stream)
        d = {}
        add_keys(d, key, value)
        myDicts = [conf, d]
        for a in myDicts:
            for k, v in a.items():
                conf[k].update(v)
        with open(fileName, 'w') as outfile:
            yaml.dump(conf, outfile, default_flow_style=False,
                      indent=4, default_style='')
        print((json.dumps(conf, ensure_ascii=False, indent=4)))


if __name__ == '__main__':
    fire.Fire(AppFlow)
