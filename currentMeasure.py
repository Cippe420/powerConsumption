import serial
import datetime

def main():

    try:
        while True:
            istante = datetime.datetime.now()
            # Open serial port and read data
            ser = serial.Serial('/dev/ttyUSB0', 9600)
            data = ser.readline().decode('utf-8').rstrip()
            # Print data
            with open('currentMeasure.csv', 'a') as file:
                file.write(str(istante) + ',' + data + '\n')
    except KeyboardInterrupt:
        ser.close()

    return


if __name__ == "__main__":
    main()