#!/bin/bash
main()
{
    processes=()
    rm cpuPower.txt
    touch cpuPower.txt

    python3 dynamicGraph.py -o out.csv -s summary.csv -v &
    # args are the ip address of the remote machine

    processes+=($!)

    ssh $1 'python3 -u powerConsumption/pwr.py' >> cpuPower.txt &
    processes+=($!)
    # wait on input
    for i in "${processes[@]}"; do
        echo runnando in background il processo : $i
    done

    while true; do
        read -p "Premi q per quittare la sessione " input
        if [[ "$input" == "q" ]]; then
            break
        else
            echo "Input non valido. Riprova."
        fi
    done
    # kill the python script
    for i in "${processes[@]}"; do
        if ps -p $i > /dev/null; then
            echo killando il processo: $i
            kill -9 $i
        fi
    done

}
main $1
