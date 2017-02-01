#!/bin/bash

DIST=`uname -s`
echo "#############################";
echo "Installing AppFlow..."
echo "#############################";
sudo mkdir -p /usr/local/bin/
sudo cp $HOME/appflow/appflow /usr/local/bin/appflow
sudo chmod +x /usr/local/bin/appflow
if [ $DIST == 'Darwin' ]; then
	sudo cp $HOME/appflow/utils/autocomplete /usr/local/etc/bash_completion.d/appflow
	source /usr/local/etc/bash_completion.d
else
	sudo cp $HOME/appflow/utils/autocomplete /etc/bash_completion.d/appflow
	source /usr/share/bash-completion/bash_completion
fi
