import matplotlib.pyplot as plt
import argparse
from datetime import datetime as timer

import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-f1','--filename1',type=str,help='name of the file')


now = timer.now().strftime('%Y-%m-%d_%H-%M-%S')
args = parser.parse_args()
filename= args.filename1

def leggi_dati(filename):
    datatableWatts={}
    datatableAmperes = {}
    with open(filename,'r') as f:
        data = f.readlines()

        for lines in data:
            line = lines.split()
            if line[0] in datatableWatts.keys():
                datatableWatts[line[0]].append(line[3])
            else:
                datatableWatts[line[0]] = [line[3]]
            if line[0] in datatableAmperes.keys():
                datatableAmperes[line[0]].append(line[4])
            else:
                datatableAmperes[line[0]] = [line[4]]
    
        # ho creato due dizionari, uno con i watt per ogni nSens, l'altro con gli amperes per ogni nSens
    return datatableWatts,datatableAmperes

def main():

    dati_watt,dati_ampere = leggi_dati(filename)

    # Convertire i valori da stringhe a float
    dati_watt = {int(k): list(map(float, v)) for k, v in dati_watt.items()}

    # Ordinare i dati per numero di sensori
    dati_watt = dict(sorted(dati_watt.items()))

    means = []

    for el in dati_watt.values():
        media = np.mean(el)
        means.append(media)
        deviazione_std=np.std(el,ddof=1)
        print('deviazione : ',deviazione_std)
    for el in means:
        print(el)



    # Estrarre etichette e valori per il boxplot
    etichette = list(dati_watt.keys())
    valori = list(dati_watt.values())

    # Creare il boxplot
    plt.figure(figsize=(8, 6))
    plt.boxplot(valori, tick_labels=etichette)
    plt.xlabel("Numero di sensori")
    plt.ylabel("Watt consumati")
    plt.title("Distribuzione dei consumi in base al numero di sensori")
    plt.grid(True)

    plt.savefig('growingbox.png')
    return

if __name__=='__main__':
    main()
