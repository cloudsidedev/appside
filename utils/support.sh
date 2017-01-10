#!/bin/sh

source ~/.appflow/config

tmate -S /tmp/tmate.sock new-session -d
tmate -S /tmp/tmate.sock wait tmate-ready
SESSION=`tmate -S /tmp/tmate.sock display -p '#{tmate_ssh}'`

ssh atlantis "echo $SESSION | mail -s 'Support Request' $CFG_APPFLOW_SUPPORT_MAIL"
