#!/bin/bash

source $HOME/.bashrc
source $HOME/.virtualenvs/laopenacres/bin/activate
django-admin.py sync_rss
