import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import serial
import argparse
import signal

with open('cpuPower.txt','w') as f:
    pass

parser = argparse.ArgumentParser()
parser.add_argument('-v' , '--visual',action='store_true',help='Visualize the data')
parser.add_argument('-o' , '--output',type=str,help='Name of the file to store the data')
parser.add_argument('-s', '--summary',type=str,help='Name of the file to store the summary')

args= parser.parse_args()
visual_mode = args.visual
output_file = args.output
summary_file = args.summary

def signal_handler(sig,frame):
    summary,sx = plt.subplots(2,2)
    sx[0,0].set_xlim(0,len(watts))
    sx[0,0].set_ylim(0,20)
    sx[0,1].set_xlim(0,len(amps))
    sx[0,1].set_ylim(0,6)
    sx[0,0].plot(watts,label='wattage',color='black')
    sx[0,1].plot(amps,label='amps',color='orange')
    sx[1,0].set_ylim(0,100)
    avgCpu = [sum(cpuN[i])/len(cpuN[i]) for i in range(4)]
    sx[1,0].bar(labels, avgCpu, color='red')
    sx[0,0].set_title('Wattage')
    sx[0,0].set_xlabel('Time')
    sx[0,0].set_ylabel('Power (W)')
    sx[0,1].set_title('Amperes')
    sx[0,1].set_xlabel('Time')
    sx[0,1].set_ylabel('Current (A)')
    sx[1,0].set_title('Cpu Power')
    sx[1,0].set_xlabel('Time')
    sx[1,0].set_ylabel('%')
    plt.legend()
    plt.savefig('summary.png')
    exit(0)
    
signal.signal(signal.SIGINT,signal_handler)

time = list(range(100)) 
watts = [0 for _ in time] 
amps = [0 for _ in time]  
cpuN = [[0 for _ in time] for _ in range(4)] 
lastSeenCpu = [0 for _ in range(4)] 
serial_port = serial.Serial('/dev/ttyUSB0', 9600)

# configurazione iniziale del grafico
fig, ax = plt.subplots(2, 2, figsize=(10, 8))
ax[0, 0].set_xlim(0, 100)
ax[0, 0].set_ylim(0, 10)
ax[0, 1].set_xlim(0, 100)
ax[0, 1].set_ylim(0, 4)
ax[0, 0].set_title('Wattage')
ax[0, 0].set_xlabel('Time')
ax[0, 0].set_ylabel('Power (W)')
ax[0, 1].set_title('Amperes')
ax[0, 1].set_xlabel('Time')
ax[0, 1].set_ylabel('Current (A)')
ax[1, 0].set_title('CPU Power')
ax[1, 0].set_xlabel('CPU')
ax[1, 0].set_ylabel('%')
ax[1, 0].set_ylim(0, 100)

line1, = ax[0, 0].plot(time, watts, label='Wattage', color='black')
line2, = ax[0, 1].plot(time, amps, label='Amps', color='orange')
labels = ['CPU 0', 'CPU 1', 'CPU 2', 'CPU 3']
bars = ax[1, 0].bar(labels, lastSeenCpu, color='red')

plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.3, hspace=0.5)
ax[0, 0].legend()
ax[0, 1].legend()

def update(frame):
    
    sLine = serial_port.readline().decode('utf-8')
    new_amp = sLine.split()[1]
    new_watt = sLine.split()[3][1:]
    with open('cpuPower.txt','r') as f:
        riga = f.readlines()[-4:]
        for i in range(len(riga)):
            cpuN[i].append(float(riga[i].split()[1][0:-1]))
            lastSeen = [cpuN[i][-1] for i in range(4)]        
    watts.append(new_watt)
    amps.append(new_amp)
    if len(watts) > 100:
        watts.pop(0)
        amps.pop(0)
    line1.set_ydata(watts)
    line2.set_ydata(amps)

    for bar, value in zip(bars, lastSeen):
        bar.set_height(value)
    
    return line1, line2, bars


if visual_mode:
    ani = animation.FuncAnimation(fig, update, frames=100, interval=100, blit=False)
    plt.show()
            




