#!/bin/bash
currdir=`pwd`

echo "Installing dependencies...";
echo "#############################";
DIST=`uname -s`
if [ $DIST == 'Darwin' ]; then 
	brew unlink ansible ; brew unlink ansible20 ; brew reinstall ansible --HEAD;
else 
	sudo pip install git+git://github.com/ansible/ansible.git;
fi

echo "#############################";
echo "Configuring default Hosts..."
echo "#############################";
echo '192.168.80.2 atlantis
192.168.80.3 atlantis.centos
192.168.90.2 testing
192.168.90.3 testing.centos' | sudo tee -a /etc/hosts

echo "#############################";
echo "Configuring default Dirs..."
echo "#############################";
mkdir -p ~/Documents/webdev;
cd ~/Documents/webdev;

echo "#############################";
echo "Cloning AppFlow..."
echo "#############################";
git clone git@github.com:ttssdev/appflow.git;
ln -s ~/Documents/webdev/appflow ~/appflow;

echo "#############################";
echo "Preparing the environment..."
echo "#############################";
cd ~/Documents/webdev/appflow
make local ask-sudo-pass=true;

echo "#############################";
echo "DONE!"
echo "#############################";

cd $currdir;
