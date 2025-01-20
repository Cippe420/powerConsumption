import serial
import matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-v' , '--visual',action='store_true',help='Visualize the data')
parser.add_argument('-o' , '--output',type=str,help='Name of the file to store the data')
parser.add_argument('-s', '--summary',type=str,help='Name of the file to store the summary')

args= parser.parse_args()
visual_mode = args.visual
output_file = args.output
summary_file = args.summary

amps = [0 for i in range(100)]
watts = [0 for i in range(100)]

summary = plt.figure()
sx = summary.add_subplot(111)
sx.set_title('Summary')
sx.set_xlabel('Time')
sx.set_ylabel('Power (W)')


if visual_mode:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.ylim([0,20])
    plt.xlim([0,100])
    line, =ax.plot(watts,label='wattage')
    lin2, = ax.plot(amps,label='amps')
    plt.legend()
    ax.set_title('Power Consumption')
    ax.set_xlabel('Time')
    ax.set_ylabel('Power (W)')

memWatt = 0
memAmps = 0
nValues = 0

serial_port = serial.Serial('/dev/ttyUSB0', 9600)
while True:
    try:
        sLine = serial_port.readline().decode('utf-8')
        nValues += 1
        new_amps = sLine.split()[1]
        new_watts = sLine.split()[3][1:]
        amps.append(float(new_amps))
        watts.append(float(new_watts))
        watts = watts[-100:]
        amps = amps[-100:]
        if output_file != None:
            with open(output_file,'a') as f:
                f.write('' + str(new_amps) + ' A ' + str(new_watts) +' W ' + '\n')
        memWatt += float(new_watts)
        memAmps += float(new_amps)

        if visual_mode:
            lin2.set_ydata(amps)
            lin2.set_xdata(np.arange(len(amps)))
            line.set_ydata(watts)
            line.set_xdata(np.arange(len(watts)))
            fig.canvas.draw_idle()
            plt.pause(0.1)

    except KeyboardInterrupt:
        if summary_file != None:
            with open(summary_file,'w') as f:
                f.write('Average Current: ' + str(memAmps/nValues) + ' A\n')
                f.write('Average Power: ' + str(memWatt/nValues) + ' W\n')
        break

if visual_mode:
    sWatt = sx.plot(memWatt, label='Wattage')
    sAmps = sx.plot(memAmps, label='Amps')
    sx.legend()
    plt.savefig('summary.png')



        