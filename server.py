from flask import Flask, Response, request
import cv2
import threading
import socket

app = Flask(__name__)
videos = {
    '1': 'video1.mp4',
    '2': 'video2.mp4',
    '3': 'video3.mp4',
    '4': 'video4.mp4',
}
overlays = {
    '1': '', '2': '', '3': '', '4': ''
}
glitch_videos = {'1': 'glitch.mp4', '2': 'glitch.mp4', '3': 'glitch.mp4', '4': 'glitch.mp4'}
glitches = {'1': False, '2': False, '3': False, '4': False}

def generate(video_path, overlay_text, glitch_flag, glitch_video_path):
    cap = cv2.VideoCapture(video_path)
    glitch_cap = cv2.VideoCapture(glitch_video_path) if glitch_flag else None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize and overlay glitch frame if active
        if glitch_flag and glitch_cap and glitch_cap.isOpened():
            ret_glitch, glitch_frame = glitch_cap.read()
            if not ret_glitch:
                glitch_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # loop
                ret_glitch, glitch_frame = glitch_cap.read()

            glitch_frame = cv2.resize(glitch_frame, (frame.shape[1], frame.shape[0]))
            alpha = 0.5  # blending strength
            frame = cv2.addWeighted(glitch_frame, alpha, frame, 1 - alpha, 0)

        # Optional overlay text
        if overlay_text:
            cv2.putText(frame, overlay_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    if glitch_cap:
        glitch_cap.release()

@app.route('/video')
def video_feed():
    n = request.args.get('n', '1')
    video = videos.get(n, 'video1.mp4')
    overlay = overlays.get(n, '')
    glitch = glitches.get(n, False)
    glitch_video = glitch_videos.get(n, 'glitch.mp4')
    return Response(generate(video, overlay, glitch, glitch_video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

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
                glitch_videos[n] = val  # set a specific glitch video path

            print(f"Updated stream {n}: {cmd} = {val}")
        except Exception as e:
            print("Invalid UDP command:", msg)

if __name__ == '__main__':
    threading.Thread(target=udp_listener, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
