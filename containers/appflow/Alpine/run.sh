#!/bin/bash

# eval $(ssh-agent)
# ssh-add

USER_ID=${LOCAL_USER_ID:-9001}

echo "Starting with UID : $USER_ID"

# NOTE: /home/appflow exists already due to volume mounts (just need to set perms)
adduser -s "/bin/bash" -u $USER_ID -g "" -D -H appflow

export HOME=/home/appflow

chown appflow:appflow /home/appflow
mkdir -p /home/appflow/tmp/.ssh/cm
chown -R appflow:appflow /home/appflow/tmp
echo 'alias ssh="assh wrapper ssh"' >> /home/appflow/.bashrc
PARAMS="$@"


if [[ "$DOCKERHOST_OSTYPE" =~ ^cygwin ]]; then
    cp -r /tmp/vault /home/appflow/.appflow
    chmod -x /home/appflow/.appflow/vault/*/*
fi

su appflow -c "eval \$(ssh-agent) ; ssh-add ; /opt/appflow/appflow $PARAMS"