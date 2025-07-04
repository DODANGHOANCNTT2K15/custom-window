import psutil
import time
import threading
from PIL import Image, ImageTk
import queue
import os

battery_queue = queue.Queue()
_last_state = {'percent': None, 'charging': None}  

def get_battery_status():
    try:
        battery = psutil.sensors_battery()
        if battery:
            return battery.percent, battery.power_plugged
    except Exception:
        pass
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
            if (percent, charging) != (_last_state['percent'], _last_state['charging']):
                icon_path = get_battery_icon_path(percent, charging)
                battery_queue.put((percent, icon_path))
                _last_state['percent'] = percent
                _last_state['charging'] = charging
            time.sleep(5) 

    threading.Thread(target=update_battery_loop, daemon=True).start()

_icon_cache = {}

def update_battery_ui(root, battery_icon_label, battery_label):
    try:
        while not battery_queue.empty():
            percent, icon_path = battery_queue.get_nowait()
            if icon_path in _icon_cache:
                icon = _icon_cache[icon_path]
            else:
                try:
                    icon_img = Image.open(icon_path).resize((22, 22), Image.LANCZOS)
                    icon = ImageTk.PhotoImage(icon_img)
                    _icon_cache[icon_path] = icon
                except Exception:
                    icon = None

            battery_icon_label.config(image=icon)
            battery_icon_label.image = icon

            battery_label.config(text=f"{percent:.0f}%" if percent is not None else "N/A")
    except Exception as e:
        print("Battery UI error:", e)

    root.after(1000, lambda: update_battery_ui(root, battery_icon_label, battery_label))
