#!/usr/bin/python3

# local ??? Really necessary?
# decrypt (more complicated, have to make utils first)

### Utils
# reset
# ssh/assh
# status
# checkin
# checkout

import os
import fire


class AppFlow(object):
    def provision(self, tenant, env, *args):
        print("Provisioning:", tenant, "Environment:", env)

        inventory = os.getenv("HOME") + "/.appflow/tenant/" + \
            tenant + "/" + env + "/inventory"
        playbook = '/opt/appflow/playbooks/generic.yml'
        passwordFile = os.getenv(
            "HOME") + "/.appflow/vault/" + tenant + "/" + env

        # Convert tags=xyz to --tags xyz
        tags = list(args)
        for i, a in enumerate(tags):
            tags[i] = '--' + \
                tags[i].split('=')[0] + ' ' + tags[i].split('=')[1]

        os.system('ansible-playbook -b ' + ' '.join(tags) + ' -i ' +
                  inventory + ' ' + playbook + ' --vault-password-file ' + passwordFile)

    def encrypt(self, tenant, env, *args):
        print("Encrypting:", tenant, "Environment:", env)

        targetFolder = os.getenv(
            "HOME") + "/.appflow/tenant/" + tenant + "/" + env
        passwordFile = os.getenv(
            "HOME") + "/.appflow/vault/" + tenant + "/" + env

        os.system('find ' + targetFolder +
                  ' -type f ! -iname ".*" -exec ansible-vault encrypt {} --vault-password-file ' + passwordFile + ' \; ||:')

    def tags(self, tenant, env, *args):
        print("Tags:", tenant, "Environment:", env)
        inventory = os.getenv("HOME") + "/.appflow/tenant/" + \
            tenant + "/" + env + "/inventory"
        playbook = '/opt/appflow/playbooks/generic.yml'
        passwordFile = os.getenv(
            "HOME") + "/.appflow/vault/" + tenant + "/" + env

        os.system('ansible-playbook --list-tags -i ' + inventory +
                  ' ' + playbook + ' --vault-password-file ' + passwordFile)

    # def decrypt(self, tenant, env, *args):
    # def local(self, tenant, env, *args):


if __name__ == '__main__':
    fire.Fire(AppFlow)
