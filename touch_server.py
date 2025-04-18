import socket
import time
import cv2
import numpy as np
from urllib.parse import urlparse, parse_qs

# --- Frame fetcher ---
def get_frame(n):
    try:
        path = f'jpg_out/TDMovieOut.{n}.0.jpg'
        frame = cv2.imread(path)
        if frame is None:
            raise Exception(f"Image not found: {path}")
        _, jpeg = cv2.imencode('.jpg', frame)
    except:
        fallback = f'jpg_out/TDMovieOut.{n}.1.jpg'
        frame = cv2.imread(fallback)
        if frame is None:
            print(f"Fallback image not found: {fallback}")
            return b''
        _, jpeg = cv2.imencode('.jpg', frame)

    return jpeg.tobytes()

# --- MJPEG response handler ---
def handle_client(conn):
    request = conn.recv(1024).decode()
    try:
        path = request.split(" ")[1]  # Extract URL from GET request
        parsed = urlparse(path)
        query = parse_qs(parsed.query)
        n = int(query.get("n", ["0"])[0])
    except:
        n = 0  # Default to 0 if any error in parsing

    print(f"Streaming for n={n}")

    conn.send(b"HTTP/1.1 200 OK\r\n")
    conn.send(b"Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n")

    try:
        while True:
            frame = get_frame(n)
            if not frame:
                break  # Stop if image load failed

            conn.send(b"--frame\r\n")
            conn.send(b"Content-Type: image/jpeg\r\n")
            conn.send(f"Content-Length: {len(frame)}\r\n\r\n".encode())
            conn.send(frame)
            conn.send(b"\r\n")
            # time.sleep(1/30)  # Limit FPS if needed
    except:
        print("Client disconnected")
    finally:
        conn.close()

# --- Start server ---
def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 8080))
    s.listen(5)
    print("Server listening on http://localhost:8080")

    while True:
        conn, addr = s.accept()
        print(f"Connected: {addr}")
        handle_client(conn)

start_server()
