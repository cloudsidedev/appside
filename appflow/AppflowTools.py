import os
import subprocess
import appflow.AppflowUtils as utils
import appflow.AppflowAnsible as apansible
import yaml
import shutil

def initialize(tenant, env):
    dirs = ['/.ssh', '/.ssh/assh.d/' + tenant, '/tmp/.ssh/cm']

    for d in dirs:
        os.makedirs(os.getenv('HOME') + d, exist_ok=True)

    conf = {'defaults': {'ControlMaster': 'auto', 'ControlPath': '~/tmp/.ssh/cm/%h-%p-%r.sock', 'ControlPersist': True,
                         'ForwardAgent': True}, 'includes': ['~/.ssh/assh.d/*/*.yml', '~/.ssh/assh_personal.yml']}
    fileName = os.getenv('HOME') + "/.ssh/assh.yml"
    utils.safeRemove(fileName)
    with open(fileName, 'w') as outfile:
        yaml.dump(conf, outfile, default_flow_style=False,
                  indent=4)


def setupSsh(tenant, env):
    initialize(tenant, env)
    dir = utils.getTenantDir(tenant)
    targetFolder = dir + env
    destFolder = os.getenv('HOME') + '/.ssh/assh.d/' + tenant
    destFile = destFolder + '/' + env + '.yml'

    Enc = False
    if(utils.checkStringInFile(targetFolder + "/inventory", 'AES256')):
        apansible.decrypt(tenant, env)
        Enc = True

    shutil.copy2(targetFolder + "/assh.yml", destFile)

    if (Enc == True):
        gitReset(tenant, env)


def gitReset(tenant, env):
    dir = utils.getTenantDir(tenant)
    PIPE = subprocess.PIPE
    process = subprocess.Popen(
        ['git', '-C', dir, 'clean -xdf', env], stdout=PIPE, stderr=PIPE)
    process = subprocess.Popen(
        ['git', '-C', dir, 'checkout', env], stdout=PIPE, stderr=PIPE)
    process = subprocess.Popen(
        ['git', '-C', dir, 'reset --hard'], stdout=PIPE, stderr=PIPE)
    md5StoreFolder = utils.getMD5folder(tenant)
    md5StoreFile = md5StoreFolder + "/appflow-" + env + "-md5"
    utils.safeRemove(md5StoreFile)
    utils.safeRemove(md5StoreFile + "-new")


def gitStatus(tenant, env):
    dir = utils.getTenantDir(tenant)
    targetFolder = dir + env
    if(utils.checkStringInFile(targetFolder + "/inventory", 'AES256')):
        print('Files Already Encrypted')
        PIPE = subprocess.PIPE
        process = subprocess.Popen(
            ['git', '-C', dir, 'diff-files --name-only -B -R -M', env], stdout=PIPE, stderr=PIPE)
        return False
    else:
        md5StoreFolder = utils.getMD5folder(tenant)
        md5StoreFile = md5StoreFolder + "/appflow-" + env + "-md5"
        md5StoreFileNew = md5StoreFolder + "/appflow-" + env + "-md5-new"
        utils.safeRemove(md5StoreFileNew)
        fileList = utils.getFileList(targetFolder)
        for file in fileList:
            utils.writeMD5sum(file, md5StoreFileNew)

        diff = utils.diffFiles(md5StoreFile, md5StoreFileNew)
        print('Changed files:')
        print('\n'.join(diff))
        return diff


def gitCheckin(tenant, env):
    dir = utils.getTenantDir(tenant)
    folder = utils.getTenantEnvDir(tenant, env)
    file_list = utils.getFileList(folder)
    Encrypted = True
    for f in file_list:
        if (utils.checkStringInFile(f, 'AES256') == False):
            Encrypted = False
    diff = gitStatus(tenant, env)
    if (Encrypted == False):
        apansible.encrypt(tenant, env)

    PIPE = subprocess.PIPE
    for f in diff:
        process = subprocess.Popen(
            ['git', '-C', dir, 'add', f], stdout=PIPE, stderr=PIPE)
    commit = "Auto Commit"
    process = subprocess.Popen(
        ['git', '-C', dir, 'commit',  '-m', commit], stdout=PIPE, stderr=PIPE)
    process = subprocess.Popen(
        ['git', '-C', dir, 'push'], stdout=PIPE, stderr=PIPE)
    gitReset(tenant, env)


def gitCheckOut(tenant, env):
    query = utils.query_yes_no(
        'Warning, this process will overwrite any un-pushed work, continue?', 'no')
    if(query == True):
        gitReset(tenant, env)
        dir = utils.getTenantDir(tenant)
        PIPE = subprocess.PIPE
        process = subprocess.Popen(
            ['git', '-C', dir, 'pull'], stdout=PIPE, stderr=PIPE)
