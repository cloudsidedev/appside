Setting up a new user
=====================

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
(you can find it in **$HOME/.ssh/id_rsa.pub**)
``private_key``     is not needed for a simple user
``is_deployer``     will specify if this user is allowed to deploy
``is_mysql_admin``  will specify if this user is a mysql admin

**User Groups**
You can also specify in what group the user should (or not) be. 
Populate the ``groups`` line with a list of the groups.
``www_group``                   is likely needed for a developer and deployer.
``conf_sudo_nopasswd_group``    is likely needed for a mantainer and admin user.

And that's it.
If you want to add new users you can simply clone the settings of the example user 
and modify the confs as described.


