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

    def decrypt(self, tenant, env):
        apansible.decrypt(tenant, env)


if __name__ == '__main__':
    fire.Fire(AppFlow)
