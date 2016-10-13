#!/bin/sh

#
# Execute Makefile tasks on all tenants for each environment.
#

tenant=$1
vault=$2
env=$3
args=$4
make_tenant=$5

# Check if files are already encrypted; if so, exit gracefully because there is nothing to do
git -C ~/.appflow/tenant/$tenant checkout $env
