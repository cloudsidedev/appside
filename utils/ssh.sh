#!/bin/bash

tenant=$1
vault=$2
env=$3
args=$4
make_tenant=$5

status=`grep AES256 ~/.appflow/tenant/$tenant/$env/inventory > /dev/null; echo $?`
if [ $status -eq 0 ]; then 
	echo "Files are encrpyted, first run \"make decrypt\"." 
	false; 
	exit 1; 
fi

if [ "$(uname)" == "Darwin" ]; then
	which -s assh	
	if [[ $? != 0 ]] ; then
	  brew install assh
	fi
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
	# check if assh is installed:
	if [ ! -f "~/go/bin/assh" ]; then
		echo 'export GOPATH=$HOME/go
				export PATH=$PATH:$GOROOT/bin:$GOPATH/bin
				alias ssh="assh wrapper ssh"' >> ~/.appflow/ssh.source
		source ~/.appflow/ssh.source
		go get -u github.com/moul/advanced-ssh-config/cmd/assh
	fi
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
	echo 'Cygwin not currently supported'
fi

if [[ ! -d $HOME"/.ssh/assh.d" ]]; then
	# first run, backup personal files
	cp ~/.ssh/config ~/.ssh/config_personal
fi

mkdir -p ~/.ssh/assh.d
#cp -f ~/.appflow/tenant/$tenant/$env/assh.d/* ~/.ssh/assh.d/
assh config build > ~/.ssh/config
# Restore original config hosts
cat ~/.ssh/config_personal >> ~/.ssh/config
