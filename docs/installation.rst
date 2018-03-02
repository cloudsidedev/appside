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

At this point the installation is **complete**. Now we will illustrate the folder structure.


Others
~~~~~~

**Fix Ansible problems on 14.04**

The python3 version Shipped with Ubuntu 14.04 is not enough to use ansible from pip3 that Appflow
brings as dependency.
We need to remove it and default to the PPA installation:

::

    -  sudo pip3 uninstall ansible
    -  sudo apt install python2 python2-pip python3 python3-pip git
    -  sudo apt-add-repository ppa:ansible/ansible
    -  sudo apt install ansible
