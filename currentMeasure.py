import serial
import matplotlib.pyplot as plt
import numpy as np

with open('currentMeasure.csv','r') as f:
    data = f.readlines()

data = [x.strip() for x in data]

#print(data)

amps = []
watts = [0 for i in range(100)]

fig = plt.figure()
ax = fig.add_subplot(111)
plt.ylim([0,20])
plt.xlim([0,100])

line, =ax.plot(watts)

ax.set_title('Power Consumption')
ax.set_xlabel('Time')
ax.set_ylabel('Power (W)')

serial_port = serial.Serial('/dev/ttyUSB0', 9600)

while True:
    try:
        sLine = serial_port.readline().decode('utf-8')
        new_value = sLine.split()[3][1:]
        watts.append(float(new_value))
        if len(watts) > 100:
            watts = watts[-100:]

        line.set_ydata(watts)
        line.set_xdata(np.arange(len(watts)))
        fig.canvas.draw_idle()
        plt.pause(0.1)
    except KeyboardInterrupt:
        break
    