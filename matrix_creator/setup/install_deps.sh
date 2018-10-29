#!/bin/bash
#
# Install the necessary *nix dependencies

set -o errexit

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root (use sudo)" 1>&2
    exit 1
fi

# Install Matrix One repository
curl https://apt.matrix.one/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.matrix.one/raspbian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/matrixlabs.list

# Install ZeroMQ
echo "deb http://download.opensuse.org/repositories/network:/messaging:/zeromq:/release-stable/Debian_9.0/ ./" | sudo tee /etc/apt/sources.list.d/zeromq.list
wget https://download.opensuse.org/repositories/network:/messaging:/zeromq:/release-stable/Debian_9.0/Release.key -O- | sudo apt-key add

# Install NVM
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.8/install.sh | bash
source ~/.bashrc

nvm install 8.6
nvm use 8.6

npm install npm@latest -g

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install matrixio-malos