import socket

def send_udp_command(message, host='127.0.0.1', port=9999):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (host, port))
    sock.close()

# Example usage:
send_udp_command("glitch:1:on")       # Turn glitch ON for stream 1
send_udp_command("glitch:2:on")       # Turn glitch ON for stream 1
send_udp_command("glitch:3:on")       # Turn glitch ON for stream 1
send_udp_command("glitch:4:on")       # Turn glitch ON for stream 1
send_udp_command("glitch:5:on")       # Turn glitch ON for stream 1
# send_udp_command("glitch:1:off")    # Turn it OFF
send_udp_command("text:3:hi!")   # Set overlay text
send_udp_command("text:1:hi!")   # Set overlay text
