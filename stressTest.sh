#!/bin/bash

# Nome del file di log
LOGFILE="stress_test.log"

# Durata del test in secondi
TEST_DURATION=180

# Intervallo di logging (in secondi)
LOG_INTERVAL=5

# Percentuale di stress
STRESS_PERCENTAGE=15

start_stress_test() {
    echo "Inizio stress test: $(date)" | tee -a "$LOGFILE"

    # Esegui stress test su CPU, RAM e I/O in background
    stress-ng --cpu 4 --vm 2 --vm-bytes $STRESS_PERCENTAGE% --hdd 2 --hdd-bytes 2G --timeout "$TEST_DURATION" &
    STRESS_PID=$! # Salva il PID del processo
    STRESS_PERCENTAGE+=20
    echo "Stress test avviato con PID $STRESS_PID e percentuale $STRESS_PERCENTAGE" | tee -a "$LOGFILE"
}

log_system_stats() {
    echo "-----------------------------" >> "$LOGFILE"
    echo "Timestamp: $(date)" >> "$LOGFILE"

    # Temperatura
    TEMP=$(vcgencmd measure_temp | awk -F'=' '{print $2}')
    echo "Temperatura: $TEMP" >> "$LOGFILE"

    # Frequenza CPU
    CPU_FREQ=$(vcgencmd measure_clock arm | awk -F'=' '{print $2}')
    echo "Frequenza CPU: $((CPU_FREQ / 1000000)) MHz" >> "$LOGFILE"

    # Stato del throttling
    THROTTLED=$(vcgencmd get_throttled | awk -F'=' '{print $2}')
    echo "Throttled: $THROTTLED" >> "$LOGFILE"

    echo "-----------------------------" >> "$LOGFILE"
}

# Funzione principale per avviare il logging
main() {

    sudo ifconfig wlan0 down

    start_stress_test

    # Loop per registrare i dati ogni LOG_INTERVAL secondi
    END_TIME=$((SECONDS + TEST_DURATION))
    while [ $SECONDS -lt $END_TIME ]; do
        log_system_stats
        sleep "$LOG_INTERVAL"
    done

    # Attendi il completamento dello stress test
    wait $STRESS_PID

    # stress al 35%
    start_stress_test
    wait $STRESS_PID

    # stress al 55%
    start_stress_test

    wait $STRESS_PID
    # stress al 75%
    start_stress_test
    wait $STRESS_PID



    echo "Stress test completato: $(date)" | tee -a "$LOGFILE"

    sudo ifconfig wlan0 up
}

# Esegui lo script principale
main
