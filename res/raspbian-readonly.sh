#!/bin/bash

die() {
    echo "ERROR: $1"
    exit 1
}

[ "$(whoami)" == "root" ] || die "This script must be run as root"

# Remove unnecessary packages
apt-get remove --purge logrotate dphys-swapfile fake-hwclock
apt-get autoremove --purge

# Disable unnecessary services
disable_service() {
    systemctl stop $1
    systemctl mask $1
}
disable_service apt-daily.timer
disable_service apt-daily-upgrade.timer
disable_service man-db.timer
disable_service systemd-rfkill.socket
#disable_service systemd-hostnamed
#disable_service systemd-rfkill
#systemctl daemon-reload
#systemctl reset-failed

# Remove old folders and link them to the temporary partition
link_to_ramdisk() {
    mount $1 2>/dev/null
    if [ $? == 1 ] ; then # Could not find in fstab
        rm -rf $1/*
        echo "tmpfs $1 tmpfs nodev,nosuid 0 0" >>/etc/fstab
        mount $1 || die "Could not mount $1 partition"
    else
        echo "$1 seems to be already configured in fstab, skipping"
    fi
}
link_to_ramdisk /tmp
link_to_ramdisk /var/tmp
link_to_ramdisk /var/log
link_to_ramdisk /var/lock
link_to_ramdisk /var/spool
link_to_ramdisk /var/lib/dhcp/
link_to_ramdisk /var/lib/systemd/timesync/

# Adapt kernel command line
add_kernel_option() {
    grep "$1" /boot/cmdline.txt || sed -i "1s/$/ $1/" /boot/cmdline.txt
}
add_kernel_option fastboot
add_kernel_option noswap

# Create script to make system rw until next reboot
RW_SCRIPT=/usr/local/sbin/rw
echo "mount -o remount,rw /" >$RW_SCRIPT
echo "mount -o remount,rw /boot" >>$RW_SCRIPT
echo "echo Device will be writable until next reboot." >>$RW_SCRIPT
chmod +x $RW_SCRIPT

# Make root partition read only
make_ro() {
    cp /etc/fstab /etc/fstab.bak
    awk -v partition="$1" '($2==partition) && ($4!~",ro") {$4=$4",ro"} 1' /etc/fstab.bak >/etc/fstab
    mount -o remount "$1"
}
make_ro /boot
make_ro /

# Finished :)
echo "Setup finished, you may reboot now."
