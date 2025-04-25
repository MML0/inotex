import socket
import struct
import math

# Setup
UDP_IP = "192.168.0.12"
UDP_PORT = 4210
avreg = []

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    sock.setblocking(False)  # Non-blocking mode
    print("Listening on {}:{}".format(UDP_IP, UDP_PORT))
except Exception as e:
    debug('Socket Error:', e)

# Clear out buffer before starting
try:
    while True:
        sock.recv(65536)  # Big buffer to flush pending data
except BlockingIOError:
    pass

def whileOn(channel, sampleIndex, val, prev):
    try:
        data, addr = sock.recvfrom(1024)  # Read UDP packet
        ip = addr[0]
        print(ip)
        digital_values = list(data)  # Convert bytes to list of ints
        #print(f"Received data from {addr}: {list(data)}")

        # Loop through and put data in 'keys' table
        for i, value in enumerate(digital_values):
            table = op('keys')
            row_name = 'k{}'.format(i + 1) + str(ip.split('.')[-1])
        
             if table.row(row_name) is None:
                table.appendRow([row_name, '0'])
        
            table[row_name, 1] = value
        
    except BlockingIOError:
        pass  # No new data to process
    except Exception as e:
        debug('Error:', e)

    return

def whileOff(channel, sampleIndex, val, prev):
    return

def onOffToOn(channel, sampleIndex, val, prev):
    return

def onOnToOff(channel, sampleIndex, val, prev):
    return