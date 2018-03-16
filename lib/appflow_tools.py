"""
Appflow Tools.
This contains all the functions needed to perform actions connected to
initialization, config deployment and git versioning.
"""
import json
import os
import shutil
import subprocess

import yaml

import lib.appflow_ansible as apansible
import lib.appflow_utils as utils
import lib.appflow_yaml as apyaml


def initialize(tenant, env):
    """
    Create default dirs, clone playbooks and yaml files for Assh to function properly.

    :type  tenant: string
    :param tenant: The name of the tenant. (ex: mrrobot)

    :type  env: string
    :param env: The name of the tenant.


    :rtype:   None
    :return:  This function doesn't have a return statement.
    """

    # We use this to distinguish if tenant+env is specified
    # if not, we should ask them!
    if tenant is None or env is None:
        tenant = input("What's the tenant name? ")
        choice = int(input("""
        Choose your default environment
        1) Development
        2) Staging
        3) Production
        """))
        if choice < 1 or choice > 3:
            print('Invalid option')
            return

        environmens = ['development', 'staging', 'production']
        env = environmens[choice - 1]

    dirs = ['/.ssh', '/.ssh/assh.d/' + tenant, '/tmp/.ssh/cm', '/.appflow',
            '/.appflow/tenant', '/.appflow/vault']

    # Mkdir -p of needed folders.
    for directory in dirs:
        os.makedirs(os.getenv('HOME') + directory, exist_ok=True)

    # Setup default configs
    setup_default_config(tenant, env)

    # Initialize a default assh.yml config
    conf = {'defaults': {'ControlMaster': 'auto',
                         'ControlPath': '~/tmp/.ssh/cm/%h-%p-%r.sock',
                         'ControlPersist': True,
                         'ForwardAgent': True},
            'includes': ['~/.ssh/assh.d/*/*.yml',
                         '~/.ssh/assh_personal.yml']}
    file_name = os.getenv('HOME') + "/.ssh/assh.yml"
    # Write it to file.
    with open(file_name, 'w') as outfile:
        yaml.dump(conf, outfile, default_flow_style=False,
                  indent=4)

    # Clone appflow-playbooks.
    subprocess.Popen(['git', '-C', os.getenv('HOME') + '/.appflow',
                      'clone',
                      'https://github.com/ttssdev/appflow-playbooks',
                      'playbooks'],
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Done")
    return


def setup_default_config(tenant, env):
    """
    Deploy a default config file in ~/.appflow/config.yml

    :type  tenant: string
    :param tenant: The name of the tenant. (ex: mrrobot)

    :type  env: string
    :param env: The name of the tenant.

    :rtype:   None
    :return:  the function prints to screen the ansible output of the execution.
    """
    file_name = os.getenv('HOME') + "/.appflow/config.yml"
    utils.safe_remove(file_name)
    conf = {'appflow': {'tenant': {'id': 'appflow-' + tenant,
                                   'name': tenant,
                                   'default_env': env}}}
    with open(file_name, 'w') as outfile:
        yaml.dump(conf, outfile, default_flow_style=False,
                  indent=4)


def set_vhosts_hosts(tenant):
    """
    Setup /etc/hosts for tenant.
    Requires root access to write.

    :type  tenant: string
    :param tenant: The name of the tenant.

    :rtype:   None
    :return:  the function doesn't have a return statement.
    """
    _dir = utils.get_tenant_dir(tenant)
    target_folder = _dir + "development"
    is_decrypted = False
    # Files are encrypted. Decrypt and save status to re-encrypt later.
    if utils.check_string_in_file(target_folder + "/inventory", 'AES256'):
        apansible.decrypt(tenant, "development")
        is_decrypted = True
    vhosts = apyaml.get_value(tenant + ".development.group_vars.all",
                              "conf_vhosts_common")
    vhosts = json.loads(vhosts)
    ip_list = apyaml.get_value(tenant + ".development.group_vars.all",
                               "conf_hosts")
    ip_list = json.loads(ip_list)

    # Open /etc/hosts file.
    # Put it in string list.
    file = open("/etc/hosts", 'r')
    current_hosts = [line.strip() for line in file]

    new_hosts = []
    for _ip in ip_list:
        # Check if this line is already present
        if _ip not in "".join(current_hosts):
            # if not present add it!
            new_hosts.append(_ip)
    for host in vhosts:
        if vhosts.get(host)["state"] == "enabled":
            server_alias = vhosts.get(host)["servername"]
            for alias in vhosts.get(host)["serveralias"]:
                server_alias = server_alias + " " + alias
        for _ip in ip_list:
            # Assemble the line IP + servername + aliases
            _ip = _ip.split()[0] + " " + server_alias
            # Check if this line is already present
            if _ip not in "".join(current_hosts):
                # if not present add it!
                new_hosts.append(_ip)
    for host in new_hosts:
        # let's append to the file only the lines we need
        # we will need sudo in order to write in /etc/hosts
        os.system('echo ' + host + ' | sudo tee -a /etc/hosts')
    if is_decrypted is True:
        git_reset(tenant, "development")


def setup_ssh(tenant, env):
    """
    Deploy Assh configs for tenant/environment.

    :type  tenant: string
    :param tenant: The name of the tenant.

    :type  env: string
    :param env: The name of the tenant.

    :rtype:   None
    :return:  the function doesn't have a return statement.
    """
    _dir = utils.get_tenant_dir(tenant)
    target_folder = _dir + env
    dest_folder = os.getenv('HOME') + '/.ssh/assh.d/' + tenant
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder, exist_ok=True)
    dest_file = dest_folder + '/' + env + '.yml'

    is_decrypted = False
    # Files are encrypted. Decrypt and save status to re-encrypt later.
    if utils.check_string_in_file(target_folder + "/inventory", 'AES256'):
        apansible.decrypt(tenant, env)
        is_decrypted = True

    shutil.copy2(target_folder + "/assh.yml", dest_file)
    print(dest_folder + '/' + env + '.yml', "deployed")
    if is_decrypted is True:
        git_reset(tenant, env)


def git_reset(tenant, env):
    """
    Perform git reset in the specified tenant/environment folder.
    After this, updates the md5 file to reflect the new status.

    :type  tenant: string
    :param tenant: The name of the tenant.

    :type  env: string
    :param env: The name of the tenant.

    :rtype:   None
    :return:  the function doesn't have a return statement.
    """
    _dir = utils.get_tenant_dir(tenant)
    _pipe = subprocess.PIPE
    subprocess.Popen(
        ['git', '-C', _dir, 'clean -xdf', env], stdout=_pipe, stderr=_pipe)
    subprocess.Popen(
        ['git', '-C', _dir, 'checkout', env], stdout=_pipe, stderr=_pipe)
    subprocess.Popen(
        ['git', '-C', _dir, 'reset --hard'], stdout=_pipe, stderr=_pipe)
    md5_store_folder = utils.get_md5_folder(tenant)
    md5_store_file = md5_store_folder + "/appflow-" + env + "-md5"
    utils.safe_remove(md5_store_file)
    utils.safe_remove(md5_store_file + "-new")


def git_status(tenant, env):
    """
    Return a status of modified files in the tenant/environment folder.
    this is tracked separately from git, because encryption/decryption of files
    will always override the git status method.

    :type  tenant: string
    :param tenant: The name of the tenant.

    :type  env: string
    :param env: The name of the tenant.

    :rtype:   list
    :return:  the function returns a list containing the different lines between
                the 2 md5 files.
    """
    _dir = utils.get_tenant_dir(tenant)
    target_folder = _dir + env
    if not utils.check_string_in_file(target_folder + "/inventory", 'AES256'):
        md5_store_folder = utils.get_md5_folder(tenant)
        md5_store_file = md5_store_folder + "/appflow-" + env + "-md5"
        md5_store_file_new = md5_store_folder + "/appflow-" + env + "-md5-new"
        utils.safe_remove(md5_store_file_new)
        file_list = utils.get_file_list(target_folder)
        for file in file_list:
            utils.write_md5_sum(file, md5_store_file_new)

        diff = utils.diff_files(md5_store_file, md5_store_file_new)
        return diff

    # Files are encrypted, simply do a git diff
    _pipe = subprocess.PIPE
    out = subprocess.Popen(['git', '-C', _dir,
                            'diff-files', '--name-only', '-B', '-R', '-M', env],
                           stdout=_pipe, stderr=_pipe)
    result = []
    for line in iter(out.stdout):
        result.append(line.decode('utf-8'))
    return result


def git_check_in(tenant, env, commit):
    """
    Git push.
    This will affecy only the modified files (see git_status function).
    Commit message can be specified.

    :type  tenant: string
    :param tenant: The name of the tenant.

    :type  env: string
    :param env: The name of the tenant.

    :type  commit: string
    :param commit: The commit message to use when committing.

    :rtype:   None
    :return:  the function doesn't have a return statement.

    """
    _dir = utils.get_tenant_dir(tenant)
    folder = utils.get_tenant_env_dir(tenant, env)
    file_list = utils.get_file_list(folder)
    is_encrypted = False
    for file in file_list:
        if utils.check_string_in_file(file, 'AES256'):
            is_encrypted = True
    diff = git_status(tenant, env)
    if is_encrypted is False:
        apansible.encrypt(tenant, env)

    _pipe = subprocess.PIPE
    for file in diff:
        out = subprocess.Popen(
            ['git', '-C', _dir, 'add', file], stdout=_pipe, stderr=_pipe)
        for line in iter(out.stdout.readline, b''):
            print(line.decode('utf-8'))
    out = subprocess.Popen(
        ['git', '-C', _dir, 'commit', '-m', commit], stdout=_pipe, stderr=_pipe)
    for line in iter(out.stdout.readline, b''):
        print(line.decode('utf-8'))
    out = subprocess.Popen(
        ['git', '-C', _dir, 'push'], stdout=_pipe, stderr=_pipe)
    for line in iter(out.stdout.readline, b''):
        print(line.decode('utf-8'))
    git_reset(tenant, env)


def git_check_out(tenant, env):
    """
    Git pull of the specified tenant/environment folder.
    un-pushed work can be overwritten by this, so ask for confirmation.

    :type  tenant: string
    :param tenant: The name of the tenant.

    :type  env: string
    :param env: The name of the tenant.

    :rtype:   None
    :return:  the function doesn't have a return statement.
    """
    query = utils.yes_no(
        'WARNING, this will overwrite any un-pushed work, continue?', 'no')
    if query is True:
        git_reset(tenant, env)
        _dir = utils.get_tenant_dir(tenant)
        _pipe = subprocess.PIPE
        out = subprocess.Popen(
            ['git', '-C', _dir, 'pull'], stdout=_pipe, stderr=_pipe)
        for line in iter(out.stdout.readline, b''):
            print(line.decode('utf-8'))


def git_update_playbooks(branch):
    """
    Git pull the latest version of the playbooks.
    You can specify which branch you want to use

    :type  branch: string
    :param branch: The name of the branch
    """
    _dir = utils.get_appflow_folder() + "/playbooks"
    _pipe = subprocess.PIPE
    out = subprocess.Popen(
        ['git', '-C', _dir, 'checkout', branch], stdout=_pipe, stderr=_pipe)
    for line in iter(out.stdout.readline, b''):
        print(line.decode('utf-8'))
    out = subprocess.Popen(
        ['git', '-C', _dir, 'pull'], stdout=_pipe, stderr=_pipe)
    for line in iter(out.stdout.readline, b''):
        print(line.decode('utf-8'))
