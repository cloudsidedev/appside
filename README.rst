AppFlow
=======


**Read the documentation on** `appflow.rtfd.io <https://appflow.readthedocs.io>`__

**For the playbooks, visit the** `appflow-playbooks repository <https://github.com/ttssdev/appflow-playbooks>`__

.. raw:: html

    <script src="https://asciinema.org/a/BlCYYwDRMFAg31XrfwAY6Z8yc.js" id="asciicast-BlCYYwDRMFAg31XrfwAY6Z8yc" async data-speed="1" data-theme="tango"></script>

More Screencasts: `Installation`_, `Basic setup`_, `Atlantis setup`_, `Atlantis provision`_, `Project provision`_

| Get an invite and join the conversations!
| |Slack Status|

AppFlow is a multitenant environment automation tool based on Ansible.

AppFlow is your transparent platform that incorporates the various
digital infrastructures into a continuous workflow. At the same time, it
creates a consistent environment for the entire development process,
saving time and money. AppFlow is an open source developer and DevOps
application that maps the entire development process (continuous
deployment & provisioning) from development to test & staging to
production. This ensures that the systems being managed on the different
infrastructures are deployed in the same way. At the same time, AppFlow
creates a consistent environment (on-premise, in the cloud or on bare
metal) throughout the development process. The administrators and
developers (DevOps) can therefore independently control the entire
toolchain. The automation process is created using Ansible playbooks and
contains the admin and developer code, which is stored in a git
repository (encrypted). The code (AppFlow) runs on any UNIX-like
operating system where Python can run, including Linux, BSD, and OSX.
Orchestration of the AppFlow code requires only SSH access to the
respective systems. AppFlow has been designed and optimized from DevOps
for DevOps.

Features
--------

Provisioning:

-  Multitenant architecture (different teams with different
   environments)
-  Supports ``development``, ``testing``, ``staging`` and ``production``
-  All configuration files are encrypted in git with ``ansible-vault``
-  Provision all nodes with one command

Development:

-  Provides a Vagrant based development environment called ``atlantis``
-  Code locally on any Unix-like system or Windows (cygwin)

Deployment:

-  Made for `Bedrock <https://roots.io/bedrock/>`__ projects and
   `bedrock-capistrano <https://github.com/roots/bedrock-capistrano>`__
   deployments
-  Deploy and rollback with one command

Infrastructure:

-  Builtin `Percona XtraDB Cluster
   5.6 <https://www.percona.com/software/mysql-database/percona-xtradb-cluster>`__
   and `GlusterFS <http://www.gluster.org>`__ support for sharing web
   uploads on multiple nodes
-  Easy development environments with
   `Vagrant <http://www.vagrantup.com/>`__
-  Easy server provisioning with `Ansible <http://www.ansible.com/>`__
   (Ubuntu 16.04, PHP 5.6/7)

Technologies
------------

The technology behind AppFlow uses countless best-in-class programs and
maps them in a toolbox. The software accesses an extensive repository of
various freeware packages. Out-of-the-box, many enterprise features
already exist, such as:

-  Load balancing
-  Apache / PHP
-  Web Accelerator / Caching / PageSpeed
-  Distributed file system
-  Master-Master Database
-  Backup & Monitoring Integration
-  Jailkit - chroot
-  ...

Installation
~~~~~~~~~~~~

Appflow is hosted on PiP using python3. ``pip3 install appflow`` will
install appflow. To start using it you first need to *initialize* it:
``appflow init`` follow the onscreen instructions to set it up!

Developers
~~~~~~~~~~

Contribute a new feature
^^^^^^^^^^^^^^^^^^^^^^^^

-  Create a new issue, e.g. #XX new superfeature
-  Create local branch: ``git checkout -b XX-new-superfeature``
-  Code on it.
-  Push it to remote as new branch:
   ``git push -u origin XX-new-superfeature``
-  Create new pull request
   (``base: master ... compare: XX-new-superfeature``)

Get all vars
^^^^^^^^^^^^

``ansible all -m setup --tree /tmp/facts -i examples/YOUR_TENANT/local/inventory -a "filter=ansible_distribution*"``

Contributing
------------

Contributions are welcome from everyone.

Join us! |Slack Status|

.. |Slack Status| image:: https://static1.squarespace.com/static/53f68e19e4b0f401658fbb93/58b99eee725e2580fa698860/58b9a61603596ea54d1c5035/1488819693257/slack-logo-01.png?format=100w
   :target: https://appflow-community.ttss.ch

.. start-badges

.. _Installation: https://asciinema.org/a/0lglEIPiYhsceMExzOKHBUcdZ?autoplay=1&speed=1
.. _Basic setup: https://asciinema.org/a/VRlp5YqiT4gvKXrYFYZW9Oz3l?autoplay=1&speed=1
.. _Atlantis setup: https://asciinema.org/a/pcApeQ82UF7kXrygK5jnv9GBA?autoplay=1&speed=1
.. _Atlantis provision: https://asciinema.org/a/BlCYYwDRMFAg31XrfwAY6Z8yc?autoplay=1&speed=1
.. _Project provision: https://asciinema.org/a/lWERm9quxFM91hBnGDBr1UIgH?autoplay=1&speed=1
