import operator
import os
import hashlib

def getFileList(dir):
    fileList = list()
    for root, subdirs, files in os.walk(dir):
        for file in files:
            fileList.append(os.path.join(root, file))
    return fileList


def getMD5sum(file_name):
    with open(file_name, 'rb') as file_to_check:
        data = file_to_check.read()
        return hashlib.md5(data).hexdigest() + '\t' + file_name + '\n'


def writeMD5sum(file_name, md5StoreFile):
    os.makedirs(os.path.dirname(md5StoreFile), exist_ok=True)
    line = getMD5sum(file_name)
    if (os.path.exists(md5StoreFile)):
        open(md5StoreFile, 'a').write(line)
    else:
        open(md5StoreFile, 'w+').write(line)


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

def checkStringInFile(file_name, string):
    with open(file_name) as f:
        found = False
        for line in f:
            if string in line: # Key line: check if `w` is in the line.
                found = True
        return found

def diffFiles(file1, file2):
    result = list()
    with open(file1) as f1:
        with open(file2) as f2:
            linesFile1 = f1.readlines()
            linesFile2= f2.readlines()
            diff = [ x for x in linesFile1 if x not in linesFile2 ]
            for x in diff:
                fileName = x.split('\t')[1].replace('\n','')
                result.append(fileName)
            return result