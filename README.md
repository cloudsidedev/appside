# AppFlow

[![Join the chat at https://gitter.im/ttssdev/appflow](https://badges.gitter.im/ttssdev/appflow.svg)](https://gitter.im/ttssdev/appflow?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

AppFlow is a multitenant environment automation tool based on Ansible.

## Auto installation

```
bash <(curl -s https://raw.githubusercontent.com/ttssdev/appflow/master/utils/appflow.sh)
```

on macOS install [brew](http://brew.sh), on GNU/Linux install [VirtualBox](https://www.virtualbox.org/wiki/Linux_Downloads) before.

## Manual installation

```
cd ~/ ; git clone git@github.com:ttssdev/appflow.git
cd ~/appflow ; make install ; source ~/.zshrc
appflow local
```

## Local development

```
appflow vagrant reload atlantis ; ssh atlantis
```

## Remote provisioning

```
appflow provision env=production limit=webservers tenant=mrrobot tags=base_packages
```

## Features

Provisioning:

* Multitenant architecture (different teams with different environments)
* Supports `development`, `testing`, `staging` and `production`
* All configuration files are encrypted in git with `ansible-vault`
* Provision all nodes with one command

Development:

* Provides a Vagrant based development environment called `atlantis`
* Code locally on any Unix-like system or Windows (cygwin)

Deployment:

* Made for [Bedrock](https://roots.io/bedrock/) projects and [bedrock-capistrano](https://github.com/roots/bedrock-capistrano) deployments
* Deploy and rollback with one command

Infrastructure:

* Builtin [Percona XtraDB Cluster 5.6](https://www.percona.com/software/mysql-database/percona-xtradb-cluster) and [GlusterFS](http://www.gluster.org) support for sharing web uploads on multiple nodes
* Easy development environments with [Vagrant](http://www.vagrantup.com/)
* Easy server provisioning with [Ansible](http://www.ansible.com/) (Ubuntu 14.04, PHP 5.6)

## Deployment requirements

### Capistrano

#### Ubuntu

```
sudo apt-get install software-properties-common
sudo apt-add-repository ppa:brightbox/ruby-ng
sudo apt-get update
sudo apt-get install ruby2.3 libxml2-dev zlib1g-dev
sudo gem2.3 install bundler
```

## Installation

1. Create new config directory layout - `mkdir -p ~/.appflow/{tenant,vault}`
2. Copy `config.example` to `~/.appflow/config` and update variables:
  * `CFG_TENANT_ID` - identity of the own tenant
  * `CFG_TENANT_NAME` - name of the own tenant
  * `CFG_TENANT_ENV` - default provisioning environment
  * `CFG_APPFLOW_SUPPORT_MAIL` - e-mail address to send support requests to
3. Copy the `appflow-mrrobot` folder in `examples` to `~/.appflow/tenant/`
4. Link the folder: `ln -s ~/.appflow/tenant/appflow-mrrobot ~/.appflow/tenant/mrrobot`
5. Copy the `vault` folder in `examples` to `~/.appflow/vault`

Now you are ready to deploy!
In the main appflow folder (where you cloned the repo) you can start provisioning with:
	`appflow provision env=development tenant=mrrobot`

## Documentation

Take a look at the [walkthrough](https://github.com/ttssdev/appflow/wiki/Walkthrough) for initial setup.

For easy code management, just use:

```
appflow checkout env=production tenant=mrrobot
appflow decrypt env=production tenant=mrrobot
edit tenant's configs in ~/.appflow/tenant/appflow-mrrobot/production
appflow status env=production tenant=mrrobot
appflow checkin env=production tenant=mrrobot
```

Forgot what you've done? go back:

`appflow reset env=production tenant=mrrobot`

Want to update everything and provision?

`appflow update ; appflow checkout ; appflow provision local=true`

## Tags

`appflow tags`

```
playbook: playbooks/generic.yml

  play #1 (all): all	TAGS: []
      TASK TAGS: [ansible, apache2, apache2-conf, apt, apt-listchanges,
      apticron, assh, assh-conf, autossh, autossh-conf, base_packages, borg,
      borgmatic, cloud, clustercheck, common, composer, env, environment,
      etckeeper, fstab, geoip, glusterfs, golang, grafana, groups, haproxy,
      haproxy-acl, haproxy-conf, hold, hosts, htaccess, htpasswd, icinga,
      icinga-conf, icinga-conf-etc, icinga-conf-hosts, icinga-ssh, jenkins,
      keepalived, keepalived-conf, letsencrypt, letsencrypt-conf, lvm, motd,
      munin, munin-conf, mysql, mysql-conf, mysql-users, mysqlpass, nodejs, ntp,
      nullmailer, percona, php, php-conf, pkg, rsyslog, shell, shell-users,
      smtpd, ssh, ssh-keys, ssl, ssl-conf, sudo, swap, update, users, varnish,
      varnish-conf, vhosts, web_packages, wp-cli, xfs, yum_proxy]
```

## Vagrant

```
vagrant plugin install vagrant-vbguest
vagrant vbguest --status
```

Before you can `appflow vm reload atlantis`. This will download the needed trusty64 box.
```
appflow vagrant
```

### Troubleshooting

#### [vagrant] Missing Vagrantfile.local.yml

```
Issue: There was an error loading a Vagrantfile. The file being loaded
       and the error message are shown below. This is usually caused by
       a syntax error.

       Path: /Users/foo/Documents/webdev/appflow/Vagrantfile
       Line number: 0
       Message: Errno::ENOENT: No such file or directory @ rb_sysopen - Vagrantfile.local.yml`

Solve: add Vagrantfile.local.yml to the appflow folder with this content:

       synced_folder:
         appflow_folder: "~/Documents/webdev/appflow"
         webdev_folder: "~/Documents/webdev/development"
```

#### [vagrant] Vagrant was unable to mount VirtualBox shared folders

```
Issue: Vagrant was unable to mount VirtualBox shared folders.
       This is usually because the filesystem "vboxsf" is not available.
       This filesystem is made available via the VirtualBox Guest Additions
       and kernel module. Please verify that these guest additions are properly
       installed in the guest. This is not a bug in Vagrant and is usually
       caused by a faulty Vagrant box. For context, the command attempted was:

       id -u deploy

       The error output from the command was:

       id: deploy: no such user

Solve: appflow provision limit=atlantis firstrun=true (password is vagrant).
```

#### [vagrant] The box you attempted to add doesn't match the provider you specified

```
Issue: The box you attempted to add doesn't match the provider you specified.

Solve: vagrant up --provider=virtualbox atlantis
```

#### [vagrant] Lost Vagrant reference to VirtualBox VM

```
Issue: Lost Vagrant reference to VirtualBox VM

Solve:
VBoxManage list vms
  "vagrant-atlantis" {xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx}
echo xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx > ~/appflow/.vagrant/machines/atlantis/virtualbox/id
```

#### [vagrant] Warning: Authentication failure. Retrying...

```
Issue: vagrant Warning: Authentication failure. Retrying...
```

Solve: [http://stackoverflow.com/a/30792296](http://stackoverflow.com/a/30792296)

#### [vagrant] an error occurred while downloading the remote file

```
Issue: An error occurred while downloading the remote file.
       The error message, if any, is reproduced below. Please fix this error and try again.

Solve: sudo mv /opt/vagrant/embedded/bin/curl /tmp
```

See also: [https://github.com/mitchellh/vagrant/issues/7997](https://github.com/mitchellh/vagrant/issues/7997)

#### [boot] An error occurred while mounting /

```
Issue: An error occurred while mounting /.
Keys: Press S to skip mounting or M for manual recovery

Solve:
Press S and try to see if atlantis boots up.
ssh atlantis
mount -o remount,rw / (optional)
e2fsck /dev/sda1
reboot
```

### Developers

#### Contribute a new feature

 - Create a new issue, e.g. #XX new superfeature
 - Create local branch: `git checkout -b XX-new-superfeature`
 - Code on it.
 - Push it to remote as new branch: `git push -u origin XX-new-superfeature`
 - Create new pull request (`base: master ... compare: XX-new-superfeature`)

#### Get all vars

`ansible all -m setup --tree /tmp/facts -i examples/appflow-mrrobot/local/inventory -a "filter=ansible_distribution*"`

## Contributing

Contributions are welcome from everyone. [Join the chat](https://gitter.im/ttssdev/appflow?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge).
