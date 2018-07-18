"""
Appflow Ansible utilities.
This contains all the functions needed to perform Ansible actions.
From provision to encryption/decryption and tag listing.
"""
import os
import subprocess

import lib.appflow_utils as utils

# TODO: add dynamic ouput from terminal


def provision(tenant: str, env: str, limit: str, tags: str,
              skip_tags: str, firstrun: bool, local: bool,
              debug: bool, user: str = None, remote: bool = False):
    """
    This will perform the ansible playbook.
    We pass tenant and environment and all other options as
    --option xys
    in order to respect ansible's syntax.

    :type  tenant: string
    :param tenant: The name of the tenant.

    :type  env: string
    :param env: The name of the tenant.

    :type  limit: string
    :param limit: Comma separated list of hosts to provision.

    :type  tags: string
    :param tags: Comma separated list of tags to exec (default All).

    :type  skip_tags: string
    :param skip_tags: Comma separated list of tags to skip (default None).

    :type  firstrun: bool
    :param firstrun: if it's first run (default False)

    :type  debug: bool
    :param debug: if it's a debug run (default False)

    :type  user: string
    :param user: if it's a firstrun you can choose the default user.

    :rtype:   string
    :return:  the function returns 0 if successful and a number >0 if failed.
    """
    inventory = utils.get_tenant_dir(tenant) + env + "/inventory"
    appflow_folder = utils.get_appflow_folder()
    playbook = appflow_folder + '/playbooks/generic.yml'
    password_file = utils.get_vault_file(tenant, env)

    # Let's be sure the arguments are strings.
    # In case of multiple arguments (comma separated), convert them back to str.
    limit = utils.format_string_argument(limit)
    tags = utils.format_string_argument(tags)
    skip_tags = utils.format_string_argument(skip_tags)

    tags_argument = ['ansible-playbook', '-b']
    # Format arguments for ansible command now.
    if limit is not None:
        tags_argument.append("--limit")
        tags_argument.append(limit)
    if tags is not None:
        tags_argument.append("--tags")
        tags_argument.append(tags)
    if skip_tags is not None:
        tags_argument.append("--skip-tags")
        tags_argument.append(skip_tags)
    # First run! Let's default to the generic user waiting for users provision
    if firstrun:
        if user is None:
            tags_argument.append("-k")
            tags_argument.append("-u")
            tags_argument.append("ubuntu")
        else:
            tags_argument.append("-k")
            tags_argument.append("-u")
            tags_argument.append(user)
    if debug:
        tags_argument.append("-vvv")
    if local:
        tags_argument.append("-c")
        tags_argument.append("local")

    tags_argument.append('-i')
    tags_argument.append(inventory)
    tags_argument.append(playbook)
    tags_argument.append('--vault-password-file')
    tags_argument.append(password_file)
    # If we are remote provisioning, return only the command string
    # The server will take care of executing it.
    if remote:
        return tags_argument
    else:
        process = subprocess.Popen(tags_argument)
        process.wait()


def list_tags(tenant, env):
    """
    List all available tags for tenant/environment

    :type  tenant: string
    :param tenant: The name of the tenant.

    :type  env: string
    :param env: The name of the tenant.

    :rtype:   string
    :return:  the function returns the available tags.
    """
    inventory = utils.get_tenant_dir(tenant) + env + "/inventory"
    appflow_folder = utils.get_appflow_folder()
    playbook = appflow_folder + '/playbooks/generic.yml'
    password_file = utils.get_vault_file(tenant, env)

    return subprocess.Popen('ansible-playbook --list-tags -i ' + inventory +
                            ' ' + playbook + ' --vault-password-file ' +
                            password_file).communicate()


def encrypt(tenant, env):
    """
    Encrypt the tenant/environment data

    :type  tenant: string
    :param tenant: The name of the tenant.

    :type  env: string
    :param env: The name of the tenant.

    :rtype:   string
    :return:  the function returns 0 if successful and a number >0 if failed.
    """
    target_folder = utils.get_tenant_env_dir(tenant, env)
    password_file = utils.get_vault_file(tenant, env)
    flie_list = utils.get_file_list(target_folder)
    # out initialized to zero. Add all out values of the subprocess.
    # A value != 0 indicates a failure
    out = 0
    for file in flie_list:
        out = out + os.system('ansible-vault encrypt ' + file +
                              ' --vault-password-file ' + password_file)
    return out


def decrypt(tenant, env):
    """
    Decrypt the tenant/environment data

    :type  tenant: string
    :param tenant: The name of the tenant.

    :type  env: string
    :param env: The name of the tenant.

    :rtype:   string
    :return:  the function returns 0 if successful and a number >0 if failed.
    """
    target_folder = utils.get_tenant_env_dir(tenant, env)
    password_file = utils.get_vault_file(tenant, env)

    md5_store_folder = utils.get_md5_folder(tenant)
    md5_store_file = md5_store_folder + "/appflow-" + env + "-md5"

    utils.safe_remove(md5_store_file)
    flie_list = utils.get_file_list(target_folder)
    # out initialized to zero. Add all out values of the subprocess.
    # A value != 0 indicates a failure
    out = 0
    for file in flie_list:
        out = out + os.system('ansible-vault decrypt ' + file +
                              ' --vault-password-file ' + password_file)
        utils.write_md5_sum(file, md5_store_file)
    return out
