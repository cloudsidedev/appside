.. include:: global.rst.inc
.. highlight:: none
.. _faq:

Frequently asked questions
==========================

Usage & Issues
##############


## Vagrant

```
vagrant plugin install vagrant-vbguest
vagrant vbguest --status
```

Before you can `appflow vm reload atlantis`. This will download the needed trusty64 box.
```
appflow vagrant
```

### Troubleshooting

#### [vagrant] Missing Vagrantfile.local.yml

```
Issue: There was an error loading a Vagrantfile. The file being loaded
       and the error message are shown below. This is usually caused by
       a syntax error.

       Path: /Users/foo/Documents/webdev/appflow/Vagrantfile
       Line number: 0
       Message: Errno::ENOENT: No such file or directory @ rb_sysopen - Vagrantfile.local.yml`

Solve: add Vagrantfile.local.yml to the appflow folder with this content:

       synced_folder:
         appflow_folder: "~/Documents/webdev/appflow"
         webdev_folder: "~/Documents/webdev/development"
```

#### [vagrant] Vagrant was unable to mount VirtualBox shared folders

```
Issue: Vagrant was unable to mount VirtualBox shared folders.
       This is usually because the filesystem "vboxsf" is not available.
       This filesystem is made available via the VirtualBox Guest Additions
       and kernel module. Please verify that these guest additions are properly
       installed in the guest. This is not a bug in Vagrant and is usually
       caused by a faulty Vagrant box. For context, the command attempted was:

       id -u deploy

       The error output from the command was:

       id: deploy: no such user

Solve: appflow provision limit=atlantis firstrun=true (password is vagrant).
```

#### [vagrant] The box you attempted to add doesn't match the provider you specified

```
Issue: The box you attempted to add doesn't match the provider you specified.

Solve: vagrant up --provider=virtualbox atlantis
```

#### [vagrant] Lost Vagrant reference to VirtualBox VM

```
Issue: Lost Vagrant reference to VirtualBox VM

Solve:
VBoxManage list vms
  "vagrant-atlantis" {xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx}
echo xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxx > ~/appflow/.vagrant/machines/atlantis/virtualbox/id
```

#### [vagrant] Warning: Authentication failure. Retrying...

```
Issue: vagrant Warning: Authentication failure. Retrying...
```

Solve: [http://stackoverflow.com/a/30792296](http://stackoverflow.com/a/30792296)

#### [vagrant] an error occurred while downloading the remote file

```
Issue: An error occurred while downloading the remote file.
       The error message, if any, is reproduced below. Please fix this error and try again.

Solve: sudo mv /opt/vagrant/embedded/bin/curl /tmp
```

See also: [https://github.com/mitchellh/vagrant/issues/7997](https://github.com/mitchellh/vagrant/issues/7997)

#### [boot] An error occurred while mounting /

```
Issue: An error occurred while mounting /.
Keys: Press S to skip mounting or M for manual recovery

Solve:
Press S and try to see if atlantis boots up.
ssh atlantis
mount -o remount,rw / (optional)
e2fsck /dev/sda1
reboot
```


