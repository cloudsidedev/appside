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
status=`grep AES256 ~/.appflow/tenant/$tenant/$env/inventory > /dev/null; echo $?`
if [ $status -eq 0 ]; then 
	echo "Files are already encrpyted, nothing to do." 
	false; 
	exit 1; 
fi
find ~/.appflow/tenant/$tenant/$env -type f -exec md5sum {} > /tmp/.appflow/$tenant/appflow-$env-md5-new \;
changed_files=`(diff /tmp/.appflow/$tenant/appflow-$env-md5 /tmp/.appflow/$tenant/appflow-$env-md5-new | cut -d " " -f 4 | grep "/" | sort | uniq )`
make encrypt tenant=$make_tenant
echo $changed_files  | tr ' ' '\n' |  xargs git -C ~/.appflow/tenant/$tenant add
git -C ~/.appflow/tenant/$tenant commit -m "Auto commit"
git -C ~/.appflow/tenant/$tenant push
git -C ~/.appflow/tenant/$tenant checkout .
rm /tmp/.appflow/$tenant/appflow-$env-md5-new
