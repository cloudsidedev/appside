# AppFlow walkthrough

Here we document all steps needed for setting up AppFlow on a blank developer machine, usually running OS X or GNU/Linux.

## Requirements

Be sure to have installed this components:

* [brew](https://github.com/Homebrew/brew/)
* [VirtualBox](https://www.virtualbox.org)
* [Vagrant](https://www.vagrantup.com/downloads.html)

### AppFlow installation

```
% bash <(curl -s https://raw.githubusercontent.com/ttssdev/appflow/master/utils/appflow.sh)
```

Install and run AppFlow locally to provision all the required packages.
AppFlow installs different packages depending on the local development environment:

- [OS X](https://github.com/ttssdev/appflow/tree/master/playbooks/vars/os/environment/Darwin-local.yml)
- [GNU/Linux](https://github.com/ttssdev/appflow/tree/master/playbooks/vars/os/environment/Linux-local.yml)

## AppFlow configuration

1. Create new config directory layout - `mkdir -p ~/.appflow/{tenant,vault}`
2. Copy `config.example` to `~/.appflow/config` and update variables:
  * `CFG_TENANT_ID` - identity of the own tenant
  * `CFG_TENANT_NAME` - name of the own tenant
  * `CFG_TENANT_ENV` - default provisioning environment
3. Copy the `appflow-mrrobot` folder in `examples` to `~/.appflow/tenant/`
4. Link the folder: `ln -s ~/.appflow/tenant/appflow-mrrobot ~/.appflow/tenant/mrrobot`
5. Copy the `vault` folder in `examples` to `~/.appflow/vault`

Now you are ready to deploy!
In the main appflow folder (where you cloned the repo) you can start provisioning with:
	`make provision env=development tenant=mrrobot`

## Atlantis VM

```
% cd ~/appflow
% make vagrant
% vagrant up
```

## Provison local assh settings for tenants

```
% cd ~/appflow
% make ssh [tenant=<tenant>] [env=<environment>]
% assh config build > ~/.ssh/config
```
