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
    file_name = os.getenv('HOME') + "/.ssh/assh.yml"
    utils.safe_remove(file_name)
    with open(file_name, 'w') as outfile:
        yaml.dump(conf, outfile, default_flow_style=False,
                  indent=4)


def setup_ssh(tenant, env):
    initialize(tenant, env)
    dir = utils.get_tenant_dir(tenant)
    target_folder = dir + env
    dest_folder = os.getenv('HOME') + '/.ssh/assh.d/' + tenant
    dest_file = dest_folder + '/' + env + '.yml'

    Enc = False
    if(utils.check_string_in_file(target_folder + "/inventory", 'AES256')):
        apansible.decrypt(tenant, env)
        Enc = True

    shutil.copy2(target_folder + "/assh.yml", dest_file)

    if (Enc == True):
        git_reset(tenant, env)


def git_reset(tenant, env):
    dir = utils.get_tenant_dir(tenant)
    PIPE = subprocess.PIPE
    process = subprocess.Popen(
        ['git', '-C', dir, 'clean -xdf', env], stdout=PIPE, stderr=PIPE)
    process = subprocess.Popen(
        ['git', '-C', dir, 'checkout', env], stdout=PIPE, stderr=PIPE)
    process = subprocess.Popen(
        ['git', '-C', dir, 'reset --hard'], stdout=PIPE, stderr=PIPE)
    md5_store_folder = utils.get_md5_folder(tenant)
    md5_store_file = md5_store_folder + "/appflow-" + env + "-md5"
    utils.safe_remove(md5_store_file)
    utils.safe_remove(md5_store_file + "-new")


def git_status(tenant, env):
    dir = utils.get_tenant_dir(tenant)
    target_folder = dir + env
    if(utils.check_string_in_file(target_folder + "/inventory", 'AES256')):
        PIPE = subprocess.PIPE
        process = subprocess.Popen(
            ['git', '-C', dir, 'diff-files --name-only -B -R -M', env], stdout=PIPE, stderr=PIPE)
        return False
    else:
        md5_store_folder = utils.get_md5_folder(tenant)
        md5_store_file = md5_store_folder + "/appflow-" + env + "-md5"
        md5_store_file_new = md5_store_folder + "/appflow-" + env + "-md5-new"
        utils.safe_remove(md5_store_file_new)
        file_list = utils.get_file_list(target_folder)
        for f in file_list:
            utils.write_md5_sum(f, md5_store_file_new)

        diff = utils.diff_files(md5_store_file, md5_store_file_new)
        return diff


def git_checkin(tenant, env):
    dir = utils.get_tenant_dir(tenant)
    folder = utils.get_tenant_env_dir(tenant, env)
    file_list = utils.get_file_list(folder)
    Encrypted = True
    for f in file_list:
        if (utils.check_string_in_file(f, 'AES256') == False):
            Encrypted = False
    diff = git_status(tenant, env)
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
    git_reset(tenant, env)


def git_checkOut(tenant, env):
    query = utils.query_yes_no(
        'Warning, this process will overwrite any un-pushed work, continue?', 'no')
    if(query == True):
        git_reset(tenant, env)
        dir = utils.get_tenant_dir(tenant)
        PIPE = subprocess.PIPE
        process = subprocess.Popen(
            ['git', '-C', dir, 'pull'], stdout=PIPE, stderr=PIPE)
