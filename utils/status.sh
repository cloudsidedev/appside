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
	#git -C ~/.appflow/tenant/$tenant/$env status | grep -v '\.\./'
	git -C ~/.appflow/tenant/$tenant diff-files --name-only -B -R -M $env
	exit 0
fi
find ~/.appflow/tenant/$tenant/$env -type f -exec md5sum {} > $HOME/.appflow/tmp/.appflow-$USER/$tenant/appflow-$env-md5-new \;
changed_files=`(diff $HOME/.appflow/tmp/.appflow-$USER/$tenant/appflow-$env-md5 $HOME/.appflow/tmp/.appflow-$USER/$tenant/appflow-$env-md5-new | cut -d " " -f 4 | grep "/" | sort | uniq )`
echo $changed_files  | tr ' ' '\n' 

