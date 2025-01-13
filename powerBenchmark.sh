#!/bin/bash


main ()
{
 	
	
	for i in {20..80..10}
	do
		echo "sto stressando $i%"
		stress-ng -c 0 -l $i -t 60s
	done

	rm log.txt
	touch log.txt
}


main
