#!/usr/bin/python3

# Reuirements
# fire, yaml, json, flask

import fire
import appflow.AppflowTools as tools
import appflow.AppflowAnsible as apansible
import appflow.AppflowYaml as apyaml
import appflow.AppflowUtils as utils


class AppFlow(object):

    def init(self, tenant, env):
        tools.initialize(tenant, env)

    def ssh(self, tenant, env):
        tools.setup_ssh(tenant, env)

    def reset(self, tenant, env):
        tools.git_reset(tenant, env)

    def status(self, tenant, env):
        result = tools.git_status(tenant, env)
        if (result == False):
            print('Files Already Encrypted')
        else:
            print('Changed files:')
            print('\n'.join(result))

    def checkout(self, tenant, env):
        tools.git_checkOut(tenant, env)

    def checkin(self, tenant, env):
        tools.git_checkin(tenant, env)

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
        apansible.provision(tenant, env, args)

    def get(self, file, key=None):
        apyaml.get(file, key)

    def set(self, file, key, value):
        apyaml.set(file, key, value)

    def rm(self, file, key):
        apyaml.rm(file, key)

    def add(self, file, key, value):
        apyaml.add(file, key, value)


if __name__ == '__main__':
    fire.Fire(AppFlow)
