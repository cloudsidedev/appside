#!/bin/bash

if [ $# -ge 3 ]
then
  OPT_TENANT=$1
  OPT_ENV=$2
  OPT_SSH_USER=$3
  OPT_HOST=$4
elif [ $# -ge 4 ]
then
  OPT_TENANT=$1
  OPT_ENV=$2
  OPT_SSH_USER="appflow"
  OPT_HOST=$4
else
  echo "Usage: utils/bootstrap.sh <tenant> <env> [<ssh-username>] <host>"
  exit -1
fi

echo -n "Enter your ssh password and press [ENTER] (will not be shown): "
read -s OPT_SSH_PASSWORD
echo

mkdir -p ~/.appflow/{tenant,vault}
mkdir -p ~/.appflow/tenant/appflow-$OPT_TENANT
echo "foo: $OPT_SSH_PASSWORD"
