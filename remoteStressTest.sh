#!/bin/bash
main()
{

    hastosleep=false
    interactive=false
    processes=()
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
                echo "Invalid option: $OPTARG" 1>&2
                ;;
        esac
    done

    ssh $sshmachine 'python3 -u powerConsumption/pwr.py' >> cpuPower.txt &
    processes+=($!)

    python3 dynamicGraph.py -o out.csv -s summary.csv -v &
    # args are the ip address of the remote machine
    processes+=($!)

    # wait on input
    for i in "${processes[@]}"; do
        echo runnando in background il processo : $i
    done

    if $hastosleep; then
        sleep $sleeptime
    else
        if $interactive; then
            while true; do
                read -p "Premi q per quittare la sessione " input
                if [[ "$input" == "q" ]]; then
                    break
                else
                    echo "Input non valido. Riprova."
                fi
            done
        
        fi
    fi

    # kill the python script
    for i in "${processes[@]}"; do
        if ps -p $i > /dev/null; then
            echo killando il processo: $i
            kill -9 $i 
        fi
    done

}

main "$@"
