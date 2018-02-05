.. include:: global.rst.inc
.. highlight:: bash
.. _installation:

Installation
============

The preferred method to install |project_name| is using:

::

    pip3 install appflow

this will install the appflow executable you will use.

This installation is incomplete without initializing the playbooks and your tenant.
To initialize use:

::

   appflow init

Then follow the simple instructions to choose your tenant name and default environment.

This will initialize your folders and default playbooks in the appflow config directory.
This folder is placed in **$HOME** in **$HOME/.appflow**

You will find here:

:: 

    ls ~/.appflow  
    .appflow  
    ├── config.yml 
    ├── playbooks  
    ├── tenant 
    ├── tmp 
    └── vault   

    4 directories, 1 file

What you need to know:

**config.yml** 
holds your default config (default tenant, environment) so you do not
have to specify them always.
To use something different from defaults, |project_name| allows you to specify 
them during your command:
*appflow provision --tenant ANOTHER_TENANT --env ANOTHER_ENV*

**playbooks** 
this is where all playbooks are placed, you can contribute to them visiting
the repository: `Appflow-Playbooks
<https://github.com/ttssdev/appflow-playbooks>`_.
To keep them updated, you can just type *appflow update*

**tenant** 
this is where all your tenants (you can have as many as you wish) will be placed.
all TEnants aRE ogranized by name (*~/.appflow/tenant/tenant1, ~/.appflow/tenant/tenant2*...)
in your tenant you then specify the inventory files for each 
environment (*~/.appflow/tenant/tenant1/development, ~/.appflow/tenant/tenant1/testing*...)

**vault** 
this will hold your passwords to decrypt your intentories (**appflow decrypt**, **appflow encrypt**)
it's organized in a similar fashon of tenant folder:
*~/.appflow/vault/tenant1/* this folder will contain files with the password.
These files have to be named with the environment they correspond to:
*~/.appflow/vault/tenant1/development*...

in your tenant you then specify the inventory files for each environment (*~/.appflow/tenant/tenant1/development, ~/.appflow/tenant/tenant1/testing*...)

**Fix Ansible problems on 14.04**

The python3 version Shipped with Ubuntu 14.04 is not enough to use ansible from pip3 that Appflow
brings as dependency.
We need to remove it and default to the PPA installation:

::

    -  sudo pip3 uninstall ansible
    -  sudo apt install python2 python2-pip python3 python3-pip git
    -  sudo apt-add-repository ppa:ansible/ansible
    -  sudo apt install ansible


Setting Up Atlantis (14.04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This procedure has to be executed in the Atlantis VM.
To enter it just do

``vagrant ssh atlantis``

We need percona repo to complete the provisioning
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    -   wget https://repo.percona.com/apt/percona-release_0.1-4.$(lsb_release -sc)_all.deb
    -   sudo dpkg -i percona-release_0.1-4.$(lsb_release -sc)_all.deb
    -   sudo apt update
    -   sudo apt-get install -y percona-xtradb-cluster-server-5.7
    -   sudo chown mysql:mysql /run/mysqld

Upgrade Packages
^^^^^^^^^^^^^^^^

::

    -  sudo apt update && sudo apt upgrade
    -  sudo pip list --outdated --format=columns | grep -v sdist | awk '{print $1}' | tail -n +3 | xargs -n1 sudo pip install -U
    -  sudo pip list --outdated --format=columns | grep -v sdist | awk '{print $1}' | tail -n +3 | xargs -n1 sudo pip3 install -U

Setting Up Atlantis (16.04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

We first need to install Python or ansible will not work
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    - sudo apt-get install -y python


We now need to setup the percona repo and package to install
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    -   wget https://repo.percona.com/apt/percona-release_0.1-4.$(lsb_release -sc)_all.deb
    -   sudo dpkg -i percona-release_0.1-4.$(lsb_release -sc)_all.deb
    -   sudo apt update
    -   sudo apt-get install -y percona-xtradb-cluster-server-5.7
    -   sudo chown mysql:mysql /run/mysqld



note: get ssh pwd for ubuntu user:
""""""""""""""""""""""""""""""""""

::

    -   vagrant ssh atlantis -c "echo $(cat ~/.ssh/id_rsa.pub) | sudo tee /home/ubuntu/.ssh/authorized_keys"
    -   vagrant ssh atlantis -c "sudo passwd ubuntu"
