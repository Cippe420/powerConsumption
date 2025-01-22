#!/bin/bash
main ()
{
	for i in {20..40..10}; do
		echo $i > cpuPower.txt
		stress-ng -c 0 -l $i -t 10s
	done
}
main
