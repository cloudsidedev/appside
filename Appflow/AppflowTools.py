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

import Appflow.AppflowAnsible as apansible
import Appflow.AppflowUtils as utils
import Appflow.AppflowYaml as apyaml


def initialize(tenant):
    """
    Create default dirs and yaml files for Assh to function properly.
    """
    dirs = ['/.ssh', '/.ssh/assh.d/' + tenant, '/tmp/.ssh/cm']

    # Mkdir -p of needed folders.
    for directory in dirs:
        os.makedirs(os.getenv('HOME') + directory, exist_ok=True)

    # Initialize a default assh.yml config
    conf = {'defaults': {'ControlMaster': 'auto',
                         'ControlPath': '~/tmp/.ssh/cm/%h-%p-%r.sock',
                         'ControlPersist': True,
                         'ForwardAgent': True},
            'includes': ['~/.ssh/assh.d/*/*.yml',
                         '~/.ssh/assh_personal.yml']}
    file_name = os.getenv('HOME') + "/.ssh/assh.yml"
    utils.safe_remove(file_name)
    # Write it to file.
    with open(file_name, 'w') as outfile:
        yaml.dump(conf, outfile, default_flow_style=False,
                  indent=4)

    # Setup the autocompletion now.
    # Generate is using -- --completion function of Fire
    # Save it to ~/.appflow_completion
    # Source if for bash and zsh.
    bash_source_files = [os.getenv('HOME') + "/.bashrc",
                         os.getenv('HOME') + "/.bashrc.local"]
    zsh_source_files = [os.getenv('HOME') + "/.zshrc",
                        os.getenv('HOME') + "/.zshrc.local"]
    os.system(utils.get_appflow_folder(__file__) +
              "/appflow -- --completion > " +
              os.getenv('HOME') + "/.appflow_completion")
    # Add bash completion
    for bash_file in bash_source_files:
        if os.path.exists(bash_file):
            if not utils.check_string_in_file(bash_file, "appflow_completion"):
                os.system('echo "source ' + os.getenv('HOME') +
                          '/.appflow_completion" >> ' + bash_file)
    # Add zsh completion
    for zsh_file in zsh_source_files:
        if os.path.exists(zsh_file):
            if not utils.check_string_in_file(zsh_file, "appflow_completion"):
                os.system("""echo "autoload bashcompinit
                bashcompinit
                source """ + os.getenv('HOME') +
                          '/.appflow_completion" >> ' + zsh_file)


def set_vhosts_hosts(tenant):
    """
    Setup /etc/hosts for tenant.
    Requires root access to write.
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

    # Just add a separation line.
    os.system('echo "\n" | sudo tee -a /etc/hosts')

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


def setup_default_config(tenant_id, tenant, environment):
    """
    Deploy a default config file in ~/.appflow/config.yml
    """
    file_name = os.getenv('HOME') + "/.appflow/config.yml"
    if not os.path.isfile(file_name):
        conf = {'appflow': {'tenant': {'id': tenant_id,
                                       'name': tenant,
                                       'default_env': environment}}}
        utils.safe_remove(file_name)
        with open(file_name, 'w') as outfile:
            yaml.dump(conf, outfile, default_flow_style=False,
                      indent=4)


def setup_ssh(tenant, env):
    """
    Deploy Assh configs for tenant/environment.
    """
    initialize(tenant)
    _dir = utils.get_tenant_dir(tenant)
    target_folder = _dir + env
    dest_folder = os.getenv('HOME') + '/.ssh/assh.d/' + tenant
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
    """
    _dir = utils.get_tenant_dir(tenant)
    target_folder = _dir + env
    if utils.check_string_in_file(target_folder + "/inventory", 'AES256'):
        _pipe = subprocess.PIPE
        subprocess.Popen(
            ['git', '-C', _dir, 'diff-files --name-only -B -R -M', env],
            stdout=_pipe, stderr=_pipe)
        return []
    else:
        md5_store_folder = utils.get_md5_folder(tenant)
        md5_store_file = md5_store_folder + "/appflow-" + env + "-md5"
        md5_store_file_new = md5_store_folder + "/appflow-" + env + "-md5-new"
        utils.safe_remove(md5_store_file_new)
        file_list = utils.get_file_list(target_folder)
        for file in file_list:
            utils.write_md5_sum(file, md5_store_file_new)

        diff = utils.diff_files(md5_store_file, md5_store_file_new)
        return diff


def git_check_in(tenant, env, commit):
    """
    Git push.
    This will affecy only the modified files (see git_status function).
    Commit message can be specified.
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
