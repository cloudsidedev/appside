#!/bin/bash

if [ -z $1 ]; then
	echo "Insufficient parameters"
	exit 0
fi
if [ -z $2 ]; then
	echo "Insufficient parameters"
	exit 0
fi
if [ -z $3 ]; then
	echo "Insufficient parameters"
	exit 0
fi
current=`pwd`

mkdir -p ~/.appflow/tenant/
mkdir -p ~/.appflow/vault/
cd ~/.appflow/tenant/

#git clone $1
dir=`echo $1 | cut -d "/" -f 5`
ln -sf $dir $2

cd ~/.appflow/
if [ ! -f ~/.appflow/config ]; then
	cp ~/appflow/config.example ~/.appflow/config 
	sed -i 's/CFG_TENANT_ID=mrrobot-ttss/CFG_TENANT_ID='$dir'/g' ~/.appflow/config 
	sed -i 's/CFG_TENANT_NAME=mrrobot/CFG_TENANT_NAME='$2'/g' ~/.appflow/config 
	sed -i 's/CFG_DEFAULT_ENV=development/CFG_DEFAULT_ENV='$3'/g' ~/.appflow/config 
fi

cd $current

echo " "
echo "#######################"
echo "### Done! ###"
echo "#######################"
echo " "
echo "Now, you must add your pass in vault:"
echo "Type this command, replacing the \"password\" with your own key:"
echo "echo \"password\" > ~/.appflow/vault/$2/$3"
