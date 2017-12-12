#!/usr/bin/env python3

# Reuirements
# fire, yaml, json, flask, PyMySQL

import fire
import appflow.AppflowAnsible as apansible
import appflow.AppflowTools as tools
import appflow.AppflowUtils as utils
import appflow.AppflowYaml as apyaml


class AppFlow(object):

    def init(self, tenant):
        tools.initialize(tenant)

    def ssh(self, tenant, env):
        tools.setup_ssh(tenant, env)

    def vhosts(self, tenant):
        tools.set_vhosts_hosts(tenant)

    def reset(self, tenant, env):
        tools.git_reset(tenant, env)

    def status(self, tenant, env):
        result = tools.git_status(tenant, env)
        if result is False:
            print('Files Already Encrypted')
        else:
            print('Changed files:')
            print('\n'.join(result))

    def checkout(self, tenant, env):
        tools.git_check_out(tenant, env)

    def checkin(self, tenant, env):
        tools.git_check_in(tenant, env)

    def decrypt(self, tenant, env):
        print(utils.get_provision_color_string('decrypt', tenant, env))
        apansible.decrypt(tenant, env)

    def encrypt(self, tenant, env):
        print(utils.get_provision_color_string('encrypt', tenant, env))
        apansible.encrypt(tenant, env)

    def tags(self, tenant, env):
        print(utils.get_provision_color_string('tags', tenant, env))
        apansible.tags(tenant, env)

    def provision(self, tenant, env, *args):
        print(utils.get_provision_color_string('provision', tenant, env))
        apansible.provision(tenant, env, *args)

    def get(self, file, key=None):
        print(apyaml.get_value(file, key))

    def set(self, file, key, value):
        print(apyaml.set_value(file, key, value))

    def rm(self, file, key):
        print(pyaml.rm_value(file, key))

    def add(self, file, key, value):
        print(apyaml.add_value(file, key, value))


if __name__ == '__main__':
    fire.Fire(AppFlow)
