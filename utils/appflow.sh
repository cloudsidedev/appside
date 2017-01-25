#!/bin/bash
currdir=`pwd`

cd $HOME
echo "Installing dependencies...";
echo "#############################";
DIST=`uname -s`
if [ $DIST == 'Darwin' ]; then 
	if ! brew ls --versions bash-completion | grep HEAD; then
		brew install bash-completion
	fi
	if ! brew ls --versions ansible | grep HEAD; then
		brew unlink ansible ; brew unlink ansible20 ; brew reinstall ansible --HEAD;
	fi 
	brew install caskroom/cask/brew-cask
	if ! brew cask ls --versions virtualbox; then 
		brew cask install virtualbox	
	fi 
	if ! brew cask ls --versions vagrant; then 
		brew cask install vagrant
	fi 
	if ! brew cask ls --versions vagrant-manager; then 
		brew cask install vagrant-manager
	fi 
else 
	declare -A osInfo;
	osInfo[/etc/redhat-release]=dnf
	osInfo[/etc/SuSE-release]=zypp
	osInfo[/etc/debian_version]=apt-get
	PKG=
	for f in ${!osInfo[@]} 
	do
		if [[ -f $f ]]; then
			PKG=${osInfo[$f]}
		fi
	done
	sudo pip install git+git://github.com/ansible/ansible.git; 
	sudo $PKG install -y vagrant virtualbox bash-completion
	if (($? == 1)); then
		echo "Error! Check your dependencies! Without vagrant and virtualbox
you cannot use AppFlow, But it can still be installed.
Would You Like to continue?"
		
		read  -n 1 -p "[y/N]:" vm
		echo ""
		case $vm in
			[Yy]* ) ;;
			[Nn]* ) exit 1;;
			* ) echo "Please answer yes or no.";;
		esac
	fi
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
mkdir -p $HOME/Documents/webdev;
cd $HOME/Documents/webdev;

echo "#############################";
echo "Cloning AppFlow..."
echo "#############################";
git clone git@github.com:ttssdev/appflow.git;
ln -s $HOME/Documents/webdev/appflow $HOME/appflow;


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

echo "#############################";
echo "Preparing the environment..."
echo "#############################";

mkdir -p $HOME/.appflow/tenant
ln -s $HOME/Documents/webdev/appflow/examples/appflow-mrrobot $HOME/.appflow/tenant/appflow-mrrobot
ln -s $HOME/.appflow/tenant/appflow-mrrobot  $HOME/.appflow/tenant/mrrobot
ln -s $HOME/Documents/webdev/appflow/examples/vault $HOME/.appflow/tenant/vault 
cp $HOME/Documents/webdev/appflow/config.example $HOME/.appflow/config
cd $HOME/Documents/webdev/appflow
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
	[Yy]* ) make vagrant$DIS && vagrant up atlantis$DIS && appflow provision firstrun=true limit=atlantis$DIS;;
	[Nn]* ) ;;
	* ) echo "Please answer yes or no.";;
esac

echo ""


echo "#############################";
echo "DONE!"
echo "#############################";

cd $currdir;
