import os
import shutil
import subprocess

import yaml

import appflow.AppflowAnsible as apansible
import appflow.AppflowUtils as utils


def initialize(tenant):
    dirs = ['/.ssh', '/.ssh/assh.d/' + tenant, '/tmp/.ssh/cm']

    for directory in dirs:
        os.makedirs(os.getenv('HOME') + directory, exist_ok=True)

    conf = {'defaults': {'ControlMaster': 'auto', 'ControlPath': '~/tmp/.ssh/cm/%h-%p-%r.sock', 'ControlPersist': True,
                         'ForwardAgent': True}, 'includes': ['~/.ssh/assh.d/*/*.yml', '~/.ssh/assh_personal.yml']}
    file_name = os.getenv('HOME') + "/.ssh/assh.yml"
    utils.safe_remove(file_name)
    with open(file_name, 'w') as outfile:
        yaml.dump(conf, outfile, default_flow_style=False,
                  indent=4)


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
        return False
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


def git_check_in(tenant, env):
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
        subprocess.Popen(
            ['git', '-C', _dir, 'add', file], stdout=_pipe, stderr=_pipe)
    commit = "Auto Commit"
    subprocess.Popen(
        ['git', '-C', _dir, 'commit', '-m', commit], stdout=_pipe, stderr=_pipe)
    subprocess.Popen(
        ['git', '-C', _dir, 'push'], stdout=_pipe, stderr=_pipe)
    git_reset(tenant, env)


def git_check_out(tenant, env):
    query = utils.query_yes_no(
        'Warning, this process will overwrite any un-pushed work, continue?', 'no')
    if query is True:
        git_reset(tenant, env)
        _dir = utils.get_tenant_dir(tenant)
        _pipe = subprocess.PIPE
        subprocess.Popen(
            ['git', '-C', _dir, 'pull'], stdout=_pipe, stderr=_pipe)
