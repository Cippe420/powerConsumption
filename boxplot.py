import matplotlib.pyplot as plt
import argparse
import numpy as np
from datetime import datetime as timer

parser = argparse.ArgumentParser()
parser.add_argument('-f1','--filename1',type=str,help='name of the first file')
parser.add_argument('-f2','--filename2',type=str,help='name of the second file')

now = timer.now().strftime("%Y-%m-%d_%H-%M-%S")

args= parser.parse_args()
filename1=args.filename1
filename2=args.filename2
def leggi_dati(file_path):
    watts,ampere = [],[]

    with open(file_path, 'r') as f:
        data = f.readlines()
        watts = [float(el.split()[3]) for el in data]
        amperes = [float(el.split()[4]) for el in data]

    return watts,amperes
def main():

    # Estrarre i valori per il boxplot (scegli "watt" o "ampere")
    watts1,amperes1 = leggi_dati(filename1)
    print('watts1 ',watts1)
    print('amperes1 ', amperes1)
    watts2,amperes2 = leggi_dati(filename2)
    print('watts2 ', watts2)
    print('amperes2 ', amperes2)
    mediaWatt1 = np.mean(watts1)
    mediaWatt2 = np.mean(watts2)
    deviazione_standard_watts1 = np.std(watts1,ddof=1)
    deviazione_standard_watts2 = np.std(watts2,ddof=1)

    print(mediaWatt1,mediaWatt2,deviazione_standard_watts1,deviazione_standard_watts2)
    # Creare il boxplot
    plt.figure(figsize=(8, 6))
    plt.boxplot([watts1, watts2], tick_labels=["Baseline", "Low-power"])
    plt.ylabel("Watt")
    plt.grid(True)
    
    plt.savefig(f'boxplot{now}.png')
    
    return



if __name__ == '__main__':
    main()
