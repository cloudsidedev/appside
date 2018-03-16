"""
Appflow Ansible utilities.
This contains all the functions needed to perform Ansible actions.
From provision to encryption/decryption and tag listing.
"""
import os

import lib.appflow_utils as utils


def provision(tenant: str, env: str, limit: str, tags: str,
              skip_tags: str, firstrun: bool, local: bool, debug: bool):
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

    :rtype:   None
    :return:  the function prints to screen the ansible output of the
                execution.
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

    tags_argument = []
    # Format arguments for ansible command now.
    if limit is not None:
        tags_argument.append("--limit " + limit)
    if tags is not None:
        tags_argument.append("--tags " + tags)
    if skip_tags is not None:
        tags_argument.append("--skip-tags " + skip_tags)
    # First run! Let's default to the generic user waiting for users provision
    if firstrun:
        tags_argument.append("-k -u ubuntu")
    if debug:
        tags_argument.append("-vvv")
    if local:
        tags_argument.append("-c local")
    os.system('ansible-playbook -b ' + ' '.join(tags_argument) + ' -i ' +
              inventory + ' ' + playbook +
              ' --vault-password-file ' + password_file)


def list_tags(tenant, env):
    """
    List all available tags for tenant/environment

    :type  tenant: string
    :param tenant: The name of the tenant.

    :type  env: string
    :param env: The name of the tenant.

    :rtype:   None
    :return:  the function prints to screen the available tags.
    """
    inventory = utils.get_tenant_dir(tenant) + env + "/inventory"
    appflow_folder = utils.get_appflow_folder()
    playbook = appflow_folder + '/playbooks/generic.yml'
    password_file = utils.get_vault_file(tenant, env)

    os.system('ansible-playbook --list-tags -i ' + inventory +
              ' ' + playbook + ' --vault-password-file ' + password_file)


def encrypt(tenant, env):
    """
    Encrypt the tenant/environment data

    :type  tenant: string
    :param tenant: The name of the tenant.

    :type  env: string
    :param env: The name of the tenant.

    :rtype:   None
    :return:  the function prints to screen the ansible output of the
                execution.
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

    :type  tenant: string
    :param tenant: The name of the tenant.

    :type  env: string
    :param env: The name of the tenant.

    :rtype:   None
    :return:  the function prints to screen the ansible output of the
                execution.
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
