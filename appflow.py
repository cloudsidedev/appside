#!/usr/bin/env python3
"""
Appflow CLI tool.

Type appflow to have a list of available commands.
Type appflow command -- --help to have help for the specified command.

"""

import json
import os

import fire

import lib.appflow_ansible as apansible
import lib.appflow_tools as tools
import lib.appflow_utils as utils
import lib.appflow_yaml as apyaml

__version__ = "1.0.1.4"

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
    print("appflow init")
    print("to setup the default configs")
    print("")


class AppFlow(object):
    """

    Appflow CLI tool.

    Type appflow to have a list of available commands.
    Type appflow command -- --help to have help for the specified command.
    """

    def update(self):
        """
        Simple function to update Appflow.
        This is handy for the appflow-git package.
        """
        tools.git_update_playbooks()

    def init(self, tenant=None, env=None):
        """
        This will initialize all the folders for Assh.
        This will also setup autocompletion for the CLI tool.

        :type  tenant: string
        :param tenant: The name of the tenant.

        :type  env: string
        :param env: The name of the tenant.
        """
        tools.initialize(tenant, env)

    def ssh(self, tenant=DEFAULT_TENANT, env=DEFAULT_ENV):
        """
        This will deploy the ssh keys from your tenant/env
        to the Assh folders.

        :type  tenant: string
        :param tenant: The name of the tenant.

        :type  env: string
        :param env: The name of the tenant.
        """
        tools.setup_ssh(tenant, env)

    def vhosts(self, tenant=DEFAULT_TENANT):
        """
        This will setup your /etc/hosts to reflect the configs
        int your tenant/development host_vars.
        ** Needs Root Access **

        :type  tenant: string
        :param tenant: The name of the tenant.
        """
        tools.set_vhosts_hosts(tenant)

    def reset(self, tenant=DEFAULT_TENANT, env=DEFAULT_ENV):
        """
        Reset your local tenant repository.
        This will restore the status to the latest git pull.
        This will also reset any unpushed work.

        :type  tenant: string
        :param tenant: The name of the tenant.

        :type  env: string
        :param env: The name of the tenant.
        """
        tools.git_reset(tenant, env)

    def status(self, tenant=DEFAULT_TENANT, env=DEFAULT_ENV):
        """
        Outputs your local tenant status, any modified files.
        This is handy to have an overview of what's going to be pushed
        as a dry run.

        :type  tenant: string
        :param tenant: The name of the tenant.

        :type  env: string
        :param env: The name of the tenant.
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

        :type  tenant: string
        :param tenant: The name of the tenant.

        :type  env: string
        :param env: The name of the tenant.
        """
        tools.git_check_out(tenant, env)

    def checkin(self, tenant=DEFAULT_TENANT, env=DEFAULT_ENV,
                commit="Auto Commit"):
        """
        Git push from yout local tenant repository.
        This will only push the files that were modified.
        Before any push, all the files are encrypted.

        :type  tenant: string
        :param tenant: The name of the tenant.

        :type  env: string
        :param env: The name of the tenant.

        :type  commit: string
        :param commit: The commit message to use
                        when committing. (default Auto Commit)
        """
        tools.git_check_in(tenant, env, commit)

    def decrypt(self, tenant=DEFAULT_TENANT, env=DEFAULT_ENV):
        """
        Decrypt your local tenant repository

        :type  tenant: string
        :param tenant: The name of the tenant.

        :type  env: string
        :param env: The name of the tenant.
        """
        print(utils.get_provision_color_string('decrypt', tenant, env))
        apansible.decrypt(tenant, env)

    def encrypt(self, tenant=DEFAULT_TENANT, env=DEFAULT_ENV):
        """
        Encrypt your local tenant repository

        :type  tenant: string
        :param tenant: The name of the tenant.

        :type  env: string
        :param env: The name of the tenant.
        """
        print(utils.get_provision_color_string('encrypt', tenant, env))
        apansible.encrypt(tenant, env)

    def tags(self, tenant=DEFAULT_TENANT, env=DEFAULT_ENV):
        """
        Show available tags. This is handy to provision only a part of them
        or skipping some of them.

        :type  tenant: string
        :param tenant: The name of the tenant.

        :type  env: string
        :param env: The name of the tenant.
        """
        print(utils.get_provision_color_string('tags', tenant, env))
        apansible.list_tags(tenant, env)

    def provision(self, tenant=DEFAULT_TENANT, env=DEFAULT_ENV,
                  limit: str = None, tags: str = None, skip_tags: str = None,
                  firstrun: bool = False, local: bool = False, debug: bool = False):
        """
        Provision your machines.
        Syntax is:
        appflow provision "machine1,machine2" tag1,tag2 skiptag1,skiptag2
        tags: will run only the tags specified
        skip_tags: will run all the tags except for the specified ones
        limit: limit to only some specified hosts.

        Optionally it is possible to specify custom tenant and environment
        appflow provision tenant-name env-name...
        this is optional and by default will read the
        default config in ~/.appflow/config.yml

        :type  tenant: string
        :param tenant: The name of the tenant.

        :type  env: string
        :param env: The name of the tenant.

        :type  limit: string
        :param limit: Comma separated list of hosts to provision. (default None)

        :type  tags: string
        :param tags: Comma separated list of tags to exec (default All).

        :type  skip_tags: string
        :param skip_tags: Comma separated list of tags to skip (default None).

        :type  firstrun: bool
        :param firstrun: if it's first run (default False)

        :type  local: bool
        :param local: if it's doing a local auto-provision (default False)

        :type  debug: bool
        :param debug: if it's a debug run (default False)

        """
        print(utils.get_provision_color_string('provision', tenant, env))
        apansible.provision(tenant, env, limit, tags,
                            skip_tags, firstrun, local, debug)

    def get(self, file, key=None):
        """
        This will print the key you are searcing (or the whole file if key is not specified)
        Syntax:
        appflow get tenant.environment.folder.to.file.searched key.subkey.value

        :type  file: string
        :param file: path.to.file (dot encoded) where to search the key.

        :type  key: string
        :param key: The key to search.
        """
        print(apyaml.get_value(file, key))

    def set(self, file, key, value):
        """
        This will modify and then print the key you are specifying.
        Syntax:
        appflow get tenant.environment.folder.to.file.searched key.subkey.value

        :type  file: string
        :param file: path.to.file (dot encoded) where to set the key.

        :type  key: string
        :param key: The key to search.

        :type  value: T
        :param value: the value to set.
        """
        print(apyaml.set_value(file, key, value))

    def rm(self, file, key):
        """
        This will remove and then print the key you are specifying.
        Syntax:
        appflow get tenant.environment.folder.to.file.searched key.subkey.value

        :type  file: string
        :param file: path.to.file (dot encoded) where to remove the key.

        :type  key: string
        :param key: The key to search.
        """
        print(apyaml.rm_value(file, key))

    def add(self, file, key, value):
        """
        This will create and then print the key you are specifying.
        Syntax:
        appflow get tenant.environment.folder.to.file.searched key.subkey.value

        :type  file: string
        :param file: path.to.file (dot encoded) where to set the key.

        :type  key: string
        :param key: The key to search. (this function will add it if not found.)

        :type  value: T
        :param value: the value to set.
        """
        print(apyaml.add_value(file, key, value))

    def version(self):
        """
        This will print the appflow version
        """
        print(__version__)


if __name__ == '__main__':
    fire.Fire(AppFlow)
