import os
import subprocess
import appflow.AppflowUtils as utils
import difflib

# ssh/assh (deploy assh.yml and do the rest)
# checkin
# checkout


def gitReset(tenant, env):
    dir = os.getenv("HOME") + "/.appflow/tenant/" + \
        tenant + "/"
    PIPE = subprocess.PIPE
    process = subprocess.Popen(
        ['git', '-C', dir, 'clean -xdf', env], stdout=PIPE, stderr=PIPE)
    process.communicate()
    process = subprocess.Popen(
        ['git', '-C', dir, 'checkout', env], stdout=PIPE, stderr=PIPE)
    process.communicate()

    md5StoreFile = os.getenv("HOME") + "/.appflow/tmp/.appflow-" + \
        os.getenv("USER") + "/" + tenant + "/appflow-" + env + "-md5"
    try:
        os.remove(md5StoreFile)
    except IOError:
        pass
    try:
        os.remove(md5StoreFile + "-new")
    except IOError:
        pass


def gitStatus(tenant, env):
    dir = os.getenv("HOME") + "/.appflow/tenant/" + \
        tenant + "/"
    targetFolder = dir + env
    if(utils.checkStringInFile(targetFolder + "/inventory", 'AES256')):
        print ('Files Already Encrypted')
        PIPE = subprocess.PIPE
        process = subprocess.Popen(
            ['git', '-C', dir, 'diff-files --name-only -B -R -M', env], stdout=PIPE, stderr=PIPE)
        process.communicate()
        return False
    else:
        md5StoreFolder = os.getenv(
            "HOME") + "/.appflow/tmp/.appflow-" + os.getenv("USER") + "/" + tenant
        md5StoreFile = md5StoreFolder + "/appflow-" + env + "-md5"
        md5StoreFileNew = md5StoreFolder + "/appflow-" + env + "-md5-new"
        try:
            os.remove(md5StoreFileNew)
        except IOError:
            pass
        fileList = utils.getFileList(targetFolder)
        for file in fileList:
            utils.writeMD5sum(file, md5StoreFileNew)
        
        diff = utils.diffFiles(md5StoreFile, md5StoreFileNew)
        print('Changed files:')
        print('\n'.join(diff))