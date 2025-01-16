import serial
import matplotlib.pyplot as plt

def main():

    measurements={}

    with open('currentMeasure.csv','w') as f:
        f.write('')
    while True:
        # Open serial port and read data
        ser = serial.Serial('/dev/ttyUSB0', 9600)
        data = ser.readline().decode('utf-8').rstrip()

        datalist = data.split()

        with open('cpuPower.txt','r') as f:
            istante = f.read().strip()
        if istante == 'stop':
            break
        else:   
            # Print data
            with open('currentMeasure.csv', 'a') as file:
                file.write(istante + ', ' + datalist[1] +','+ datalist[3][1::] + '\n')
    #             if istante not in measurements:
    #                 measurements[istante] = (float(datalist[1]),float(datalist[3][1::]),1)
    #             else:
    #                 measurements[istante] = (measurements[istante][0] + float(datalist[1]) , measurements[istante][1] +float(datalist[3][1::]),measurements[istante][2]+1)

    percentualeCpu = []
    amperaggio = []
    wattaggio = []

    with open('currentMeasure.csv','r') as f:
        for line in f:
            datalist = line.split(',')
            percentualeCpu.append(float(datalist[0]))
            amperaggio.append(float(datalist[1]))
            wattaggio.append(float(datalist[2]))

    #         if datalist[0] not in measurements:
    #             measurements[datalist[0]] = (float(datalist[1]),float(datalist[2]),1)
    #         else:
    #             measurements[datalist[0]] = (measurements[datalist[0]][0] + float(datalist[1]) , measurements[datalist[0]][1] +float(datalist[2]),measurements[datalist[0]][2]+1)

    # averageM = []

    # for el in measurements:
    #     averageM.append((el,measurements[el][0]/measurements[el][2],measurements[el][1]/measurements[el][2]))

    # print(averageM)

    # percentualeCpu = [el[0] for el in averageM]
    # amperaggio = [el[1] for el in averageM]
    # wattaggio = [el[2] for el in averageM]

    # Creazione del grafico
    plt.figure(figsize=(10, 6))

    # Tracciare i dati
    plt.plot(percentualeCpu, amperaggio, label="Amperaggio (A)", marker="o", color="blue")
    plt.plot(percentualeCpu, wattaggio, label="Wattaggio (W)", marker="s", color="red")

    # Etichette e titolo
    plt.title("Andamento di Amperaggio e Wattaggio in funzione della CPU", fontsize=16)
    plt.xlabel("Percentuale di utilizzo CPU (%)", fontsize=14)
    plt.ylabel("Valori Istantanei", fontsize=14)
    plt.grid(True, linestyle="--", alpha=0.7)

    # Aggiungere una legenda
    plt.legend(fontsize=12)

    # Mostrare il grafico
    # Salva il grafico
    plt.savefig("grafico_cpu.png", dpi=300, bbox_inches="tight") 


    return


if __name__ == "__main__":
    main()
