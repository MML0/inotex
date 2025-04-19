import socket
import time

# Network Configuration
UDP_IP = "192.168.43.81"  # The IP address of this computer
UDP_PORT = 4210          # Same port as configured in the ESP8266

def main():
    try:
        # Create UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))
        print(f"Listening for UDP data on {UDP_IP}:{UDP_PORT}")
        
        # Main loop
        while True:
            try:
                # Receive data
                data, addr = sock.recvfrom(1024)
                
                if len(data) == 9:  # 8 switch states + 1 info byte
                    # Extract switch states
                    switch_states = list(data[:8])
                    
                    # Extract info byte
                    info_byte = data[8]
                    switch_index = info_byte & 0x0F  # Lower 4 bits for switch index
                    is_long_press = (info_byte & 0x80) != 0  # Highest bit for long press
                    
                    # Print switch states
                    print("\nSwitch States:", end=" ")
                    for i, state in enumerate(switch_states):
                        print(f"SW{i+1}:{state}", end=" ")
                    
                    # Print event information
                    event_type = "LONG PRESS" if is_long_press else "STATE CHANGE"
                    print(f"\nEvent: {event_type} on Switch {switch_index + 1}")
                    
            except BlockingIOError:
                # No data available
                time.sleep(0.01)
                continue
                
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        sock.close()

if __name__ == "__main__":
    main()

