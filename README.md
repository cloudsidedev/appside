# AppFlow

[![Join the chat at https://gitter.im/ttssdev/appflow](https://badges.gitter.im/ttssdev/appflow.svg)](https://gitter.im/ttssdev/appflow?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

AppFlow is a multitenant environment automation tool based on Ansible.

`% make provision env=production limit=webservers tenant=mrrobot tags=base_packages`

## Features

Provisiong:

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

## Requirements

* `% brew install md5sha1sum`

### Capistrano

#### Ubuntu

```
% sudo apt-get install software-properties-common
% sudo apt-add-repository ppa:brightbox/ruby-ng
% sudo apt-get update
% sudo apt-get install ruby2.3 libxml2-dev zlib1g-dev
% sudo gem2.3 install bundler
```

## Installation

1. Create new config directory layout - `mkdir -p ~/.appflow/{tenant,vault}`
2. Copy `config.example` to `~/.appflow/config` and update variables:
  * `CFG_TENANT_ID` - identity of the own tenant
  * `CFG_TENANT_NAME` - name of the own tenant
  * `CFG_TENANT_ENV` - default provisioning environment
5. TODO

## Documentation
For easy code management, just use:
	`make checkin`
this command will automatically check if your files are already encrypted (if so, exits)
then will check and push only the files you have modified after encrpyting them
 
TODO.

## Contributing

Contributions are welcome from everyone. [Join the chat](https://gitter.im/ttssdev/appflow?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge).

## Community

Keep track of development and community news.

TODO.
