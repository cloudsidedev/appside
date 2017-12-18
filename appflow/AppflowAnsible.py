"""
Appflow Ansible utilities.
This contains all the functions needed to perform Ansible actions.
From provision to encryption/decryption and tag listing.
"""
import os
import appflow.AppflowUtils as utils


def provision(tenant, env, *args):
    """
    This will perform the ansible playbook.
    We pass tenant and environment.
    all other tags are parsed from option=xyz to --option xys
    in order to respect ansible's syntax.
    """
    inventory = utils.get_tenant_dir(tenant) + env + "/inventory"
    appflow_folder = os.path.dirname(
        os.path.dirname(os.path.realpath(__file__)))
    playbook = appflow_folder + '/playbooks/generic.yml'
    password_file = utils.get_vault_file(tenant, env)

    # Convert tags=xyz to --tags xyz
    tags_argument = list(args)
    firstrun = False
    for tag in tags_argument:
        if tag.split('=')[1] == '':
            tags_argument.remove(tag)
        elif tag == "firstrun=true":
            tags_argument.remove(tag)
            firstrun = True
    for i, tag in enumerate(tags_argument):
        tags_argument[i] = '--' + \
            tags_argument[i].split('=')[0].replace('_', '-') + \
            ' ' + tags_argument[i].split('=')[1]

    # First run! Let's default to the generic user waiting for users provision
    if firstrun:
        tags_argument.append("-k -u ubuntu")
    os.system('ansible-playbook -b ' + ' '.join(tags_argument) + ' -i ' +
              inventory + ' ' + playbook +
              ' --vault-password-file ' + password_file)


def tags(tenant, env):
    """
    List all available tags for tenant/environment
    """
    inventory = utils.get_tenant_dir(tenant) + env + "/inventory"
    appflow_folder = os.path.dirname(
        os.path.dirname(os.path.realpath(__file__)))
    playbook = appflow_folder + '/playbooks/generic.yml'
    password_file = utils.get_vault_file(tenant, env)

    os.system('ansible-playbook --list-tags -i ' + inventory +
              ' ' + playbook + ' --vault-password-file ' + password_file)


def encrypt(tenant, env):
    """
    Encrypt the tenant/environment data
    """
    target_folder = utils.get_tenant_env_dir(tenant, env)
    password_file = utils.get_vault_file(tenant, env)
    flie_list = utils.get_file_list(target_folder)
    for file in flie_list:
        os.system('ansible-vault encrypt ' + file +
                  ' --vault-password-file ' + password_file)


def decrypt(tenant, env):
    """
    Decrypt the tenant/environment data
    """
    target_folder = utils.get_tenant_env_dir(tenant, env)
    password_file = utils.get_vault_file(tenant, env)

    md5_store_folder = utils.get_md5_folder(tenant)
    md5_store_file = md5_store_folder + "/appflow-" + env + "-md5"

    utils.safe_remove(md5_store_file)
    flie_list = utils.get_file_list(target_folder)
    for file in flie_list:
        os.system('ansible-vault decrypt ' + file +
                  ' --vault-password-file ' + password_file)
        utils.write_md5_sum(file, md5_store_file)