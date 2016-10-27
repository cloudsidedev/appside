# -*- mode: ruby -*-
# vi: set ft=ruby :

#
# Issues with MS, see: https://github.com/Varying-Vagrant-Vagrants/VVV/issues/354#issuecomment-181513066
#

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"
ANSIBLE_TAGS=ENV['ANSIBLE_TAGS']


Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :machine
  end

  ############
  # ATLANTIS #
  ############
  config.vm.define "atlantis" do |atlantis|
    atlantis.vm.box = "atlantis"
    atlantis.vm.hostname = "atlantis"
    atlantis.vm.box_url = "Vagrant-Boxes/trusty64.box"
    atlantis.vm.network :private_network, ip: "192.168.80.2"
    atlantis.vm.synced_folder "~/Documents/webdev/development", "/var/www/vhosts", owner: "deploy", group: "www-data", :mount_options => ['dmode=0775,fmode=0775']
    atlantis.vm.synced_folder "~/Documents/webdev/appflow", "/var/appflow", owner: "deploy", group: "www-data", :mount_options => ['dmode=0775,fmode=0775']

    atlantis.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--cpus", 2, "--memory", 2048, "--name", "vagrant-atlantis", "--natdnshostresolver1", "on"]
    end

  end

  config.vm.define "atlantis.centos" do |atlantiscentos|
    atlantiscentos.vm.box = "atlantis.centos"
    atlantiscentos.vm.hostname = "atlantis.centos"
    atlantiscentos.vm.box_url = "Vagrant-Boxes/centos64.box"
    atlantiscentos.vm.network :private_network, ip: "192.168.80.3"
    atlantiscentos.vm.synced_folder "~/Documents/webdev/development", "/var/www/vhosts", owner: "deploy", group: "www-data", :mount_options => ['dmode=0775,fmode=0775']
    atlantiscentos.vm.synced_folder "~/Documents/webdev/appflow", "/var/appflow", owner: "deploy", group: "www-data", :mount_options => ['dmode=0775,fmode=0775']

    atlantiscentos.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--cpus", 2, "--memory", 2048, "--name", "vagrant-atlantis-centos", "--natdnshostresolver1", "on"]
    end

  end

  config.vm.define "testing" do |testing|
    testing.vm.box = "testing"
    testing.vm.hostname = "testing"
    testing.vm.box_url = "Vagrant-Boxes/ubuntu-ttss.box"
    testing.vm.network :private_network, ip: "192.168.90.2"
    # testing.vm.synced_folder "~/Documents/webdev/development", "/var/www/vhosts", owner: "deploy", group: "www-data", :mount_options => ['dmode=0775,fmode=0775']
    # testing.vm.synced_folder "~/Documents/webdev/appflow", "/var/appflow", owner: "deploy", group: "www-data", :mount_options => ['dmode=0775,fmode=0775']

    testing.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--cpus", 1, "--memory", 512, "--name", "vagrant-testing", "--natdnshostresolver1", "on"]
    end

    testing.vm.provision "fix-no-tty", type: "shell" do |s|
      s.privileged = false
      s.inline = "sudo sed -i '/tty/!s/mesg n/tty -s \\&\\& mesg n/' /root/.profile"
    end

    testing.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbooks/generic.yml"
      ansible.inventory_path = "~/.appflow/tenant/appflow-ttss/development/inventory"
      ansible.vault_password_file = "~/.appflow/vault/ttss/development"
      ansible.sudo = true
      ansible.tags = ANSIBLE_TAGS
    end

  end

  config.vm.define "testing.centos" do |testingcentos|
    testingcentos.vm.box = "testing.centos"
    testingcentos.vm.hostname = "testing.centos"
    # TESTFIX
    testingcentos.vm.host_name = 'testing.centos'
    # TESTFIX
    testingcentos.vm.box_url = "Vagrant-Boxes/centos-ttss.box"
    testingcentos.vm.network :private_network, ip: "192.168.90.3"
    config.vm.synced_folder ".", "/home/vagrant/sync", disabled: true
    # testingcentos.vm.synced_folder "~/Documents/webdev/development", "/var/www/vhosts", owner: "deploy", group: "www-data", :mount_options => ['dmode=0775,fmode=0775']
    # testingcentos.vm.synced_folder "~/Documents/webdev/appflow", "/var/appflow", owner: "deploy", group: "www-data", :mount_options => ['dmode=0775,fmode=0775']

    testingcentos.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--cpus", 1, "--memory", 512, "--name", "vagrant-testing-centos", "--natdnshostresolver1", "on"]
    end

#    testingcentos.vm.provision "fix-no-tty", type: "shell" do |s|
#      s.privileged = false
#      s.inline = "sudo sed -i '/tty/!s/mesg n/tty -s \\&\\& mesg n/' /root/.profile"
#    end

    testingcentos.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbooks/generic.yml"
      ansible.inventory_path = "~/.appflow/tenant/appflow-ttss/development/inventory"
      ansible.vault_password_file = "~/.appflow/vault/ttss/development"
      ansible.sudo = true
      ansible.tags = ANSIBLE_TAGS
    end

  end

end
