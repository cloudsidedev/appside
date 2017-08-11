#!/usr/bin/python3

# Reuirements
# fire, yaml, json

import fire
import appflow.AppflowTools as tools
import appflow.AppflowAnsible as apansible
import appflow.AppflowYaml as apyaml


class AppFlow(object):
    def init(self, tenant, env):
        tools.initialize(tenant, env)

    def ssh(self, tenant, env):
        tools.setupSsh(tenant, env)

    def reset(self, tenant, env):
        tools.gitReset(tenant, env)

    def status(self, tenant, env):
        tools.gitStatus(tenant, env)

    def checkout(self, tenant, env):
        tools.gitCheckOut(tenant, env)

    def checkin(self, tenant, env):
        tools.gitCheckin(tenant, env)

    def decrypt(self, tenant, env):
        apansible.decrypt(tenant, env)

    def encrypt(self, tenant, env):
        apansible.encrypt(tenant, env)

    def tags(self, tenant, env):
        apansible.tags(tenant, env)

    def provision(self, tenant, env, *args):
        apansible.provision(tenant, env, args)

    def get(file, key=None):
        apyaml.get(file, key)

    def set(file, key, value):
        apyaml.set(file, key, value)

    def rm(file, key):
        apyaml.rm(file, key)

    def add(file, key, value):
        apyaml.add(file, key,value)

if __name__ == '__main__':
    fire.Fire(AppFlow)
