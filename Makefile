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

ifeq "$(local)" "true"
args += -c local
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

syntax-check:
	@echo "[$(.BOLD)$(.CYAN)provision$(.CLEAR)][$(.BOLD)$(.WHITE)$($(vault))$(.CLEAR)][$(.BOLD)$(.$(env))$(.CLEAR)]"
	@ansible-playbook --syntax-check -i ~/.appflow/tenant/$($(tenant))/$(env)/inventory playbooks/generic.yml

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
	@rm /tmp/.appflow/$($(tenant))/appflow-md5
	@mkdir -p /tmp/.appflow/$($(tenant))
	@find ~/.appflow/tenant/$($(tenant))/$(env) -type f -exec ansible-vault decrypt {} \
--vault-password-file ~/.appflow/vault/$($(vault))/$(env) \; ||:
	@find ~/.appflow/tenant/$($(tenant))/$(env) -type f -exec md5sum {} > /tmp/.appflow/$($(tenant))/appflow-md5 \;

checkin:
	#Check if files are already encrypted; if so, exit gracefully because there is nothing to do
	$(eval status = $(shell grep AES256 ~/.appflow/tenant/$($(tenant))/development/inventory > /dev/null; echo $$?))
	@if [ $(status) -eq 0 ]; \
		then \
		echo "Files are already encrpyted, nothing to do." \
		false; \
		exit 1; \
	fi
	@find ~/.appflow/tenant/$($(tenant))/$(env) -type f -exec md5sum {} > /tmp/.appflow/$($(tenant))/appflow-md5-new \;	
	
	$(eval .changed_files = $(shell diff /tmp/.appflow/$($(tenant))/appflow-md5 /tmp/.appflow/$($(tenant))/appflow-md5-new | cut -d " " -f 4 | grep "/" | sort | uniq))
	
	$(MAKE) encrypt
	
	@echo $(.changed_files) | sed 's/ /\n/' | xargs git -C ~/.appflow/tenant/$($(tenant)) add
	git -C ~/.appflow/tenant/$($(tenant)) commit -m "Auto commit"
	git -C ~/.appflow/tenant/$($(tenant)) push 
	git -C ~/.appflow/tenant/$($(tenant)) checkout .
	
	@rm /tmp/.appflow/$($(tenant))/appflow-md5-new
	#
	# we want to git commit files in the tenant's configs only if they have
	# been really edited:
	#
	#	- make decrypt will make git think all files have changed locally.
	#	- find only really locally modified files, encrypt and commit them.
	#	- all other files, which have not been edited but just decryped: git checkout.
	#
	# decrypt and then encrypt always marks the files as modified, they never
	# re-encrypt with the same value. We need to decrypt, save MD5s of each unecrpyted
	# file, check if MD5 of file has been changed directly after encrpyting, if so
	# encrpyt and commit, all other files git checkout.
	#

vagrant:
	mkdir -p ~/Downloads/Software
	mkdir -p ~/Downloads/Software/Vagrant-Boxes
	cd ~/Downloads/Software/Vagrant-Boxes && wget -c -q http://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box > /dev/null && mv trusty-server-cloudimg-amd64-vagrant-disk1.box trusty64.box && cd ~/Documents/webdev/appflow
	# pushd ~/Downloads/Software/Vagrant-Boxes && wget -c -q http://files.vagrantup.com/precise64.box > /dev/null && wget -c -q http://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box > /dev/null && mv trusty-server-cloudimg-amd64-vagrant-disk1.box trusty64.box && wget -c http://files.wunki.org/freebsd-10.0-amd64-wunki.box > /dev/null && popd
	ln -s -f ~/Downloads/Software/Vagrant-Boxes .
	vagrant plugin install vagrant-cachier
	# https://github.com/mitchellh/vagrant/issues/1673
	vagrant plugin install vagrant-vbguest
