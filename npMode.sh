#!/bin/bash

echo "riabilito i servizi"

echo "bluetooth e hdmi"

sudo rfkill unblock bluetooth
#sudo /opt/vc/bin/tvservice -p
sudo vcgencmd display_power 1

# 3. Riattiva l'interfaccia Ethernet
echo "Riattivazione dell'interfaccia Ethernet..."
sudo ifconfig eth0 up

echo "ondemand" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor


echo "Ristabilisco la frequenza di default della cpu -> min 600 : max 1500"
sudo echo 1500000 | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq
sudo echo 600000 | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_min_freq

echo "Done!"
