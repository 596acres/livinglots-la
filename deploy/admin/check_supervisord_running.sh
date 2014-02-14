#!/bin/bash

if ps -u $USER -o command | grep -v grep | grep "bin/supervisord" > /dev/null
then
    echo 'supervisord running'
else
    echo 'supervisord not running! starting now.'
    source $HOME/.bashrc
    workon laopenacres
    supervisord -c $HOME/var/supervisor/supervisord.conf
fi
