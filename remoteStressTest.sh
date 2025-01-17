#!/bin/bash
python3 currentMeasure.py &

# wait for button press
read -n 1 -s -r -p "Press q to quit"

# kill the python script
kill $PID
