from flask import Flask, Response, request
import cv2
import threading
import socket
import time

app = Flask(__name__)

videos = {
    '1': 'data/video1.mp4',
    '2': 'data/video2.mp4',
    '3': 'data/video3.mp4',
    '4': 'data/video4.mp4',
    '5': 'data/video5.mp4',
}

overlays = {n: '' for n in videos}
glitches = {n: False for n in videos}
glitch_videos = {
    '1': 'data/glitch1.mp4',
    '2': 'data/glitch2.mp4',
    '3': 'data/glitch3.mp4',
    '4': 'data/glitch4.mp4',
    '5': 'data/glitch5.mp4',
}

frame_buffers = {}

class VideoStreamThread(threading.Thread):
    def __init__(self, stream_id):
        super().__init__()
        self.stream_id = stream_id
        self.daemon = True
        self.running = True
        self.lock = threading.Lock()
        self.latest_frame = None
        self.start()

    def run(self):
        global videos, overlays, glitches, glitch_videos

        cap = cv2.VideoCapture(videos[self.stream_id])
        glitch_cap = None

        while self.running:
            if not cap.isOpened():
                time.sleep(0.1)
                cap = cv2.VideoCapture(videos[self.stream_id])
                continue

            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            if glitches[self.stream_id]:
                if not glitch_cap or not glitch_cap.isOpened():
                    glitch_cap = cv2.VideoCapture(glitch_videos[self.stream_id])

                ret_glitch, glitch_frame = glitch_cap.read()
                if not ret_glitch:
                    glitch_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue

                glitch_frame = cv2.resize(glitch_frame, (frame.shape[1], frame.shape[0]))
                alpha = 0.5
                frame = cv2.addWeighted(glitch_frame, alpha, frame, 1 - alpha, 0)

            if overlays[self.stream_id]:
                cv2.putText(frame, overlays[self.stream_id], (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])
            with self.lock:
                self.latest_frame = buffer.tobytes()

            time.sleep(1 / 60.0)  # Cap at 30 FPS

        cap.release()
        if glitch_cap:
            glitch_cap.release()

    def get_frame(self):
        with self.lock:
            return self.latest_frame

# Start a thread for each stream
stream_threads = {n: VideoStreamThread(n) for n in videos}

@app.route('/video')
def video_feed():
    n = request.args.get('n', '1')
    def generate():
        while True:
            frame = stream_threads[n].get_frame()
            if frame:
                yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.03)
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

# -- UDP Command Listener --
def udp_listener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 9999))
    while True:
        data, _ = sock.recvfrom(1024)
        msg = data.decode()
        try:
            parts = msg.strip().split(':')
            cmd, n, val = parts[0], parts[1], parts[2]
            if cmd == 'video':
                videos[n] = val
            elif cmd == 'text':
                overlays[n] = val
            elif cmd == 'glitch':
                glitches[n] = val.lower() == 'on'
            elif cmd == 'glitchvid':
                glitch_videos[n] = val
            print(f"[UDP] {cmd}:{n}:{val}")
        except Exception as e:
            print("Invalid UDP command:", msg)

if __name__ == '__main__':
    threading.Thread(target=udp_listener, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
