#!/bin/sh

source ~/.appflow/config

VAR_VER_UNAME=$(uname -nrs)
VAR_VER_ANSIBLE=$(ansible --version)

tmate -S /tmp/tmate.sock new-session -d
tmate -S /tmp/tmate.sock wait tmate-ready
SESSION=`tmate -S /tmp/tmate.sock display -p '#{tmate_ssh}'`

ssh atlantis "echo '$SESSION\n\n$VAR_VER_UNAME\n\n$VAR_VER_ANSIBLE.' | mail -s 'Support Request' $CFG_APPFLOW_SUPPORT_MAIL"

echo "email sent to $CFG_APPFLOW_SUPPORT_MAIL, join: $SESSION."
