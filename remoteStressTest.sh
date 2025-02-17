#!/bin/bash

usage()
{
    echo "Usage: remoteStressTest.sh [-i] [-t SECONDS] [-m SSH_MACHINE]"
    echo "Options: -m SSH_MACHINE    Specify the machine to ssh into"
    echo "                           "
    echo "         -t SECONDS        Specify the time to run the test"
    echo "         -i                Run in interactive mode"  
    exit 1
}


main()
{

    hastosleep=false
    interactive=false
    processes=()
    sshprocesses=()
    rm cpuPower.txt
    touch cpuPower.txt
    # parse options

    while getopts "it:m:" opt; do
        case $opt in
            m)
                sshmachine=$OPTARG
                echo "sshmachine: $sshmachine"
                ;;

            t)
                sleeptime=$OPTARG
                hastosleep=true
                echo "sleeptime: $sleeptime"
                ;;

            i)
                interactive=true
                echo "interactive: $interactive"
                ;;
            \?)
                usage
                ;;
        esac
    done

    ssh $sshmachine 'python3 -u powerConsumption/pwr.py' >> cpuPower.txt &
    sshprocesses+=($!)

    python3 dynamicGraph.py -o output.csv -s summary.csv -v &
    # args are the ip address of the remote machine
    processes+=($!)

    # wait on input
    for i in "${processes[@]}"; do
        echo runnando in background il processo : $i
    done

    for i in "${sshprocesses[@]}"; do
        echo runnando in ssh il processo : $i
    done

    nSensors=0
    echo "Totale sensori nella rete: $nSensors" >> output.csv

    if $hastosleep; then
        sleep $sleeptime
    else
        if $interactive; then
            while true; do
                read -p "Premi q per quittare la sessione, r per segnare l'aggiunta di un altro sensore " input
                if [[ "$input" == "q" ]]; then
                    break

                elif [[ "$input" == "s" ]]; then
                    echo "Aggiungo un sensore al totale"
                    nSensors=$((nSensors+1))
                    echo "Totale sensori: $nSensors"
                    echo "Totale sensori nella rete: $nSensors" >> output.csv
                else
                    echo "Input non valido. Riprova."
                fi
            done

        if [$interactive == $hastosleep]; then
            echo "Error: Interactive and Timeout conflict"
            exit 1
        fi

        fi
    fi

    # kill the python script
    for i in "${processes[@]}"; do
        if ps -p $i > /dev/null; then
            echo killando il processo: $i
            kill -INT $i 
        fi
    done

    for i in "${sshprocesses[@]}"; do
        if ps -p $i > /dev/null; then
            echo killando il processo ssh: $i
            kill -9 $i 
        fi
    done


}

if [ "$#" -eq 0 ]; then
    usage
fi

main "$@"
