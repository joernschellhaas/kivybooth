#!/bin/bash

DEVNAME="photobooth"

die() {
    echo "ERROR: $1"
    exit 1
}

[ "$(whoami)" == "root" ] || die "This script must be run as root"

# Set host name
echo "$DEVNAME" >/etc/hostname

# Configure SSH publickey only access
keyfile=$(find /boot -name '*.pub' -print -quit)
[ -f "$keyfile" ] || die "A publickey for SSH access be located in /boot folder"
mkdir ~/.ssh
cp $keyfile ~/.ssh/authorized_keys
echo "Verify that you can connect to the device as root using your SSH key."
read -p "May I disable login for the pi user? (y|n) " -n 1 -r
echo 
[[ $REPLY =~ ^[Yy]$ ]] ||die "Could not verify that certificate login works."
passwd -l pi

# Finished :)
echo "Setup finished, you may reboot now. Your device should show up in your network as '$DEVNAME'."
