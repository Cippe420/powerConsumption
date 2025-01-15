import serial
import datetime

def main():
    with open('currentMeasure.csv','w') as f:
        f.write('')
    while True:
        # Open serial port and read data
        ser = serial.Serial('/dev/ttyUSB0', 9600)
        data = ser.readline().decode('utf-8').rstrip()
        with open('cpuPower.txt','r') as f:
            istante = f.read().strip()
        if istante == 'stop':
            break
        else:   
            # Print data
            with open('currentMeasure.csv', 'a') as file:
                file.write(istante + ', ' + data + '\n')
    return


if __name__ == "__main__":
    main()
