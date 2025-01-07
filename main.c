#include<stdlib.h>

void paladin()
{
    /* list of possibly necessary daemons

    avahi-daemon
    bluetooth
    console-setup
    cron
    systemd-binfmt.service                                      loaded active     exited       Set Up Additional Binary Formats
    systemd-fsck@dev-disk-by\x2dpartuuid-2349536d\x2d01.service loaded active     exited       File System Check on /dev/disk/by-partuuid/2349536d-01
    systemd-journal-flush.service                               loaded active     exited       Flush Journal to Persistent Storage
    systemd-journald.service                                    loaded active     running      Journal Service
    systemd-logind.service                                      loaded active     running      User Login Management
    systemd-modules-load.service                                loaded active     exited       Load Kernel Modules
    systemd-random-seed.service                                 loaded active     exited       Load/Save Random Seed
    systemd-remount-fs.service                                  loaded active     exited       Remount Root and Kernel File Systems
    systemd-sysctl.service                                      loaded active     exited       Apply Kernel Variables
    systemd-sysusers.service                                    loaded active     exited       Create System Users
    systemd-timesyncd.service                                   loaded active     running      Network Time Synchronization
    systemd-tmpfiles-setup-dev.service                          loaded active     exited       Create Static Device Nodes in /dev
    systemd-tmpfiles-setup.service                              loaded active     exited       Create System Files and Directories
    systemd-udev-trigger.service                                loaded active     exited       Coldplug All udev Devices
    otbr-agent.service                                          loaded activating auto-restart OpenThread Border Router Agent
    otbr-firewall.service                                       loaded active     exited       LSB: OTBR firewall
    mdns.service
    bluetooth.service                                           loaded active     running      Bluetooth service
    
    
    
    */
}


int main()
{
    // get all the running daemons on the system
    // disable them if they are not the ones you want


    // disable every interface that is not in use (hdmi...led...)
    // sudo uhubctl kinda thing

    // underclock the raspberrypi


}