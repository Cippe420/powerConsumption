import time
import sqlite3

def parse_cpu_times(lines):
    """Parsa i tempi della CPU dalla lista delle righe."""
    cpu_times = {}
    for line in lines:
        parts = line.split()
        if parts[0].startswith("cpu"):  
            cpu_name = parts[0]
            cpu_times[cpu_name] = list(map(int, parts[1:]))
    return cpu_times

def calculate_cpu_usage(prev, curr):
    """Calcola la percentuale di utilizzo della CPU."""
    usage = {}
    for cpu_name in curr.keys():
        if cpu_name not in prev:
            continue 

        prev_idle = prev[cpu_name][3] + prev[cpu_name][4]
        curr_idle = curr[cpu_name][3] + curr[cpu_name][4]

        prev_total = sum(prev[cpu_name])
        curr_total = sum(curr[cpu_name])

        total_diff = curr_total - prev_total
        idle_diff = curr_idle - prev_idle

        usage[cpu_name] = (total_diff - idle_diff) / total_diff * 100 if total_diff > 0 else 0
    return usage

def read_cpu_times():
    """Legge i dati delle CPU da /proc/stat."""
    with open("/proc/stat", "r") as file:
        lines = file.readlines()
    return parse_cpu_times(lines)

def main():
    prev_cpu_times = read_cpu_times()
    if not prev_cpu_times:
        return

    while True:
        time.sleep(1)  
        curr_cpu_times = read_cpu_times()
        if not curr_cpu_times:
            return
        usage = calculate_cpu_usage(prev_cpu_times, curr_cpu_times)
        
        with sqlite3.connect("/home/pi/coap.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sensors")
            count = cursor.fetchone()[0]
        prev_cpu_times = curr_cpu_times
        # stampa l'utilizzo delle cpu ed il numero di sensori che compongono la rete
        
        line = ''
        line += '{count} '
        for cpu, percent in usage.items():
            line += (f" {percent:.2f}")
            
        print(line)
        

if __name__ == "__main__":
    main()
