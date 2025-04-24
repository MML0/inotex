import socket
import cv2

# تنظیمات UDP
UDP_IP = "192.168.43.81"  # آدرس IP که باید داده‌ها در آن دریافت شود
UDP_PORT = 4210           # پورت برای دریافت داده‌ها

# مسیر ویدیوها
video_paths = {
    1: "C:/Videos/video1.mp4",  # مسیر ویدیوی اول
    2: "C:/Videos/video2.mp4"   # مسیر ویدیوی دوم
}

# ایجاد سوکت UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# تابع برای پخش ویدیو
def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Cannot open video file: {video_path}")
        return
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:  # اگر ویدیو به انتها رسید
            break
        cv2.imshow('Video Player', frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):  # برای خروج کلید Q را فشار دهید
            break
    cap.release()
    cv2.destroyAllWindows()

# متغیر برای ذخیره آخرین کد ویدیو پخش شده
previous_code = None

print("Waiting for data...")
while True:
    # دریافت داده‌ها از UDP
    data, addr = sock.recvfrom(1024)  # دریافت حداکثر 1024 بایت
    print(f"Raw data received: {data}")  # پرینت داده خام دریافتی
    
    try:
        video_code = int(data[0])  # تبدیل داده به عدد
    except (ValueError, IndexError):
        print("Invalid data received!")
        continue

    print(f"Processed video code: {video_code}")  # پرینت کد پردازش‌شده

    # پخش ویدیوی جدید در صورت تغییر کد
    if video_code != previous_code:
        if video_code in video_paths:
            print(f"Playing video for code: {video_code}")
            play_video(video_paths[video_code])
            previous_code = video_code
        else:
            print(f"No video associated with code: {video_code}")
