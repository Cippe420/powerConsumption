#!/bin/bash
main ()
{
	#python3 currentMeasure.py &
	touch cpuPower.txt
	for i in {20..80..10}; do
		echo $i > cpuPower.txt
		stress-ng -c 0 -l $i -t 2s
	done
	echo 'stop' > cpuPower.txt
}
main
