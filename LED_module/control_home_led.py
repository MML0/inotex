import socket
import time
import random


# Configure server IP and port
server_port = 8266
esp_ip = "192.168.43.222"  # ESP's static IP 8266

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# Example data to send to ESP
led_data = b'\xFF\x00\x00' + b'\x00\x00\x00' * 1023  # Sync byte + RGB data for each LED
led_data = bytearray(1024 * 3)
i = 0
led_data = b'\x00\x00\x00' * 1024  # Sync byte + RGB data for each LED
led_data = bytearray(1024 *  b'\x00\x00\x00')
r = random.randint(0, 10)
g = random.randint(0, 10)
b = random.randint(0, 10)

while True: 
    # Send data to ESP
    t = time.time()
    #led_data = input().encode( encoding="utf-8")
    r += random.randint(-5, 5)
    g += random.randint(-5, 5)
    b += random.randint(-5, 5)
    
    # Insert new random color at the start of the array
    
    # Shift all pixels to the right by 1
    led_data[3:] = led_data[:-3]
    led_data[0:3] = [abs(r%24), abs(g%24), abs(b%24)]

    #led_data = b'\xFF\xFF\xFF' * 300  # Sync byte + RGB data for each LED

    sock.sendto(bytearray(b'\xAA' + led_data), (esp_ip, 8266))

    i += 1
    # Wait for the ESP's response
    #data, addr = sock.recvfrom(64)
    #print("Received from ESP:", data.decode())
    print(time.time()-t)
    time.sleep(0.05)

