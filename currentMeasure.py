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
                if istante not in measurements:
                    measurements[istante] = (float(datalist[1]),float(datalist[3][1::]),1)
                else:
                    measurements[istante] = (measurements[istante][0] + float(datalist[1]) , measurements[istante][1] +float(datalist[3][1::]),measurements[istante][2]+1)

    averageM = []

    for el in measurements:
        averageM.append((el,measurements[el][0]/measurements[el][2],measurements[el][1]/measurements[el][2]))

    print(averageM)

    return


if __name__ == "__main__":
    main()
