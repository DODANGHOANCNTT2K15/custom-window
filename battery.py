import psutil
import time
import threading
from PIL import Image, ImageTk
import queue

battery_queue = queue.Queue()

def get_battery_status():
    try:
        battery = psutil.sensors_battery()
        if battery is not None:
            return battery.percent, battery.power_plugged
        else:
            return None, None
    except Exception:
        return None, None

def get_battery_icon_path(percent, charging):
    if charging:
        return "assets/battery_5.png"
    if percent is None:
        return "assets/battery_0.png"
    if percent < 5:
        return "assets/battery_0.png"
    elif percent < 20:
        return "assets/battery_1.png"
    elif percent < 50:
        return "assets/battery_2.png"
    elif percent < 80:
        return "assets/battery_3.png"
    else:
        return "assets/battery_4.png"

def start_battery_thread():
    def update_battery_loop():
        while True:
            percent, charging = get_battery_status()
            icon_path = get_battery_icon_path(percent, charging)
            battery_queue.put((percent, icon_path))
            time.sleep(5)  # Cập nhật mỗi 5 giây
    threading.Thread(target=update_battery_loop, daemon=True).start()

def update_battery_ui(root, battery_icon_label, battery_label):
    try:
        while not battery_queue.empty():
            percent, icon_path = battery_queue.get_nowait()
            try:
                icon_img = Image.open(icon_path).resize((22, 22), Image.LANCZOS)
                icon = ImageTk.PhotoImage(icon_img)
                battery_icon_label.config(image=icon)
                battery_icon_label.image = icon
            except Exception:
                battery_icon_label.config(image=None)
                battery_icon_label.image = None

            if percent is not None:
                battery_label.config(text=f"{percent:.0f}%")
            else:
                battery_label.config(text="N/A")
    except Exception as e:
        print("Battery UI error:", e)

    # Lặp lại sau 1000ms
    root.after(1000, lambda: update_battery_ui(root, battery_icon_label, battery_label))
