    #!/bin/bash

echo "killing bluetooth and hdmi"
sudo rfkill block bluetooth
sudo vcgencmd display_power 0

echo "disabilito interfaccia ethernet..."
sudo ifconfig eth0 down
sudo ifconfig wlan0 down
