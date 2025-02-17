import matplotlib.pyplot as plt

# Funzione per leggere i dati dal file
def leggi_file(path):
    cpu_loads = [[], [], [], []]  # Lista per i 4 sforzi delle CPU
    nSens_list = []               # Lista per nSens
    vertical_lines = []           # Posizioni in cui cambia nSens
    last_nSens = None

    with open(path, 'r') as f:
        for index, line in enumerate(f):
            if "nSens" in line:
                nSens = int(line.strip().split(":")[1])
                nSens_list.append(nSens)
                # Segna il punto se nSens cambia
                if last_nSens is not None and nSens != last_nSens:
                    vertical_lines.append(index // 6)
                last_nSens = nSens
            elif "cpu0" in line:
                cpu_loads[0].append(float(line.strip().split(":")[1]))
            elif "cpu1" in line:
                cpu_loads[1].append(float(line.strip().split(":")[1]))
            elif "cpu2" in line:
                cpu_loads[2].append(float(line.strip().split(":")[1]))
            elif "cpu3" in line:
                cpu_loads[3].append(float(line.strip().split(":")[1]))

    return cpu_loads, nSens_list, vertical_lines

# Leggi il file e ottieni i dati
file_path = "tests/2025-02-17_17-25-36/cpuPower.txt"  # Sostituisci con il percorso del tuo file
cpu_loads, nSens_list, vertical_lines = leggi_file(file_path)

# Crea il grafico
plt.figure(figsize=(12, 8))

# Plotta le 4 CPU
for i, cpu in enumerate(cpu_loads):
    plt.plot(cpu, label=f"CPU {i}")

# Aggiungi le linee verticali dove nSens cambia
for line_x in vertical_lines:
    plt.axvline(x=line_x, color='red', linestyle='--', linewidth=1)

plt.title("Sforzo CPU e cambiamenti di nSens")
plt.xlabel("Tempo (campioni)")
plt.ylabel("Sforzo CPU (%)")
plt.legend()
plt.grid(True)

# Salva e mostra il grafico
plt.savefig("output.png")
plt.show()