import socket
import select

def TRNG_ESP32(size):
    HOST = '192.168.0.14'   # ESP32 IP in local network
    PORT = 80               # ESP32 server port
    TIMEOUT_RCV = 5         # timeout waiting for receive data (s)
    TIMEOUT_CON = 5         # timeout waiting for connection with server
    POW32 = 2**32-1         # max. integer from 32bit noise server
    BUFFER = 1024           # receive data buffer size
    if(type(size)==str):
        return []
    else: # ensures that size is a positive int
        size = abs(int(size))
        None
    s = socket.socket()     # instantiate web socket
    s.settimeout(TIMEOUT_CON)
    try: 
        s.connect((HOST, PORT)) # connect with ESP32
    except:
        print('Timeout: cannot connect to server!')
        return []
    s.sendall(bytes(str(size),'utf-8')) # send size as byte composed string
    dataString = "" # initialize string of incoming data
    while True: # while still receiving data
        dataString += s.recv(BUFFER).decode('utf-8') # concat. input buffer data as string 
        ready = select.select([s], [], [], TIMEOUT_RCV) # test if there is data reaching input buffer
        if not ready[0]:
            break
    s.close() # close connection with ESP32
    data = list(map(int, dataString.split('\r\n')[0:-1])) # string to list of integers
    return [x/POW32 for x in data] # return normalized to 1 list

import matplotlib.pyplot as plt
import numpy as np  
import math
import time


# Time test
####################
size = int(1e3)
start = 0;
stop = 1;
snr = 15;
std_dev = math.sqrt(10**(-snr/10))
time = np.linspace(start, stop, num=size, dtype=float)
data = np.sin(2*math.pi*time)
TRNGnoise = std_dev*(2*np.array(TRNG_ESP32(size))-1)

fig, ax1 = plt.subplots()  
ax1.plot(time, data+TRNGnoise, label='Sine+TRNG')
ax1.plot(time, data, label='Sine')
ax1.set_title("Noise contamination, SNR=15dB")  
ax1.legend() 
####################

# Elapsed time test
#####################
#size = [int(1e0), int(1e1), int(1e2), int(1e3), int(1e4), int(1e5), int(1e6)]
# TRNGdur = []
# PRNGdur = []
# for instSize in size:
#     start = time.time()
#     TRNGnoise = np.array(TRNG_ESP32(instSize), dtype=np.uint32)
#     end = time.time()
#     TRNGdur.append(end-start)
#     print('TRNG time: ' + str(end-start))
#     start = time.time()
#     PRNGnoise = np.random.randint(2**32-1, size=instSize, dtype=np.uint32)
#     end = time.time()
#     PRNGdur.append(end-start)
#     print('PRNG time: ' + str(end-start))
#####################

# Randomness test
####################
# size = int(1e5)
# # TRNGnoise = np.array(TRNG_ESP32(size), dtype=np.uint32)
# PRNGnoise = np.random.randint(2**32-1, size=size, dtype=np.uint32)


# TRNGstr = ""
# PRNGstr = ""
# for rnd in TRNGnoise:
#     TRNGstr += '{:032b}'.format(rnd)
# for rnd in PRNGnoise:
#     PRNGstr += '{:032b}'.format(rnd)

# text_file = open("TRNG.bin", "w")
# n = text_file.write(TRNGstr)
# text_file.close()

# text_file = open("PRNG.bin", "w")
# n = text_file.write(PRNGstr)
# text_file.close()
####################




