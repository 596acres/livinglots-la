#!/bin/bash
#
# Install node (assumes you're on a Webfaction server)
#

NODE_VERSION=0.10.25

mkdir -p ~/src/
cd ~/src/
wget http://nodejs.org/dist/v$NODE_VERSION/node-v$NODE_VERSION.tar.gz
tar -xzf node-v$NODE_VERSION.tar.gz
cd node-v$NODE_VERSION
alias python=python2.7
python configure --prefix=$HOME
make
make install
