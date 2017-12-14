#!/usr/bin/env python3

# Requirements
# fire, yaml, json, flask, PyMySQL

import json
import os
import subprocess

import fire

import appflow.AppflowAnsible as apansible
import appflow.AppflowTools as tools
import appflow.AppflowUtils as utils
import appflow.AppflowYaml as apyaml


class AppFlow(object):

    default_config = json.loads(apyaml.get_value("config"))
    default_tenant = default_config.get("appflow")["tenant"]["name"]
    default_env = default_config.get("appflow")["tenant"]["default_env"]

    def test(self, branch="master"):
        appflow_dir = os.path.dirname(os.path.realpath(__file__))
        _pipe = subprocess.PIPE
        out = subprocess.Popen(
            ['git', '-C', appflow_dir, 'checkout', branch],
            stdout=_pipe,
            stderr=_pipe)
        for line in iter(out.stdout.readline, b''):
            print(line.decode('utf-8'))
        out = subprocess.Popen(
            ['git', '-C', appflow_dir, 'pull'],
            stdout=_pipe,
            stderr=_pipe)
        for line in iter(out.stdout.readline, b''):
            print(line.decode('utf-8'))

    def init(self, tenant=default_tenant):
        tools.initialize(tenant)

    def ssh(self, tenant=default_tenant, env=default_env):
        tools.setup_ssh(tenant, env)

    def vhosts(self, tenant=default_tenant):
        tools.set_vhosts_hosts(tenant)

    def reset(self, tenant=default_tenant, env=default_env):
        tools.git_reset(tenant, env)

    def status(self, tenant=default_tenant, env=default_env):
        result = tools.git_status(tenant, env)
        if result is False:
            print('Files Already Encrypted')
        else:
            print('Changed files:')
            print('\n'.join(result))

    def checkout(self, tenant=default_tenant, env=default_env):
        tools.git_check_out(tenant, env)

    def checkin(self, tenant=default_tenant, env=default_env,
                commit="Auto Commit"):
        tools.git_check_in(tenant, env, commit)

    def decrypt(self, tenant=default_tenant, env=default_env):
        print(utils.get_provision_color_string('decrypt', tenant, env))
        apansible.decrypt(tenant, env)

    def encrypt(self, tenant=default_tenant, env=default_env):
        print(utils.get_provision_color_string('encrypt', tenant, env))
        apansible.encrypt(tenant, env)

    def tags(self, tenant=default_tenant, env=default_env):
        print(utils.get_provision_color_string('tags', tenant, env))
        apansible.tags(tenant, env)

    def provision(self, tenant=default_tenant, env=default_env, *args):
        print(utils.get_provision_color_string('provision', tenant, env))
        apansible.provision(tenant, env, *args)

    def get(self, file, key=None):
        print(apyaml.get_value(file, key))

    def set(self, file, key, value):
        print(apyaml.set_value(file, key, value))

    def rm(self, file, key):
        print(apyaml.rm_value(file, key))

    def add(self, file, key, value):
        print(apyaml.add_value(file, key, value))


if __name__ == '__main__':
    fire.Fire(AppFlow)
