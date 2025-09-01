import socket
import matplotlib.pyplot as plt
import re
import os
import csv
from datetime import datetime
import time
import paramiko
import numpy as np

# Parametri connessione TCP
HOST = "10.71.214.12"  # IP del Raspberry o del server
PORT = 12345  # Porta del servizio TCP

# Parametri SSH per cambiare governor
RPI_HOST = "10.71.214.12"
RPI_USER = "pi"
RPI_PASS = "raspberry"

# Profiling settings
DURATA = 10  # secondi di raccolta dati per governor
GOVERNORS = [
    "performance",
    "ondemand",
    "powersave",
    "schedutil",
    "userspace",
    "conservative",
]

# Regex per estrarre corrente e potenza
pattern = re.compile(r"Current:\s*([\d.]+)\s*A,\s*Power:\s*([\d.]+)\s*W")


# --- Funzione SSH ---
def set_governor(governor):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(RPI_HOST, username=RPI_USER, password=RPI_PASS)
    cmd = f"echo {governor} | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
    ssh.exec_command(cmd)
    ssh.close()


# --- Funzione raccolta ---
def ricevi_valori(durata=DURATA):
    corrente, potenza = [], []
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.settimeout(1.0)
    s.setblocking(False)

    start = time.time()
    try:
        while time.time() - start < durata:
            try:
                data = s.recv(1024)
                if not data:
                    break
                for line in data.decode().strip().split("\n"):
                    match = pattern.match(line.strip())
                    if match:
                        corrente.append(float(match.group(1)))
                        potenza.append(float(match.group(2)))
            except BlockingIOError:
                pass
    finally:
        s.close()

    return corrente, potenza


# --- MAIN ---
def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cartella = f"summary_{timestamp}"
    os.makedirs(cartella, exist_ok=True)

    results = {}

    for gov in GOVERNORS:
        print(f"[INFO] Cambio governor a {gov}...")
        set_governor(gov)
        time.sleep(2)

        print(f"[INFO] Raccolgo dati per {DURATA} secondi...")
        corrente, potenza = ricevi_valori(DURATA)
        results[gov] = {"corrente": corrente, "potenza": potenza}

        # Salvataggio CSV singolo governor
        csv_path = os.path.join(cartella, f"dati_{gov}.csv")
        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Corrente (A)", "Potenza (W)"])
            for c, p in zip(corrente, potenza):
                writer.writerow([c, p])

    # --- Analisi finale e grafico comparativo ---
    means = [np.mean(results[gov]["potenza"]) for gov in GOVERNORS]
    stderr = [
        np.std(results[gov]["potenza"]) / np.sqrt(len(results[gov]["potenza"]))
        for gov in GOVERNORS
    ]

    plt.figure(figsize=(8, 5))
    plt.bar(GOVERNORS, means, yerr=stderr, capsize=5, alpha=0.7)
    plt.ylabel("Potenza media (W)")
    plt.title("Confronto Governor CPU - Potenza Media")
    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(cartella, "confronto_governor.png"), dpi=150)
    plt.close()

    print(f"Profiling completato. Risultati salvati in: {cartella}")


if __name__ == "__main__":
    main()
