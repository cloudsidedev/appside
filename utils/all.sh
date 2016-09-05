#!/bin/sh

#
# Execute Makefile tasks on all tenants for each environment.
#

ENVS=(development staging production)
TENANTS=$(find ~/.appflow/tenant -type l -exec basename {} \;)

if [ "$1" ]
then

    for TENANT in $TENANTS
    do
        for ENV in "${ENVS[@]}"
        do
            make $1 tenant=$TENANT env=$ENV
        done
    done
else
    echo "% utils/all.sh decrypt"
fi
