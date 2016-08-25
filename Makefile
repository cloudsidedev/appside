#
# AppFlow - Makefile
#
#	Usage examples:
#
#		% make provision tenant=mrrobot env=development|testing|staging|production firstrun=true|false
#		% make encrypt tenant=mrrobot env=development|testing|staging|production
#		% make decrypt tenant=mrrobot env=development|testing|staging|production
#
# TODO:
#
#		- Add support for ansible limit options.
#		- Add support for ansible tag options.
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

tenant ?= CFG_TENANT_ID
vault ?= CFG_TENANT_NAME
env ?= CFG_DEFAULT_ENV
firstrun ?= ""
# TODO: limit ?= ""
# TODO: tags ?= ""

ifneq "$(tenant)" "CFG_TENANT_ID"
vault := tenant
endif

ifeq "$(env)" "CFG_DEFAULT_ENV"
env := $($(env))
endif

ifeq "$(firstrun)" "true"
args := "-k -u vagrant"
endif

.PHONY: provision encrpy decrypt

#
# Tasks
#
all:
	@echo tenant: $($(tenant))
	@echo env: $(env)
	@echo firstrun: $(args)
	@echo vault: $($(vault))

initialize:
	# TODO: Initialize AppFlow base configuration.

provision:
	@echo "[$(.BOLD)$(.CYAN)provision$(.CLEAR)][$(.BOLD)$(.WHITE)$($(vault))$(.CLEAR)][$(.BOLD)$(.$(env))$(.CLEAR)]"
	@echo ansible-playbook $(args) -s -i tenant/$($(tenant))/$(env)/inventory generic.yml \
	--vault-password-file ~/.appflow/vault/$($(vault))/$(env)

encrypt:
	@echo "[$(.BOLD)$(.CYAN)encrypt$(.CLEAR)][$(.BOLD)$(.WHITE)$($(vault))$(.CLEAR)][$(.BOLD)$(.$(env))$(.CLEAR)]"
	@find ~/appflow/tenant/$($(tenant))/$(env) -type f -exec ansible-vault encrypt {} \
	--vault-password-file ~/.appflow/vault/$($(vault))/$(env) \; ||:

decrypt:
	@echo "[$(.BOLD)$(.CYAN)decrypt$(.CLEAR)][$(.BOLD)$(.WHITE)$($(vault))$(.CLEAR)][$(.BOLD)$(.$(env))$(.CLEAR)]"
	@find ~/appflow/tenant/$($(tenant))/$(env) -type f -exec ansible-vault decrypt {} \
	--vault-password-file ~/.appflow/vault/$($(vault))/$(env) \; ||:
