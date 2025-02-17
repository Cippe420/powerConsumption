import os
import matplotlib.pyplot as plt
import numpy as np

def main():
    
    files = os.listdir("tests")
    
    cpuS = [[],[],[],[]]
    nSens_list = []
    vertical_lines = []           
    last_nSens = None
    
    for file in files:
        # apre ogni cartella
        if os.path.isdir('tests/'+file) and len(os.listdir('tests/'+file)) == 3:
            # apro il file delle cpu e riempio la matrice
            with open("tests/"+file+"/cpuPower.txt") as f:
                for index,line in enumerate(f):
                    if "nSens" in line:
                        nSens = int(line.strip().split(":")[1])
                        nSens_list.append(nSens)
                        if last_nSens is not None and nSens != last_nSens:
                            vertical_lines.append(index // 6)
                        last_nSens = nSens
                    elif "cpu0" in line:
                        cpuS[0].append(float(line.strip().split(":")[1]))
                    elif "cpu1" in line:
                            cpuS[1].append(float(line.strip().split(":")[1]))
                    elif "cpu2" in line:
                            cpuS[2].append(float(line.strip().split(":")[1]))
                    elif "cpu3" in line:
                            cpuS[3].append(float(line.strip().split(":")[1]))                
                # apro il file output e salvo le misurazioni
                with open("tests/"+file+"/output.csv") as d:
                    lines = d.readlines()
                    watts = []
                    amperes = []
                    
                    for line in lines:
                        day,timestamp,watt,ampere = line.split()
                        watts.append(float(watt))
                        amperes.append(float(ampere))                  
                # genero un subplot che abbia un grafico per le CPU, un grafico per i watt ed un altro per gli amperes
                # Crea una figura con 3 sottografi (3 rows, 1 colonna)
                fig, axs = plt.subplots(3, 1, figsize=(12, 8))

                # 1. Grafico dei Watt
                axs[0].set_ylim(0,max(watts)+1)
                axs[0].set_xlim(0,len(watts))
                
                axs[0].plot(watts, label="Watt", color='blue', marker='o')
                axs[0].set_title("Consumo di Watt")
                axs[0].set_ylabel("Watt")
                axs[0].legend()
                axs[0].grid(True)

                # 2. Grafico degli Ampere
                axs[0].set_xlim(0,len(amperes))
                axs[1].set_ylim(0,max(amperes)+1)
                axs[1].plot(amperes, label="Ampere", color='green', marker='x')
                axs[1].set_title("Consumo di Ampere")
                axs[1].set_ylabel("Ampere")
                axs[1].legend()
                axs[1].grid(True)

                # 3. Grafico degli Sforzi delle CPU
                axs[2].set_xlim(0,len(cpuS[0]))
                if  cpuS[0] == []:
                    axs[2].set_ylim(0,100)
                else:
                    axs[2].set_ylim(0,max(cpuS[0] + cpuS[1] + cpuS[2] +cpuS[3])+10)
                for i, cpu in enumerate(cpuS):
                    axs[2].plot(cpu, label=f"CPU {i+1}", marker='*')
                axs[2].set_title("Sforzo delle 4 CPU")
                axs[2].set_ylabel("Percentuale di utilizzo (%)")
                axs[2].set_xlabel("Tempo (s)")
                axs[2].legend()
                axs[2].grid(True)
                
                for ax in axs:
                    for line_x in vertical_lines:
                        ax.axvline(x=line_x, color='red', linestyle='--', linewidth=1)

                # Ottimizza la disposizione dei grafici
                plt.tight_layout()

                # Salva l'immagine
                plt.savefig("tests/"+file+"/consumo_totale.png")
                
                plt.close()
                    
        
        
    
    return


if __name__ == "__main__":
    main()
    