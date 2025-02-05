import subprocess
from time import sleep

def getSysAmps():
    
    sysAmps={}

    vcgen = subprocess.run(['vcgencmd pmic_read_adc'], shell=True, capture_output=True , text=True)

    values = [i for i in vcgen.stdout.split('\n') if i != '']

    for i in range(len(values)):
        k,v = values[i].split()


        # clean key,values from useless chars
        if k[:-2] not in sysAmps:
            sysAmps[k[:-2]] = [v.split('=')[1]]

        else:
            sysAmps[k[:-2]] += [v.split('=')[1]]

    # add wattage data for each component

    for k,v in sysAmps.items():
        if len(v)>1:
            wattage = float(v[0][:-1]) *float(v[1][:-1])
            v.append(str(wattage) + 'W')

    return sysAmps


def main():

    
    while True:
        try:
            sysValues= getSysAmps()
            totalWattage = [float(v[2][:-1]) for k,v in sysValues.items() if len(v) > 1] 
       
            sleep(1) 
            
            print(f'{sum(totalWattage):.4f}',end='\r',flush=True)

        except KeyboardInterrupt:
    
            break

    return


if __name__ == '__main__':
    main()

