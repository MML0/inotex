import socket
import threading
import time
import cv2
import numpy as np

# --- Frame fetcher (TouchDesigner fallback) ---
def get_frame():
    try:
        top = op('out')  # TouchDesigner TOP
        frame = top.numpyArray()
        frame = np.flip(frame, axis=2)
        frame = (frame * 255).astype(np.uint8)
    except:
        frame = np.random.randint(0, 255, (240, 320, 3), dtype=np.uint8)
        # frame = cv2.imread('1.png')
        # print(1)
    _, jpeg = cv2.imencode('.jpg', frame)
    return jpeg.tobytes()

# --- MJPEG response handler ---
def client_handler(conn):
    conn.send(b"HTTP/1.1 200 OK\r\n")
    conn.send(b"Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n")

    try:
        while True:
            frame = get_frame()
            conn.send(b"--frame\r\n")
            conn.send(b"Content-Type: image/jpeg\r\n")
            conn.send(f"Content-Length: {len(frame)}\r\n\r\n".encode())
            conn.send(frame)
            conn.send(b"\r\n")
            # time.sleep(1/30)
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
        threading.Thread(target=client_handler, args=(conn,), daemon=True).start()

start_server()
