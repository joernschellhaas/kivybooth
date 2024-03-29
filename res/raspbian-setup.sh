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
if [ -f "$keyfile" ]; then
    mkdir -p ~/.ssh
    mv $keyfile ~/.ssh/authorized_keys
    echo "Verify that you can connect to the device as root using your SSH key."
    read -p "May I disable login for the pi user? (y|n) " -n 1 -r
    echo 
    [[ $REPLY =~ ^[Yy]$ ]] || die "Could not verify that certificate login works."
    passwd -l pi
fi

# Disable login tty - we only want to login via SSH and it is annoying to see that on the screen
systemctl mask getty@tty1.service

# Update OS and Packages
apt update && apt upgrade || die "Could not update packages"

# Install CUPS and libcups2 (incl. headers)
apt install cups libcups2-dev # also install `cups` ?

# Copy prepared config files
cp -Rv $(dirname "$0")/etc/ /
systemctl daemon-reload

# Finished :)
echo "Setup finished, you may reboot now. Your device should show up in your network as '$DEVNAME'."
