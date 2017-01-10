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
grep -q -F '192.168.80.2 atlantis' /etc/hosts || sudo tee -a /etc/hosts<<<'192.168.80.2 atlantis'
grep -q -F '192.168.80.3 atlantis.centos' /etc/hosts || sudo tee -a /etc/hosts<<<'192.168.80.3 atlantis.centos'
grep -q -F '192.168.90.2 testing' /etc/hosts || sudo tee -a /etc/hosts<<<'192.168.90.2 testing'
grep -q -F '192.168.90.3 testing.centos' /etc/hosts || sudo tee -a /etc/hosts<<<'192.168.90.3 testing.centos'

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
sudo cp ~/appflow/appflow /usr/local/bin/appflow
sudo chmod +x /usr/local/bin/appflow

echo "#############################";
echo "Preparing the environment..."
echo "#############################";
cd ~/Documents/webdev/appflow
make local ask-sudo-pass=true;

echo "Would you like to initialize the Atlantis VM now?"
read  -n 1 -p "[y/N]:" vm
echo ""
case $vm in
	[Yy]* ) echo "Choose your distro: 
1- Ubuntu 14.04
2- CentOS/RHEL 7.1 (Experimental, still not complete!) "; read  -n 1 -p "[choose a number]:" dist;;
	[Nn]* ) ;;
	* ) echo "Please answer yes or no.";;
esac

echo ""

if [ ! -z $dist ]; then
	if [ $dist = "1" ]; then
		DIS=
	elif [ $dist = "2" ]; then
		DIS="-centos"
	else
		echo "#############################";
		echo "DONE!"
		echo "#############################";

		cd $currdir;	
		exit 0;
	fi
fi

case $vm in
	[Yy]* ) make vagrant$DIS && vagrant up atlantis$DIS;;
	[Nn]* ) ;;
	* ) echo "Please answer yes or no.";;
esac

echo ""


echo "#############################";
echo "DONE!"
echo "#############################";

cd $currdir;
