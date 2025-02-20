import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def main():
    
    files = os.listdir("tests")
    cpuS = [[],[],[],[]]
    nSens_list = []
    vertical_lines = []           
    last_nSens = None
    timestampsCpu=[]
    timestampsMeasurements = []
    
    formato = "%Y-%m-%d %H:%M:%S.%f"
    
    
    
    for file in files:
        # apre ogni cartella
        if os.path.isdir('tests/'+file) and len(os.listdir('tests/'+file)) == 3:
            # apro il file delle cpu e riempio la matrice
            with open("tests/"+file+"/cpuPower.txt") as f:
                with open("tests/"+file+"/output.csv") as d:
                    
                    for index,line in enumerate(f):
                        now_day,now_timestamp,nSens,cpu,cpu0,cpu1,cpu2,cpu3 = line.split()
                        if index ==0:
                            start_time = datetime.strptime(now_day+" "+now_timestamp, formato)
                        now_timestamp = datetime.strptime(now_day+" "+now_timestamp, formato)
                        elapsed_time =  now_timestamp - start_time
                        timestampsCpu.append(float(elapsed_time.total_seconds())) 
                        nSens = int(nSens)
                        nSens_list.append(nSens)
                        if last_nSens is not None and nSens != last_nSens:
                            vertical_lines.append(float(elapsed_time.total_seconds()))
                        last_nSens = nSens
                        cpuS[0].append(float(cpu0))
                        cpuS[1].append(float(cpu1))
                        cpuS[2].append(float(cpu2))
                        cpuS[3].append(float(cpu3))
                    # apro il file output e salvo le misurazioni
                    watts = []
                    amperes = []
                        
                    for index,line in enumerate(d):
                        now_day,now_timestamp,watt,ampere = line.split()
                        if index ==0:
                            start_time = datetime.strptime(now_day+" "+now_timestamp, formato)
                        now_timestamp = datetime.strptime(now_day+" "+now_timestamp, formato)
                        elapsed_time =  now_timestamp - start_time
                        timestampsMeasurements.append(float(elapsed_time.total_seconds()))
                        watts.append(float(watt))
                        amperes.append(float(ampere))                  
                    # genero un subplot che abbia un grafico per le CPU, un grafico per i watt ed un altro per gli amperes
                    # Crea una figura con 3 sottografi (3 rows, 1 colonna)
                    
                    print(len(timestampsMeasurements),len(watts),len(timestampsCpu),len(cpuS[0]))
                    fig, axs = plt.subplots(3, 1, figsize=(6,6))

                    # 1. Grafico dei Watt
                    axs[0].set_ylim(0,max(watts)+1)
                    axs[0].set_xlim(0,max(timestampsMeasurements))
                    
                    axs[0].plot(timestampsMeasurements,watts, color='blue')
                    axs[0].set_title("Consumo di Watt")
                    axs[0].set_ylabel("Watt")
                    axs[0].legend()
                    axs[0].grid(True)

                    # 2. Grafico degli Ampere
                    axs[1].set_xlim(0,max(timestampsMeasurements))
                    axs[1].set_ylim(0,max(amperes)+1)
                    axs[1].plot(timestampsMeasurements,amperes,color='green')
                    axs[1].set_title("Consumo di Ampere")
                    axs[1].set_ylabel("Ampere")
                    axs[1].legend()
                    axs[1].grid(True)

                    # 3. Grafico degli Sforzi delle CPU
                    axs[2].set_xlim(0,max(timestampsCpu)+1)
                    if  cpuS[0] == []:
                        axs[2].set_ylim(0,100)
                    else:
                        axs[2].set_ylim(0,max(cpuS[0] + cpuS[1] + cpuS[2] +cpuS[3])+10)
                    for i, cpu in enumerate(cpuS):
                        axs[2].plot(timestampsCpu,cpu, label=f"CPU {i+1}")
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
    