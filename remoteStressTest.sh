#!/bin/bash
processes=()
main()
{
    rm cpuPower.txt
    touch cpuPower.txt
    python3 dynamicGraph.py -o out.csv -s summary.csv -v &
    processes+=($!)
    ssh pi@raspberrypi42.local 'python3 -u powerConsumption/pwr.py' >> cpuPower.txt &
    processes+=($!)
    # wait on input
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
        kill $i
    done

}

main
