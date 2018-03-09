.. include:: global.rst.inc
.. highlight:: bash
.. _usage:

Usage
=====

The following section will cover some basic usages of Appflow.

Folder Structure
~~~~~~~~~~~~~~~~

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


Setting up a new user
~~~~~~~~~~~~~~~~~~~~~


.. raw:: html

    <script src="https://asciinema.org/a/VRlp5YqiT4gvKXrYFYZW9Oz3l.js" id="asciicast-VRlp5YqiT4gvKXrYFYZW9Oz3l" async data-speed="1" data-theme="tango"></script>

More Screencasts: `Installation`_, `Atlantis setup`_, `Atlantis provision`_, `Project provision`_

This sction will refere to the **example tenant** that you will find in this repository:
`Appflow-Example repository <https://github.com/ttssdev/appflow-example>`__

To setup a new user, you will need to modify the file

::

    $HOME/.appflow/tenant/appflow-example/development/group_vars/all

There is a section called **conf_users**. Here you will find a series of users
that will be configured in your base system.

The example tenant will have the seguent code:

.. code-block:: python


  REPLACE_USER_NAME:
    state: enabled
    groups: "{{ conf_sudo_nopasswd_group }},{{ conf_www_group }}"
    name: "Basic User"
    home: "/home/REPLACE_USER_NAME"
    shell: "{{ conf_zsh_path }}"
    public_key: |
      REPLACE_SSH_KEY
    private_key:
    is_deployer: yes
    is_mysql_admin: yes

  deploy:
    state: enabled
    groups: "{{ conf_www_group }}"
    name: "Capistrano Deploy User"
    home: "/home/deploy"
    shell: "{{ conf_zsh_path }}"
    public_key: |
       REPLACE_SSH_KEY
    private_key: |
    is_deployer: no
    is_mysql_admin: yes


As you can see the structure is pretty simple, just REPLACE_SSH_KEY with **YOUR public ssh key**
(you can find it in **$HOME/.ssh/id_rsa.pub**).

``private_key``     is not needed for a simple user

``is_deployer``     will specify if this user is allowed to deploy

``is_mysql_admin``  will specify if this user is a mysql admin

**User Groups**
You can also specify in what group the user should (or not) be. 

Populate the ``groups`` line with a list of the groups.

``conf_www_group``                   is likely needed for a developer and deployer.

``conf_sudo_nopasswd_group``         is likely needed for a mantainer and admin user.

And that's it.

If you want to add new users you can simply clone the settings of the example user 
and modify the confs as described.


Setting up a new Project
~~~~~~~~~~~~~~~~~~~~~~~~

.. raw:: html

    <script src="https://asciinema.org/a/lWERm9quxFM91hBnGDBr1UIgH.js" id="asciicast-lWERm9quxFM91hBnGDBr1UIgH" async data-speed="1" data-theme="tango"></script>

More Screencasts: `Installation`_, `Basic setup`_, `Atlantis setup`_, `Atlantis provision`_

A project is defined in a tenant as a virtual host.

**Setup a vhost**

Referring to the *example tenant*, there is a section called ``conf_vhosts``.
Here you will find:


.. code-block:: python

  example:
    state: enabled
    servername: dev.example.com
    serveralias:
      - www.dev.example.com
    serveradmin: webmaster@ttss.ch
    db_name: example_wp
    db_user: example_wp
    db_password: We9Diel2
    db_server: 127.0.0.1
    db_host: '%'
    db_prefix: ahCh7Fei
    glusterfs_uploads: example
    type: wp_bedrock
    config_env: true
    env_opt: |
      CFG_URL_DEVELOPMENT='https://dev.example.com'
      CFG_URL_STAGING='https://stage.example.com'
      CFG_URL_PRODUCTION='https://example.com'
      WPMDB_LICENCE='XXXXXXXXXXXXXXXXXXXXXXXXXXX'
    wp_salt: |
      AUTH_KEY=']+-v`hHqK.M |QO.1|sYEqM5v:^^[3-,]:s?Bbtus9@y+nEbE7+ladg.E|H+<EC|'
      SECURE_AUTH_KEY='94ZoJdn,s:Jy)p-.pH-A3`GtK$BrwZTL6lA-520F=/l90*,i]t-zI|0QZn)Cq#1|'
      LOGGED_IN_KEY='$Jd>Gv{:5}^r|!=.F8*Psg{j_B27TVC{n-R<@9GqF[d`@$WhGd+tf?OiPyN8kcb8'
      NONCE_KEY='46^*wL<)IzG01Y/m_e,|Hb/B-!5:mc#.w{6~@ipSSJc*|67>d[|HJ&OY*|DXjV83'
      AUTH_SALT='!;oV$#%N3WcL*VsW3IkhI0}FtO/fJ`*H}n18.3.2bT5sW/svc-1nKnp~PONKT<B$'
      SECURE_AUTH_SALT='iqyy{?<h`fNX/iQ}on>cmB|/bbRD*nZD;8fGDH5`an_-Qj|:h|yO|two>a-yZ;*x'
      LOGGED_IN_SALT='l82hxF[w)R)L|bqw:a@;x=+geLouagDu:)}ss1k=T:!#.fc:9ZU{hJPEmV`7<BRi'
      NONCE_SALT='R{~-C+p|eJ=mEF,5F$m-|8@<HocSO!e&GNPw{_GTjW]c@to@8[O3RJA7:G-gMu!F'
    htaccess:
    htpasswd_password: false
    ssl_pemfile:
    ssl_haproxy: false
    ssl_pem:
    bkup: false
    bkup_www_hosts:
    bkup_mysql_hosts:
    bkup_cron_schedule:


Just replace the values with the one needed in your project.
In particular pay attention to the ``db_user`` and ``db_password``.
For the ``wp_salt`` section you can refer to `This Website <https://api.wordpress.org/secret-key/1.1/salt/>`__
to generate random values for the project.

Setting Up Atlantis (14.04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This procedure has to be executed in the Atlantis VM.
To enter it just do

::

    - vagrant ssh atlantis

We need percona repo to complete the provisioning
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

From inside atlantis we have to perform the following commands:

::

    -   wget https://repo.percona.com/apt/percona-release_0.1-4.$(lsb_release -sc)_all.deb
    -   sudo dpkg -i percona-release_0.1-4.$(lsb_release -sc)_all.deb
    -   sudo apt update
    -   sudo apt-get install -y percona-xtradb-cluster-server-5.7

Upgrade Packages
^^^^^^^^^^^^^^^^

::

    -  sudo apt update && sudo apt upgrade
    -  sudo pip list --outdated --format=columns | grep -v sdist | awk '{print $1}' | tail -n +3 | xargs -n1 sudo pip install -U
    -  sudo pip list --outdated --format=columns | grep -v sdist | awk '{print $1}' | tail -n +3 | xargs -n1 sudo pip3 install -U

Setting Up Atlantis (16.04)
~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. raw:: html

    <script src="https://asciinema.org/a/pcApeQ82UF7kXrygK5jnv9GBA.js" id="asciicast-pcApeQ82UF7kXrygK5jnv9GBA" async data-speed="1" data-theme="tango"></script>

More Screencasts: `Installation`_, `Basic setup`_, `Atlantis provision`_, `Project provision`_

We first need to install Python or ansible will not work
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    - vagrant ssh atlantis -c "sudo apt-get install -y python"


We now need to setup the percona repo and package to install
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First we enter atlantis using 

::

    - vagrant ssh atlantis

Then from inside atlantis we have to perform the following commands:

::

    -   wget https://repo.percona.com/apt/percona-release_0.1-4.$(lsb_release -sc)_all.deb
    -   sudo dpkg -i percona-release_0.1-4.$(lsb_release -sc)_all.deb
    -   sudo apt update
    -   sudo apt-get install -y percona-xtradb-cluster-server-5.7
    -   sudo chown mysql:mysql /run/mysqld



note: get ssh pwd for ubuntu user:
""""""""""""""""""""""""""""""""""

::

    -   vagrant ssh atlantis -c "echo $(cat ~/.ssh/id_rsa.pub) | sudo tee -a /home/ubuntu/.ssh/authorized_keys"
    -   vagrant ssh atlantis -c "sudo passwd ubuntu"


Provision Atlantis
~~~~~~~~~~~~~~~~~~

.. raw:: html

    <script src="https://asciinema.org/a/BlCYYwDRMFAg31XrfwAY6Z8yc.js" id="asciicast-BlCYYwDRMFAg31XrfwAY6Z8yc" async data-speed="1" data-theme="tango"></script>

More Screencasts: `Installation`_, `Basic setup`_, `Atlantis setup`_, `Project provision`_

To provision atlantis we have first to use the ``--first-run`` flag, because the basic users are not yet configured.

::

    - appflow provision --env development --tenant example --limit atlantis --first-run True


From now on the ``--first-run`` flag can be ignored as your ``id_rsa.pub`` key will be used to authenticate.

After the first provision that will setup all the basic packages, users and configs,
the most useful ``tags`` you will use are:

- ``--tags env``            this will provision ``.env``
- ``--tags htaccess``       this will provision ``.htaccess``
- ``--tags vhosts``         this will provision the projects/vhosts
- ``--tags mysql``          this will provision both ``db`` and ``users``
- ``--tags shell-users``    this will provision any new users that will be created afterwards.

**Remember, tags can be concatenated, for example**

::

    - appflow provision --env development --tenant example --limit atlantis,testing --tags htaccess,env,vhosts,mysql



.. start-badges

.. _Installation: https://asciinema.org/a/0lglEIPiYhsceMExzOKHBUcdZ?autoplay=1&speed=1
.. _Basic setup: https://asciinema.org/a/VRlp5YqiT4gvKXrYFYZW9Oz3l?autoplay=1&speed=1
.. _Atlantis setup: https://asciinema.org/a/pcApeQ82UF7kXrygK5jnv9GBA?autoplay=1&speed=1
.. _Atlantis provision: https://asciinema.org/a/BlCYYwDRMFAg31XrfwAY6Z8yc?autoplay=1&speed=1
.. _Project provision: https://asciinema.org/a/lWERm9quxFM91hBnGDBr1UIgH?autoplay=1&speed=1
