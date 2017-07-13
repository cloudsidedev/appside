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
.RED=\033[01;31m
.GREEN=\033[01;32m
.YELLOW=\033[01;33m
.BLUE=\033[01;34m
.PURPLE=\033[01;35m
.CYAN=\033[01;36m
.WHITE=\033[01;37m
.NIL=\033[00m
.CLEAR=\033[00m
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
local ?= false
limit ?= false
tags ?= false
skip_tags ?= false
verbose ?= false
url := $(url)

ifneq "$(tenant)" "CFG_TENANT_ID"
vault := tenant
endif

ifeq "$(env)" "CFG_DEFAULT_ENV"
env := $($(env))
endif

ifeq "$(firstrun)" "true"
args += -k -u vagrant
endif

ifeq "$(local)" "true"
args += -c local
endif

ifneq "$(limit)" "false"
args += --limit $(limit)
endif

ifneq "$(tags)" "false"
args += --tags $(tags)
endif

ifneq "$(skip_tags)" "false"
args += --skip-tags $(skip_tags)
endif

ifneq "$(verbose)" "false"
args += -$(verbose)
endif

ifeq "$(check)" "true"
args += --check
endif

ifeq "$(ask-sudo-pass)" "true"
args +=  --ask-sudo-pass
endif

.PHONY: provision encrypt decrypt checkin

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

update:
	git pull

init:
	# TODO: Initialize AppFlow base configuration.
	@utils/initialize.sh $(url) $(tenant) $(env)

syntax-check:
	@printf "[$(.BOLD)$(.CYAN)provision$(.CLEAR)][$(.BOLD)$(.WHITE)$($(vault))$(.CLEAR)][$(.BOLD)$(.$(env))$(.CLEAR)]\n"
	@ansible-playbook --syntax-check -i ~/.appflow/tenant/$($(tenant))/$(env)/inventory playbooks/generic.yml\
--vault-password-file ~/.appflow/vault/$($(vault))/$(env)

tags:
	@printf "[$(.BOLD)$(.CYAN)provision$(.CLEAR)][$(.BOLD)$(.WHITE)$($(vault))$(.CLEAR)][$(.BOLD)$(.$(env))$(.CLEAR)]\n"
	@ansible-playbook --list-tags -i ~/.appflow/tenant/$($(tenant))/$(env)/inventory playbooks/generic.yml \
--vault-password-file ~/.appflow/vault/$($(vault))/$(env)

provision:
	@printf "[$(.BOLD)$(.CYAN)provision$(.CLEAR)][$(.BOLD)$(.WHITE)$($(vault))$(.CLEAR)][$(.BOLD)$(.$(env))$(.CLEAR)]\n"
	@ansible-playbook $(args) -i ~/.appflow/tenant/$($(tenant))/$(env)/inventory playbooks/generic.yml \
--vault-password-file ~/.appflow/vault/$($(vault))/$(env)

provision-debug:
	@printf "[$(.BOLD)$(.CYAN)provision$(.CLEAR)][$(.BOLD)$(.WHITE)$($(vault))$(.CLEAR)][$(.BOLD)$(.$(env))$(.CLEAR)]\n"
	@ansible-playbook $(args) -i ~/.appflow/tenant/$($(tenant))/$(env)/inventory playbooks/generic.yml \
--vault-password-file ~/.appflow/vault/$($(vault))/$(env) -vvv

encrypt:
	@printf "[$(.BOLD)$(.CYAN)encrypt$(.CLEAR)][$(.BOLD)$(.WHITE)$($(vault))$(.CLEAR)][$(.BOLD)$(.$(env))$(.CLEAR)]\n"
	@find ~/.appflow/tenant/$($(tenant))/$(env) -type f ! -iname ".*" -exec ansible-vault encrypt {} \
--vault-password-file ~/.appflow/vault/$($(vault))/$(env) \; ||:

decrypt:
	@printf "[$(.BOLD)$(.CYAN)decrypt$(.CLEAR)][$(.BOLD)$(.WHITE)$($(vault))$(.CLEAR)][$(.BOLD)$(.$(env))$(.CLEAR)]\n"
	@-rm -f  ~/.appflow/tmp/.appflow-$(USER)/$($(tenant))/tmp/.appflow-$(USER)/$($(tenant))/appflow-$(env)-md5
	@mkdir -p  ~/.appflow/tmp/.appflow-$(USER)/$($(tenant))
	@find ~/.appflow/tenant/$($(tenant))/$(env) -type f ! -iname ".*" -exec ansible-vault decrypt {} \
--vault-password-file ~/.appflow/vault/$($(vault))/$(env) \; ||:
	@find ~/.appflow/tenant/$($(tenant))/$(env) -type f ! -iname ".*" -exec md5sum {} >  ~/.appflow/tmp/.appflow-$(USER)/$($(tenant))/appflow-$(env)-md5 \;

reset:
	@printf "[$(.BOLD)$(.CYAN)reset$(.CLEAR)][$(.BOLD)$(.WHITE)$($(vault))$(.CLEAR)][$(.BOLD)$(.$(env))$(.CLEAR)]\n"
	@utils/reset.sh $($(tenant)) $($(vault)) $(env) $(args) $(tenant)

status:
	@printf "[$(.BOLD)$(.CYAN)status$(.CLEAR)][$(.BOLD)$(.WHITE)$($(vault))$(.CLEAR)][$(.BOLD)$(.$(env))$(.CLEAR)]\n"
	@utils/status.sh $($(tenant)) $($(vault)) $(env) $(args) $(tenant)

checkin:
	@printf "[$(.BOLD)$(.CYAN)checkin$(.CLEAR)][$(.BOLD)$(.WHITE)$($(vault))$(.CLEAR)][$(.BOLD)$(.$(env))$(.CLEAR)]\n"
	@utils/checkin.sh $($(tenant)) $($(vault)) $(env) $(args) $(tenant)

checkout:
	@printf "[$(.BOLD)$(.CYAN)checkout$(.CLEAR)][$(.BOLD)$(.WHITE)$($(vault))$(.CLEAR)][$(.BOLD)$(.$(env))$(.CLEAR)]\n"
	@utils/checkout.sh $($(tenant)) $($(vault)) $(env) $(args) $(tenant)

jenkins:
	@source ~/.appflow/config ; docker stop jenkins ; docker-compose up -d

local:
	@printf "[$(.BOLD)$(.CYAN)auto-provision$(.CLEAR)][$(.BOLD)$(.WHITE)$($(vault))$(.CLEAR)][$(.BOLD)$(.$(env))$(.CLEAR)]\n"
	@ansible-playbook $(args) --limit local -i ~/.appflow/tenant/$($(tenant))/$(env)/inventory playbooks/local.yml \
--vault-password-file ~/.appflow/vault/$($(vault))/$(env)

ssh:
	@utils/ssh.sh $($(tenant)) $($(vault)) $(env) $(args) $(tenant)

vagrant:
	mkdir -p ~/Downloads/Software
	mkdir -p ~/Downloads/Software/Vagrant-Boxes
	cd ~/Downloads/Software/Vagrant-Boxes &&  wget -c http://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box  && mv trusty-server-cloudimg-amd64-vagrant-disk1.box trusty64.box && cd ~/Documents/webdev/appflow
	# pushd ~/Downloads/Software/Vagrant-Boxes && wget -c -q http://files.vagrantup.com/precise64.box > /dev/null && wget -c -q http://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box > /dev/null && mv trusty-server-cloudimg-amd64-vagrant-disk1.box trusty64.box && wget -c http://files.wunki.org/freebsd-10.0-amd64-wunki.box > /dev/null && popd
	ln -s -f ~/Downloads/Software/Vagrant-Boxes .
	vagrant plugin install vagrant-cachier
	# https://github.com/mitchellh/vagrant/issues/1673
	vagrant plugin install vagrant-vbguest

vagrant-centos:
	mkdir -p ~/Downloads/Software
	mkdir -p ~/Downloads/Software/Vagrant-Boxes
	cd ~/Downloads/Software/Vagrant-Boxes && wget -c http://cloud.centos.org/centos/7/vagrant/x86_64/images/CentOS-7-Vagrant-1509-x86_64-01.box  && mv CentOS-7-Vagrant-1509-x86_64-01.box centos64.box && cd ~/Documents/webdev/appflow
	ln -s -f ~/Downloads/Software/Vagrant-Boxes .
	vagrant plugin install vagrant-cachier
	vagrant plugin install vagrant-vbguest
	
support:
	@utils/support.sh

install:
	@utils/install.sh

uninstall:
	@sudo rm /usr/local/bin/appflow
