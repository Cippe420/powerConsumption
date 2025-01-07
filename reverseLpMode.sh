#!/bin/bash

echo "Ripristino delle funzionalità disabilitate in corso..."

# 1. Riattiva l'HDMI
echo "Riattivazione HDMI..."
sudo vcgencmd display_power 1

# 2. Riaccendi i LED
echo "Riattivazione dei LED..."
# Activity LED
echo mmc0 | sudo tee /sys/class/leds/led0/trigger
# Power LED
echo 1 | sudo tee /sys/class/leds/led1/brightness

# 3. Riattiva l'interfaccia Ethernet
echo "Riattivazione dell'interfaccia Ethernet..."
sudo ifconfig eth0 up

# 4. Riattiva il modulo Bluetooth
echo "Riattivazione del modulo Bluetooth..."
sudo systemctl enable hciuart
sudo systemctl start hciuart
sudo systemctl enable bluetooth
sudo systemctl start bluetooth

echo "Ristabilisco la frequenza di default della cpu -> min 600 : max 1500"
echo 1500000 | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq
echo 600000 | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq

