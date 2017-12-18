#!/usr/bin/env python3
"""
Appflow CLI tool.

Type appflow to have a list of available commands.
Type appflow command -- --help to have help for the specified command.

"""
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


# We need some default configurations
# This will allow to call "appflow action *args" without always specifying
# Tenant and environment.
if os.path.exists(os.getenv('HOME') + "/.appflow/config.yml"):
    DEFAULT_CONFIG = json.loads(apyaml.get_value("config"))
    DEFAULT_TENANT = DEFAULT_CONFIG.get("appflow")["tenant"]["name"]
    DEFAULT_ENV = DEFAULT_CONFIG.get("appflow")["tenant"]["default_env"]
else:
    DEFAULT_CONFIG = ""
    DEFAULT_TENANT = ""
    DEFAULT_ENV = ""
    print("Default configs not set")
    print("Run:")
    print("appflow default \"tenant-id\" \"tenant-name\" \"default-environment\"")
    print("to setup the default configs")
    print("")


class AppFlow(object):
    """

    Appflow CLI tool.

    Type appflow to have a list of available commands.
    Type appflow command -- --help to have help for the specified command.
    """

    def update(self, branch="master"):
        """
        Simple function to update Appflow.
        This is handy for the appflow-git package.
        """
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

    def default(self, tenant_id, tenant, environment):
        """
        We need some default configurations
        This will allow to call "appflow action *args" without always specifying
        Tenant and environment.
        """
        tools.setup_default_config(tenant_id, tenant, environment)

    def init(self, tenant=DEFAULT_TENANT):
        """
        This will initialize all the folders for Assh.
        This will also setup autocompletion for the CLI tool.
        """
        tools.initialize(tenant)
        print("Default Assh folders initialized, use appflow ssh to deploy configs.")
        print("Appflow autocompletion initialized. Re-source your rc file to take effect")

    def ssh(self, tenant=DEFAULT_TENANT, env=DEFAULT_ENV):
        """
        This will deploy the ssh keys from your tenant/env
        to the Assh folders.
        """
        tools.setup_ssh(tenant, env)

    def vhosts(self, tenant=DEFAULT_TENANT):
        """
        This will setup your /etc/hosts to reflect the configs
        int your tenant/development host_vars.
        ** Needs Root Access **
        """
        tools.set_vhosts_hosts(tenant)

    def reset(self, tenant=DEFAULT_TENANT, env=DEFAULT_ENV):
        """
        Reset your local tenant repository.
        This will restore the status to the latest git pull.
        This will also reset any unpushed work.
        """
        tools.git_reset(tenant, env)

    def status(self, tenant=DEFAULT_TENANT, env=DEFAULT_ENV):
        """
        Outputs your local tenant status, any modified files.
        This is handy to have an overview of what's going to be pushed
        as a dry run.
        """
        result = tools.git_status(tenant, env)
        if result is False:
            print('Files Already Encrypted')
        else:
            print('Changed files:')
            print('\n'.join(result))

    def checkout(self, tenant=DEFAULT_TENANT, env=DEFAULT_ENV):
        """
        Git pull your local tenant repository.
        This will download the lates available code.
        This will also overwrite any unpushed work.
        """
        tools.git_check_out(tenant, env)

    def checkin(self, tenant=DEFAULT_TENANT, env=DEFAULT_ENV,
                commit="Auto Commit"):
        """
        Git push from yout local tenant repository.
        This will only push the files that were modified.
        Before any push, all the files are encrypted.
        """
        tools.git_check_in(tenant, env, commit)

    def decrypt(self, tenant=DEFAULT_TENANT, env=DEFAULT_ENV):
        """
        Decrypt your local tenant repository
        """
        print(utils.get_provision_color_string('decrypt', tenant, env))
        apansible.decrypt(tenant, env)

    def encrypt(self, tenant=DEFAULT_TENANT, env=DEFAULT_ENV):
        """
        Encrypt your local tenant repository
        """
        print(utils.get_provision_color_string('encrypt', tenant, env))
        apansible.encrypt(tenant, env)

    def tags(self, tenant=DEFAULT_TENANT, env=DEFAULT_ENV):
        """
        Show available tags. This is handy to provision only a part of them
        or skipping some of them.
        """
        print(utils.get_provision_color_string('tags', tenant, env))
        apansible.tags(tenant, env)

    def provision(self, *args):
        """
        Provision your machines.
        Syntax is:
        appflow provision tags=xxx skip_tags=xxx limit=xxx
        tags: will run only the tags specified
        skip_tags: will run all the tags except for the specified ones
        limit: limit to only some specified hosts.

        Optionally it is possible to specify:
        tenant=xxx env=xxx
        this is optional and by default will read the
        default config in ~/.appflow/config.yml
        """
        args = list(args)
        # First we check if a tenant is specified
        # Else we fallback to the default
        if any("tenant=" in s for s in args):
            match = [s for s in args if "tenant=" in s][0]
            tenant = match.split("=")[1]
            args.remove(match)
        else:
            tenant = DEFAULT_TENANT
        # Then we check if an environment is specified
        # Else we fallback to the default
        if any("env=" in s for s in args):
            match = [s for s in args if "env=" in s][0]
            env = match.split("=")[1]
            args.remove(match)
        else:
            env = DEFAULT_ENV
        print(utils.get_provision_color_string('provision', tenant, env))
        apansible.provision(tenant, env, *args)

    def get(self, file, key=None):
        """
        This will print the key you are searcing (or the whole file if key is not specified)
        Syntax:
        appflow get tenant.environment.folder.to.file.searched key.subkey.value
        """
        print(apyaml.get_value(file, key))

    def set(self, file, key, value):
        """
        This will modify and then print the key you are specifying.
        Syntax:
        appflow get tenant.environment.folder.to.file.searched key.subkey.value
        """
        print(apyaml.set_value(file, key, value))

    def rm(self, file, key):
        """
        This will remove and then print the key you are specifying.
        Syntax:
        appflow get tenant.environment.folder.to.file.searched key.subkey.value
        """
        print(apyaml.rm_value(file, key))

    def add(self, file, key, value):
        """
        This will create and then print the key you are specifying.
        Syntax:
        appflow get tenant.environment.folder.to.file.searched key.subkey.value
        """
        print(apyaml.add_value(file, key, value))


if __name__ == '__main__':
    fire.Fire(AppFlow)
