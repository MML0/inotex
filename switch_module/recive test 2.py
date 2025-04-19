import socket

# UDP configuration
UDP_IP = "192.168.43.81"  # Replace with your computer's IP address
UDP_PORT = 4210           # Replace with the port used by ESP8266

# Create a UDP socket``
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print("Listening for UDP packets...")

try:
    while True:
        # Receive data from ESP8266
        data, addr = sock.recvfrom(1024)  # Buffer size: 1024 bytes
        print(f"Received data from {addr}: {list(data)}")
except KeyboardInterrupt:
    print("\nServer stopped.")
    sock.close()

