.. include:: global.rst.inc
.. highlight:: bash
.. _usefultips:

Useful Tips
============

Aliases
~~~~~~~

An useful alias you can add to your ``.bashrc`` or your ``.zshrc`` is:


::

    vagup(){pushd ~/.appflow/playbooks; vagrant up $@; popd}
    vaghalt(){pushd ~/.appflow/playbooks; vagrant halt $@; popd}
    vagdestroy(){pushd ~/.appflow/playbooks; vagrant destroy $@; popd}

This will make your vagrant managing much faster.

Update Playbooks and Vagrantfile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since the split in ``Appflow`` and ``Appflow-Playbooks``, you can now just update
yout playbooks and Vagrantfile using:

::

    appflow update




