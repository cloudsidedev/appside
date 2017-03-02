# -*- mode: ruby -*-
# vi: set ft=ruby :
require 'yaml'

#
# Issues with MS, see: https://github.com/Varying-Vagrant-Vagrants/VVV/issues/354#issuecomment-181513066
#

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"
ANSIBLE_TAGS=ENV['ANSIBLE_TAGS']
ANSIBLE_TAGS_SKIP=ENV['ANSIBLE_TAGS_SKIP']

# Synced folders, can be overriden via Vagrantfile.local.yml
atlantis_synced_folder_appflow = "~/Documents/webdev/appflow"
atlantis_synced_folder_webdev = "~/Documents/webdev/development"
atlantis_synced_folder_mount_options = 'dmode=0775,fmode=0775'
atlantis_synced_folder_type = ""
atlantis_synced_folder_smb_username = ""
atlantis_synced_folder_smb_password = ""

custom_settings = YAML.load_file 'Vagrantfile.local.yml'
if custom_settings['synced_folder']['appflow_folder']
  atlantis_synced_folder_appflow = custom_settings['synced_folder']['appflow_folder']
end
if custom_settings['synced_folder']['webdev_folder']
  atlantis_synced_folder_webdev = custom_settings['synced_folder']['webdev_folder']
end
if custom_settings['synced_folder']['mount_options']
  atlantis_synced_folder_mount_options = custom_settings['synced_folder']['mount_options']
end
if custom_settings['synced_folder']['type']
  atlantis_synced_folder_type = custom_settings['synced_folder']['type']
end
if custom_settings['synced_folder']['smb_username']
  atlantis_synced_folder_smb_username = custom_settings['synced_folder']['smb_username']
end
if custom_settings['synced_folder']['smb_password']
  atlantis_synced_folder_smb_password = custom_settings['synced_folder']['smb_password']
end

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
    atlantis.vm.synced_folder atlantis_synced_folder_webdev, "/var/www/vhosts", owner: "deploy", group: "www-data", :mount_options => [atlantis_synced_folder_mount_options], type: atlantis_synced_folder_type, smb_username: atlantis_synced_folder_smb_username, smb_password: atlantis_synced_folder_smb_password
    atlantis.vm.synced_folder atlantis_synced_folder_appflow, "/var/appflow", owner: "deploy", group: "www-data", :mount_options => [atlantis_synced_folder_mount_options], type: atlantis_synced_folder_type

    atlantis.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--cpus", 2, "--memory", 2048, "--name", "vagrant-atlantis", "--natdnshostresolver1", "on"]
    end

  end

  config.vm.define "atlantis.centos" do |atlantiscentos|
    atlantiscentos.vm.box = "atlantis.centos"
    atlantiscentos.vm.hostname = "atlantis.centos"
    atlantiscentos.vm.box_url = "Vagrant-Boxes/centos64.box"
    atlantiscentos.vm.network :private_network, ip: "192.168.80.3"
    atlantiscentos.vm.synced_folder atlantis_synced_folder_webdev, "/var/www/vhosts", owner: "deploy", group: "www-data", :mount_options => ['dmode=0775,fmode=0775']
    atlantiscentos.vm.synced_folder atlantis_synced_folder_appflow, "/var/appflow", owner: "deploy", group: "www-data", :mount_options => ['dmode=0775,fmode=0775']

    atlantiscentos.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--cpus", 2, "--memory", 2048, "--name", "vagrant-atlantis-centos", "--natdnshostresolver1", "on"]
    end

  end

  config.vm.define "testing" do |testing|
    testing.vm.box = "testing"
    testing.vm.hostname = "testing"
    testing.vm.box_url = "Vagrant-Boxes/ubuntu-ttss.box"
    testing.vm.network :private_network, ip: "192.168.90.2"
    testing.vm.boot_timeout = 400 # defaults 300
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
      ansible.skip_tags = ANSIBLE_TAGS_SKIP
    end

  end

end
