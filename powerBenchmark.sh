#!/bin/bash
main ()
{
	touch cpuPower.txt
	echo 20 > cpuPower.txt
	python3 currentMeasure.py &
	touch cpuPower.txt
	for i in {20..40..10}; do
		echo $i > cpuPower.txt
		stress-ng -c 0 -l $i -t 2s
	done
	echo 'stop' > cpuPower.txt
}
main
