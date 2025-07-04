import psutil
import time
import threading
from PIL import Image, ImageTk
import tkinter as tk

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

def start_battery_thread(root, battery_icon_label, battery_label):
    def update_battery_loop():
        while True:
            percent, charging = get_battery_status()
            icon_path = get_battery_icon_path(percent, charging)

            def update_ui():
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

            root.after(0, update_ui)
            time.sleep(1)

    threading.Thread(target=update_battery_loop, daemon=True).start()