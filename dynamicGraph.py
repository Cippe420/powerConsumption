import matplotlib.pyplot as plt
import os
import matplotlib.animation as animation
import numpy as np
import serial
import argparse
import signal
from datetime import datetime as timer


parser = argparse.ArgumentParser()
parser.add_argument('-v' , '--visual',action='store_true',help='Visualize the data')
parser.add_argument('-o' , '--output',type=str,help='Name of the file to store the data')
parser.add_argument('-s', '--summary',type=str,help='Name of the file to store the summary')

args= parser.parse_args()
visual_mode = args.visual
output_file = args.output
summary_file = args.summary
totalWatts=[]
totalAmps=[]

starting_time = timer.now()
starting_datetime = timer.now().strftime("%Y-%m-%d_%H-%M-%S")
currentPath='tests/'+starting_datetime
os.mkdir(currentPath)
with open('cpuPower.txt','w') as f:
    pass
with open('timedcpuPower.txt','w') as f:
    pass

def signal_handler(sig,frame):
    end_time = timer.now()
    print("Exiting...") 
    summary,sx = plt.subplots(2,2)
    sx[0,0].set_xlim(0,len(watts))
    sx[0,0].set_ylim(0,20)
    sx[0,1].set_xlim(0,len(amps))
    sx[0,1].set_ylim(0,6)
    sx[0,0].plot(watts,label='wattage',color='black')
    sx[0,1].plot(amps,label='amps',color='orange')
    sx[1,0].set_ylim(0,100)
    avgCpu = []
    for i in range(4):
        if len (cpuN[i]) != 0:
            avgCpu.append(sum(cpuN[i])/len(cpuN[i]))
        else:
            avgCpu.append(0)
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

    with open(currentPath+'/'+summary_file,'w') as f: 
        f.write(f'Starting time: {starting_time}\n')
        f.write(f'Ending time: {end_time}\n')
        f.write(f'Elapsed time: {end_time-starting_time}\n')
        f.write(f'Average Wattage: {sum(totalWatts)/len(totalWatts)}\n')
        f.write(f'Average Amperes: {sum(totalAmps)/len(totalAmps)}\n')
        for i in range(4):
            if len (cpuN[i]) != 0:
                f.write(f'Average CPU {i} Power: {sum(cpuN[i])/len(cpuN[i])}\n')
            else:
                f.write(f'Average CPU {i} Power: 0\n')
    with open('timedcpuPower.txt','r') as f:
        with open(currentPath+'/cpuPower.txt','w') as f2:
            f2.write(f.read())
    exit(0)
    
signal.signal(signal.SIGINT,signal_handler)

time = list(range(100)) 
watts = [0 for _ in time] 
amps = [0 for _ in time]  
cpuN = [[0 for _ in time] for _ in range(4)] 
lastSeenCpu = [0 for _ in range(4)] 
serial_port = serial.Serial('/dev/ttyUSB0', 9600)
last_nSens= None
vertical_lines=[]
nSens_list=[]

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
    # read the serial values of watts and amperes
    sLine = serial_port.readline().decode('utf-8')
    # get the current timestamp
    now = timer.now()
    if sLine != '':
        new_amp = sLine.split()[1]
        new_watt = sLine.split()[3][1:]
        
    with open('cpuPower.txt','r') as f:
        # read the last cpu values from file
        with open(currentPath+ '/'+output_file, 'a') as d:
            
            content = f.readlines()
            if content != []:

                nSens,cpu,cpu0,cpu1,cpu2,cpu3 = content[-1].split()
            
                with open('timedcpuPower.txt','a') as f2:
                    f2.write(f'{now} {nSens} {cpu} {cpu0} {cpu1} {cpu2} {cpu3}\n')

                cpuN[0].append(float(cpu0))
                cpuN[1].append(float(cpu1))
                cpuN[2].append(float(cpu2))
                cpuN[3].append(float(cpu3))
                lastSeen= [cpuN[i][-1] for i in range(4)]
                for bar, value in zip(bars, lastSeen):
                    bar.set_height(value)
                    
            watts.append(float(new_watt))
            amps.append(float(new_amp))
            totalWatts.append(float(new_watt))
            totalAmps.append(float(new_amp))

            # if len(watts) > 100:
            #     watts.pop(0)
            #     amps.pop(0)
            line1.set_ydata(watts[-100:])
            line2.set_ydata(amps[-100:])
            
            d.write(f'{now} {new_watt} {new_amp}\n')
                
    return line1, line2, bars


if visual_mode:
    ani = animation.FuncAnimation(fig, update, frames=100, interval=100, blit=False)
    plt.show()

        
