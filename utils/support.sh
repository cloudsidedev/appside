#!/bin/sh

source ~/.appflow/config

/usr/bin/tmate -S /tmp/tmate.sock new-session -d
/usr/bin/tmate -S /tmp/tmate.sock wait tmate-ready
SESSION=`/usr/bin/tmate -S /tmp/tmate.sock display -p '#{tmate_ssh}'`

ssh atlantis "echo $SESSION | mail -s 'Support Request' $CFG_APPFLOW_SUPPORT_MAIL"
