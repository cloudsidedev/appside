#
# AppFlow - Makefile
#
#	Usage examples:
#
#		% make provision tenant=mrrobot env=development|testing|staging|production \
#		firstrun=true|false limit=webservers tags=vhosts verbose=vvv
#
#		% make encrypt tenant=mrrobot env=development|testing|staging|production
#
#		% make decrypt tenant=mrrobot env=development|testing|staging|production
#

#
# Macros
#
.CLEAR=\x1b[0m
.BOLD=\x1b[01m
.RED=\x1b[31;01m
.GREEN=\x1b[32;01m
.BLUE=\x1b[34;01m
.YELLOW=\x1b[33;01m
.WHITE=\x1b[97;01m
.CYAN=\x1b[36;01m
.development=$(.GREEN)development$(.CLEAR)
.testing=$(.BLUE)testing$(.CLEAR)
.staging=$(.YELLOW)staging$(.CLEAR)
.production=$(.RED)production$(.CLEAR)

#
# Options
#
include ~/.appflow/config

args ?= -b
tenant ?= CFG_TENANT_ID
vault ?= CFG_TENANT_NAME
env ?= CFG_DEFAULT_ENV
firstrun ?= false
limit ?= false
tags ?= false
verbose ?= false

ifneq "$(tenant)" "CFG_TENANT_ID"
vault := tenant
endif

ifeq "$(env)" "CFG_DEFAULT_ENV"
env := $($(env))
endif

ifeq "$(firstrun)" "true"
args += -k -u vagrant
endif

ifneq "$(limit)" "false"
args += --limit $(limit)
endif

ifneq "$(tags)" "false"
args += --tags $(tags)
endif

ifneq "$(verbose)" "false"
args += -$(verbose)
endif

.PHONY: provision encrpy decrypt

#
# Tasks
#
all: help debug

debug:
	@echo "Environment settings"
	@echo "  tenant: $($(tenant))"
	@echo "  vault: $($(vault))"
	@echo "  env: $(env)"
	@echo "  args: $(args)"

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  provision  to start provisioning"
	@echo "  encrypt    to encrypt vault data"
	@echo "  decrypt    to decrypt vault data"

initialize:
	# TODO: Initialize AppFlow base configuration.

tags:
	@echo "[$(.BOLD)$(.CYAN)provision$(.CLEAR)][$(.BOLD)$(.WHITE)$($(vault))$(.CLEAR)][$(.BOLD)$(.$(env))$(.CLEAR)]"
	@ansible-playbook --list-tags -i ~/.appflow/tenant/$($(tenant))/$(env)/inventory playbooks/generic.yml

provision:
	@echo "[$(.BOLD)$(.CYAN)provision$(.CLEAR)][$(.BOLD)$(.WHITE)$($(vault))$(.CLEAR)][$(.BOLD)$(.$(env))$(.CLEAR)]"
	@ansible-playbook $(args) -i ~/.appflow/tenant/$($(tenant))/$(env)/inventory playbooks/generic.yml \
--vault-password-file ~/.appflow/vault/$($(vault))/$(env)

encrypt:
	@echo "[$(.BOLD)$(.CYAN)encrypt$(.CLEAR)][$(.BOLD)$(.WHITE)$($(vault))$(.CLEAR)][$(.BOLD)$(.$(env))$(.CLEAR)]"
	@find ~/.appflow/tenant/$($(tenant))/$(env) -type f -exec ansible-vault encrypt {} \
--vault-password-file ~/.appflow/vault/$($(vault))/$(env) \; ||:

decrypt:
	@echo "[$(.BOLD)$(.CYAN)decrypt$(.CLEAR)][$(.BOLD)$(.WHITE)$($(vault))$(.CLEAR)][$(.BOLD)$(.$(env))$(.CLEAR)]"
	@find ~/.appflow/tenant/$($(tenant))/$(env) -type f -exec ansible-vault decrypt {} \
--vault-password-file ~/.appflow/vault/$($(vault))/$(env) \; ||:

vagrant:
	mkdir -p ~/Downloads/Software
	mkdir -p ~/Downloads/Software/Vagrant-Boxes
	cd ~/Downloads/Software/Vagrant-Boxes && wget -c -q http://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box > /dev/null && mv trusty-server-cloudimg-amd64-vagrant-disk1.box trusty64.box && cd ~/Documents/webdev/wpcommon/ansible
	# pushd ~/Downloads/Software/Vagrant-Boxes && wget -c -q http://files.vagrantup.com/precise64.box > /dev/null && wget -c -q http://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box > /dev/null && mv trusty-server-cloudimg-amd64-vagrant-disk1.box trusty64.box && wget -c http://files.wunki.org/freebsd-10.0-amd64-wunki.box > /dev/null && popd
	ln -s -f ~/Downloads/Software/Vagrant-Boxes .
	vagrant plugin install vagrant-cachier
	# https://github.com/mitchellh/vagrant/issues/1673
	vagrant plugin install vagrant-vbguest
