#!/bin/bash

# eval $(ssh-agent)
# ssh-add

USER_ID=${LOCAL_USER_ID:-9001}

echo "Starting with UID : $USER_ID"

# NOTE: /home/appflow exists already due to volume mounts (just need to set perms)
useradd --shell /bin/bash -u $USER_ID -o -c "" -M appflow
export HOME=/home/appflow

# chown -R appflow:appflow /opt/appflow
chown appflow:appflow /home/appflow
mkdir -p /home/appflow/tmp/.ssh/cm
chown -R appflow:appflow /home/appflow/tmp
# chown -R appflow:appflow /home/appflow/.ansible
echo 'alias ssh="assh wrapper ssh"' >> /home/appflow/.bashrc

# exec echo appflow "$@"
# su - appflow -c "appflow $@"
PARAMS="$@"
chmod -R -x /home/appflow/.appflow/vault
su - appflow --preserve-environment -c "eval \$(ssh-agent) ; ssh-add ; appflow $PARAMS"
