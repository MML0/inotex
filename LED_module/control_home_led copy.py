import socket
import time
import random
import math


# Configure server IP and port
server_port = 8266
esp_ip = "192.168.43.222"  # ESP's static IP

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Special 10-byte sequence (replace with your own sequence if needed)
special_sequence = bytes([0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A])

# Example data to send to ESP
num_leds = 1024
led_data = bytearray(num_leds * 3)  # Prepare an array for 1024 LEDs (3 bytes per LED)

for i in range (1020):
    # Generate random color for the first LED
    r = random.randint(0, 5)
    g = random.randint(0, 5)
    b = random.randint(0, 5)

    a = 20
    r = int((math.sin(i/15  )+1)*a)
    g = int((math.sin(i/20+1)+1)*a)
    b = int((math.sin(i/25+2)+1)*a)

    # Insert new random color at the start of the array
    led_data[3*i:3+3*i] = [r, g, b]

# for i in range (20):
#     led_data[3*i:3+3*i] = [255,0,0]
# for i in range (110,125):
#     led_data[3*i:3+3*i] = [0,255,0]
# for i in range (530,535):
#     led_data[3*i:3+3*i] = [0,0,255]
# for i in range (200,210):
#     led_data[3*i:3+3*i] = [255,0,255]
# for i in range (610,625):
#     led_data[3*i:3+3*i] = [0,255,255]
# for i in range (830,845):
#     led_data[3*i:3+3*i] = [200,200,10]

packet = bytearray()
packet.append(0xAA)  # Sync byte
packet.extend(led_data)  # LED data

sock.sendto(packet, (esp_ip, server_port))

time.sleep(0.5)





shift_speed = random.randint(10, 100)  # Example: Random speed between 10 and 100
shift_speed = 10

# Create the packet to send
led_data = bytearray(num_leds * 3-10)  # Prepare an array for 1024 LEDs (3 bytes per LED)

packet = bytearray()
packet.append(0xAA)  # Sync byte
packet.extend(special_sequence)  # Special 10-byte sequence
packet.append(shift_speed)  # Shift speed byte after the special sequence
#packet.extend(led_data)  # LED data

# Send the packet to the ESP
sock.sendto(packet, (esp_ip, server_port))

