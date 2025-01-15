import serial
import time



def main():

    # Open serial port
    ser = serial.Serial('/dev/ttyUSB0', 9600)

    off = False
    while(not off):

        # Read serial data
        data = ser.readline().decode('utf-8').strip()

        # save the data into a csv file (cpuPercentage,watt,ampere)
        with open('currentMeasure.csv', 'a') as f:
            f.write(data + '\n')

        # Check if the data is the end signal
        if data == 'end':
            off = True

    return


if __name__ == "__main__":
    main()