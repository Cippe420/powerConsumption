#!/bin/bash

# script to configure a low power mode for rasp
echo "Procedo a ridurre le funzionalità..."

# disable hdmi
echo "disabilito hdmi..."
sudo vcgencmd display_power 0

#disable eth interface (maybe still powered by hub, so no power reduction)
echo "disabilito interfaccia ethernet..."
sudo ifconfig eth0 down

# disable bluetooth interface
echo "disabilito bluetooth interface..."
sudo systemctl disable hciuart
sudo systemctl stop hciuart

# disable bluetooth service
echo "disabilito il servizio bluetoot..."
sudo systemctl disable bluetooth
sudo systemctl stop bluetooth

# 5. Routine per underclockare la cpu

echo "Underclocking la CPU a 600 MHz..."
echo 600000 | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq
echo 600000 | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_min_freq



