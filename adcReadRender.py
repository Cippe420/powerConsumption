import socket
import matplotlib.pyplot as plt
import re
import os
import csv
from datetime import datetime
import time

# Parametri connessione TCP
HOST = "10.71.214.12"  # IP del Raspberry o del server
PORT = 12345  # Porta del servizio TCP

DURATA = 100  # secondi di raccolta dati

# Liste per accumulare i valori
corrente = []
potenza = []

# Regex per estrarre corrente e potenza
pattern = re.compile(r"Current:\s*([\d.]+)\s*A,\s*Power:\s*([\d.]+)\s*W")


def ricevi_valori(durata=DURATA):
    """Riceve valori dal socket per 'durata' secondi"""
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
                # nessun dato disponibile
                pass
    finally:
        s.close()


# --- MAIN ---
ricevi_valori()

# Creazione cartella summary con timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
cartella = f"summary_{timestamp}"
os.makedirs(cartella, exist_ok=True)

# Salvataggio CSV con i valori
csv_path = os.path.join(cartella, "dati.csv")
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Corrente (A)", "Potenza (W)"])
    for c, p in zip(corrente, potenza):
        writer.writerow([c, p])

# Grafico linea corrente
plt.figure(figsize=(8, 4))
plt.plot(corrente, label="Corrente (A)", color="blue")
plt.title("Andamento Corrente")
plt.xlabel("Campioni")
plt.ylabel("Ampere (A)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(cartella, "corrente_line.png"), dpi=150)
plt.close()

# Grafico linea potenza
plt.figure(figsize=(8, 4))
plt.plot(potenza, label="Potenza (W)", color="green")
plt.title("Andamento Potenza")
plt.xlabel("Campioni")
plt.ylabel("Watt (W)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(cartella, "potenza_line.png"), dpi=150)
plt.close()

print(f"Dati raccolti: {len(corrente)} campioni")
print(f"Risultati salvati in cartella: {cartella}")
