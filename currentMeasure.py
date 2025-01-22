import serial
import matplotlib.pyplot as plt
import numpy as np
import argparse
import signal

parser = argparse.ArgumentParser()
parser.add_argument('-v' , '--visual',action='store_true',help='Visualize the data')
parser.add_argument('-o' , '--output',type=str,help='Name of the file to store the data')
parser.add_argument('-s', '--summary',type=str,help='Name of the file to store the summary')

args= parser.parse_args()
visual_mode = args.visual
output_file = args.output
summary_file = args.summary

plt.tight_layout()

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

amps = [0 for i in range(100)]
watts = [0 for i in range(100)]
cpuN = [[0 for i in range(100)] for i in range(4)]
lastSeenCpu = [cpuN[i][-1] for i in range(4)]
x = np.arange(100)

if visual_mode:
    fig,ax = plt.subplots(2,2)
    ax[0,0].set_xlim(0,100)
    ax[0,0].set_ylim(0,20)
    ax[0,1].set_xlim(0,100)
    ax[0,1].set_ylim(0,6)
    ax[0,0].set_title('Wattage')
    ax[0,0].set_xlabel('Time')
    ax[0,0].set_ylabel('Power (W)')
    ax[0,1].set_title('Amperes')
    ax[0,1].set_xlabel('Time')
    ax[0,1].set_ylabel('Current (A)')
    ax[1,0].set_title('Cpu Power')
    ax[1,0].set_xlabel('Time')
    ax[1,0].set_ylabel('%')
    ax[1,0].set_ylim(0,100)
    line, =ax[0,0].plot(watts,label='wattage',color='black')
    lin2, = ax[0,1].plot(amps,label='amps',color='orange')
    labels = ['Cpu 0', 'Cpu 1', 'Cpu 2', 'Cpu 3']
    bars = ax[1,0].bar(labels, lastSeenCpu, color='red')
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.3, hspace=0.5)
    plt.legend()

memWatt = 0
memAmps = 0
nValues = 0

pastWatts=[]
pastAmps=[]
pastcpuPower=[]

serial_port = serial.Serial('/dev/ttyUSB0', 9600)
while True:
    try:
        
        
        sLine = serial_port.readline().decode('utf-8')
        nValues += 1
        
        
        with open('cpuPower.txt','r') as f:
            riga = f.readlines()[-4:]
            for i in range(len(riga)):
                cpuN[i].append(float(riga[i].split()[1][0:-1]))
                lastSeenCpu = [cpuN[i][-1] for i in range(4)]
                
                
        new_amps = sLine.split()[1]
        new_watts = sLine.split()[3][1:]
        amps.append(float(new_amps))
        watts.append(float(new_watts))
        
        
        if output_file != None:
            with open(output_file,'a') as f:
                f.write('' + str(new_amps) + ' A ' + str(new_watts) +' W ' + '\n')
                
                
        memWatt += float(new_watts)
        memAmps += float(new_amps)

        if visual_mode:
            lin2.set_ydata(amps[-100:])
            lin2.set_xdata(np.arange(len(amps[-100:])))
            line.set_ydata(watts[-100:])
            line.set_xdata(np.arange(len(watts[-100:])))
            for bar, b in zip(bars, lastSeenCpu):
                bar.set_height(b)
            fig.canvas.draw_idle()
            plt.pause(0.1)

    except KeyboardInterrupt:
        if summary_file != None:
            with open(summary_file,'w') as f:
                f.write('Average Current: ' + str(memAmps/nValues) + ' A\n')
                f.write('Average Power: ' + str(memWatt/nValues) + ' W\n')

        break
    


