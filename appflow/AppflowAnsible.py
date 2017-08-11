import os
import appflow.AppflowUtils as utils


def provision(tenant, env, *args):
    print("Provisioning:", tenant, "Environment:", env)

    inventory = utils.getTenantDir(tenant) + env + "/inventory"
    playbook = '/opt/appflow/playbooks/generic.yml'
    passwordFile = utils.getVaultFile(tenant, env)

    # Convert tags=xyz to --tags xyz
    tags = list(args)
    for i, a in enumerate(tags):
        tags[i] = '--' + \
            tags[i].split('=')[0] + ' ' + tags[i].split('=')[1]

    os.system('ansible-playbook -b ' + ' '.join(tags) + ' -i ' +
              inventory + ' ' + playbook + ' --vault-password-file ' + passwordFile)


def tags(tenant, env):
    print("Tags:", tenant, "Environment:", env)
    inventory = utils.getTenantDir(tenant) + env + "/inventory"
    playbook = '/opt/appflow/playbooks/generic.yml'
    passwordFile = utils.getVaultFile(tenant, env)

    os.system('ansible-playbook --list-tags -i ' + inventory +
              ' ' + playbook + ' --vault-password-file ' + passwordFile)


def encrypt(tenant, env):
    print("Encrypting:", tenant, "Environment:", env)

    targetFolder = utils.getTenantEnvDir(tenant, env)
    passwordFile = utils.getVaultFile(tenant, env)
    fileList = utils.getFileList(targetFolder)
    for file in fileList:
        os.system('ansible-vault encrypt ' + file +
                  ' --vault-password-file ' + passwordFile)


def decrypt(tenant, env):
    print("Decrypting:", tenant, "Environment:", env)

    targetFolder = utils.getTenantEnvDir(tenant, env)
    passwordFile = utils.getVaultFile(tenant, env)

    md5StoreFolder = utils.getMD5folder(tenant)
    md5StoreFile = md5StoreFolder + "/appflow-" + env + "-md5"

    utils.safeRemove(md5StoreFile)
    fileList = utils.getFileList(targetFolder)
    for file in fileList:
        os.system('ansible-vault decrypt ' + file +
                  ' --vault-password-file ' + passwordFile)
        utils.writeMD5sum(file, md5StoreFile)
