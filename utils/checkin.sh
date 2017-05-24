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
FILES=`find ~/.appflow/tenant/$tenant/$env/`
ENC=true
for f in $FILES; do 
	if [ -f $f ]; then
		status=`grep AES256 $f > /dev/null; echo $?`
		if [ $status -eq 0 ]; then 
			echo "Files are already encrpyted, nothing to do."
		else
			ENC=false
		fi
	fi
done
find ~/.appflow/tenant/$tenant/$env -type f -exec md5sum {} > /tmp/.appflow-$USER/$tenant/appflow-$env-md5-new \;
changed_files=`(diff /tmp/.appflow-$USER/$tenant/appflow-$env-md5 /tmp/.appflow-$USER/$tenant/appflow-$env-md5-new | cut -d " " -f 4 | grep "/" | sort | uniq )`
if [ "$ENC" = false ]; then
	make encrypt tenant=$make_tenant env=$env
fi
echo $changed_files  | tr ' ' '\n' |  xargs git -C ~/.appflow/tenant/$tenant add
git -C ~/.appflow/tenant/$tenant commit -m "Auto commit"
git -C ~/.appflow/tenant/$tenant push
git -C ~/.appflow/tenant/$tenant/$env checkout .
rm /tmp/.appflow-$USER/$tenant/appflow-$env-md5-new
