import json
import os
import shutil
import subprocess
from builtins import any as b_any

import yaml

import appflow.AppflowAnsible as apansible
import appflow.AppflowUtils as utils
import appflow.AppflowYaml as apyaml


def initialize(tenant):
    dirs = ['/.ssh', '/.ssh/assh.d/' + tenant, '/tmp/.ssh/cm']

    for directory in dirs:
        os.makedirs(os.getenv('HOME') + directory, exist_ok=True)

    conf = {'defaults': {'ControlMaster': 'auto',
                         'ControlPath': '~/tmp/.ssh/cm/%h-%p-%r.sock',
                         'ControlPersist': True,
                         'ForwardAgent': True
                         },
            'includes': ['~/.ssh/assh.d/*/*.yml',
                         '~/.ssh/assh_personal.yml']}
    file_name = os.getenv('HOME') + "/.ssh/assh.yml"
    utils.safe_remove(file_name)
    with open(file_name, 'w') as outfile:
        yaml.dump(conf, outfile, default_flow_style=False,
                  indent=4)


def set_vhosts_hosts(tenant):
    vhosts = apyaml.get_value(tenant + ".development.group_vars.all",
                              "conf_vhosts_common")
    vhosts = json.loads(vhosts)
    ips = apyaml.get_value(tenant + ".development.group_vars.all",
                           "conf_hosts")
    ips = json.loads(ips)

    file = open("/etc/hosts", 'r')
    current_hosts = [line.strip() for line in file]

    new_hosts = []
    for host in vhosts:
        if vhosts.get(host)["state"] == "enabled":
            server_alias = vhosts.get(host)["servername"]
            for alias in vhosts.get(host)["serveralias"]:
                server_alias = server_alias + " " + alias
        for ip in ips:
            # Assemble the line IP + servername + aliases
            ip = ip.split()[0] + " " + server_alias
            # Check if this line is already present
            if ip not in "".join(current_hosts):
                # if not present add it!
                new_hosts.append(ip)
    for host in new_hosts:
        # let's append to the file only the lines we need
        # we will need sudo in order to write in /etc/hosts
        os.system('echo ' + host + ' | sudo tee -a /etc/hosts')


def setup_ssh(tenant, env):
    initialize(tenant)
    _dir = utils.get_tenant_dir(tenant)
    target_folder = _dir + env
    dest_folder = os.getenv('HOME') + '/.ssh/assh.d/' + tenant
    dest_file = dest_folder + '/' + env + '.yml'

    is_decrypted = False
    if utils.check_string_in_file(target_folder + "/inventory", 'AES256'):
        apansible.decrypt(tenant, env)
        is_decrypted = True

    shutil.copy2(target_folder + "/assh.yml", dest_file)

    if is_decrypted is True:
        git_reset(tenant, env)


def git_reset(tenant, env):
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
    _dir = utils.get_tenant_dir(tenant)
    folder = utils.get_tenant_env_dir(tenant, env)
    file_list = utils.get_file_list(folder)
    is_encrypted = True
    for file in file_list:
        if utils.check_string_in_file(file, 'AES256') is False:
            is_encrypted = False
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
