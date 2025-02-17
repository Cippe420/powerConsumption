    #!/bin/bash

echo "killing bluetooth and hdmi"
sudo rfkill block bluetooth
sudo vcgencmd display_power 0

echo "disabilito interfaccia ethernet..."
sudo ifconfig eth0 down

echo "cambio il governor in powersave..."
echo "powersave" | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

echo "Underclocking la CPU a 600 MHz..."
echo 600000 | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_max_freq
echo 600000 | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_min_freq

echo "Going to sleep, bye bye u.u"

sudo ifconfig wlan0 down
echo "i will sleep for 1h"
sleep 1h
sudo ifconfig wlan0 up
echo "Done!"
