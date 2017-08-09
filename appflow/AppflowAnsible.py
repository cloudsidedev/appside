import os
import appflow.AppflowUtils as utils


def provision(tenant, env, *args):
    print("Provisioning:", tenant, "Environment:", env)

    inventory = os.getenv("HOME") + "/.appflow/tenant/" + \
        tenant + "/" + env + "/inventory"
    playbook = '/opt/appflow/playbooks/generic.yml'
    passwordFile = os.getenv(
        "HOME") + "/.appflow/vault/" + tenant + "/" + env

    # Convert tags=xyz to --tags xyz
    tags = list(args)
    for i, a in enumerate(tags):
        tags[i] = '--' + \
            tags[i].split('=')[0] + ' ' + tags[i].split('=')[1]

    os.system('ansible-playbook -b ' + ' '.join(tags) + ' -i ' +
              inventory + ' ' + playbook + ' --vault-password-file ' + passwordFile)


def tags(tenant, env, *args):
    print("Tags:", tenant, "Environment:", env)
    inventory = os.getenv("HOME") + "/.appflow/tenant/" + \
        tenant + "/" + env + "/inventory"
    playbook = '/opt/appflow/playbooks/generic.yml'
    passwordFile = os.getenv(
        "HOME") + "/.appflow/vault/" + tenant + "/" + env

    os.system('ansible-playbook --list-tags -i ' + inventory +
              ' ' + playbook + ' --vault-password-file ' + passwordFile)


def encrypt(tenant, env, *args):
    print("Encrypting:", tenant, "Environment:", env)

    targetFolder = os.getenv(
        "HOME") + "/.appflow/tenant/" + tenant + "/" + env
    passwordFile = os.getenv(
        "HOME") + "/.appflow/vault/" + tenant + "/" + env
    fileList = utils.getFileList(targetFolder)
    for file in fileList:
        os.system('ansible-vault encrypt ' + file +
                  ' --vault-password-file ' + passwordFile)


def decrypt(tenant, env, *args):
    print("Decrypting:", tenant, "Environment:", env)

    targetFolder = os.getenv(
        "HOME") + "/.appflow/tenant/" + tenant + "/" + env
    passwordFile = os.getenv(
        "HOME") + "/.appflow/vault/" + tenant + "/" + env
    md5StoreFile = os.getenv(
        "HOME") + "/.appflow/tmp/.appflow-" + os.getenv("USER") + "/" + tenant + "/appflow-" + env + "-md5"

    try:
        os.remove(md5StoreFile)
    except IOError:
        pass
    fileList = utils.getFileList(targetFolder)
    for file in fileList:
        os.system('ansible-vault decrypt ' + file +
                  ' --vault-password-file ' + passwordFile)
        utils.writeMD5sum(file, md5StoreFile)
