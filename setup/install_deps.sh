#!/bin/bash
#
# Install the necessary *nix dependencies

set -o errexit

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root (use sudo)" 1>&2
    exit 1
fi

sudo apt-get -y install alsa-utils rsync sox ntpdate