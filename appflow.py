#!/usr/bin/python3

# Reuirements
# fire, yaml, json

import fire
import appflow.AppflowTools as tools
import appflow.AppflowAnsible as apansible


class AppFlow(object):

    def reset(self, tenant, env):
        tools.gitReset(tenant, env)

    def status(self, tenant, env):
        tools.gitStatus(tenant, env)

    def checkin(self, tenant, env):
        tools.gitCheckin(tenant, env)

    def init(self, tenant, env):
        tools.initialize(tenant, env)

    def ssh(self, tenant, env):
        tools.setupSsh(tenant, env)

    def checkout(self, tenant, env):
        tools.gitCheckOut(tenant, env)

    def decrypt(self, tenant, env):
        apansible.decrypt(tenant, env)

    def encrypt(self, tenant, env):
        apansible.encrypt(tenant, env)


if __name__ == '__main__':
    fire.Fire(AppFlow)
