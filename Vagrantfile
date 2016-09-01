# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

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

    atlantis.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--cpus", 2, "--memory", 2048, "--name", "vagrant-atlantis", "--natdnshostresolver1", "on"]
    end

  end

end
