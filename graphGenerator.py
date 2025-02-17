import os
import matplotlib.pyplot as plt
import numpy as np


def generateGraph(lines):
    for line in lines:
        timestamp,watt,ampere = line.split()

def main():
    
    files = os.listdir("tests")
    
    cpuS = [[],[],[],[]]
    
    # funzione che associa il numero di sensori ai watt
    
    fSensorsWatts = {}
    fSensorsAmperes= {}
    fSensorsCpu = {}
    
    for file in files:
        # apre ogni cartella
        
        print(os.listdir('tests/'+file))
        if os.path.isdir('tests/'+file) and len(os.listdir('tests/'+file)) == 3:
            # apro il file delle cpu e riempio la matrice
            with open("tests/"+file+"/cpuPower.txt") as f:
                lines = f.readlines()
                
                nSensor = 0
                
                for line in lines:
                    
                
                
            # apro il file output e salvo le misurazioni
            with open("tests/"+file+"/output.csv") as f:
                lines = f.readlines()
                watts = []
                amperes = []
                
                for line in lines:
                    day,timestamp,watt,ampere = line.split()
                    watts.append(watt)
                    amperes.append(ampere)    
                    
            print(watts)
            print(amperes)                
            # genero un subplot che abbia un grafico per le CPU, un grafico per i watt ed un altro per gli amperes
            # Crea una figura con 3 sottografi (3 rows, 1 colonna)
            fig, axs = plt.subplots(3, 1, figsize=(10, 12))

            # 1. Grafico dei Watt
            axs[0].plot(watts, label="Watt", color='blue', marker='o')
            axs[0].set_title("Consumo di Watt")
            axs[0].set_ylabel("Watt")
            axs[0].legend()
            axs[0].grid(True)

            # 2. Grafico degli Ampere
            axs[1].plot(amperes, label="Ampere", color='green', marker='x')
            axs[1].set_title("Consumo di Ampere")
            axs[1].set_ylabel("Ampere")
            axs[1].legend()
            axs[1].grid(True)

            # 3. Grafico degli Sforzi delle CPU
            for i, cpu in enumerate(cpuS):
                axs[2].plot(cpu, label=f"CPU {i+1}", marker='*')
            axs[2].set_title("Sforzo delle 4 CPU")
            axs[2].set_ylabel("Percentuale di utilizzo (%)")
            axs[2].set_xlabel("Tempo (s)")
            axs[2].legend()
            axs[2].grid(True)

            # Ottimizza la disposizione dei grafici
            plt.tight_layout()

            # Salva l'immagine
            plt.savefig("tests/"+file+"/consumo_totale.png")

            # Mostra il grafico
            plt.show()
                
                
    
    
    
    return


if __name__ == "__main__":
    main()
    