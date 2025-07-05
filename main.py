import tkinter as tk
import ctypes
import threading
import os
import sys
import subprocess
from PIL import Image
import pystray
import time
from appbar import register_appbar, unregister_appbar
from ui import create_main_window
from time_display import update_time
from battery import start_battery_thread, update_battery_ui
from icon_status import update_mute_icon, update_mic_mute_icon, update_bluetooth_icon
from comtypes import CoInitialize, CoUninitialize
from fullscreen import is_any_window_fullscreen
from ui import start_window_monitor

root = None

def resource_path(relative_path):
    try:
        return os.path.join(sys._MEIPASS, relative_path)
    except Exception:
        return os.path.join(os.path.abspath("."), relative_path)

def reset_app(icon, item):
    exe_path = sys.executable
    subprocess.Popen([exe_path] + sys.argv, creationflags=subprocess.CREATE_NO_WINDOW)

    def safe_exit():
        if root:
            root.destroy()
        sys.exit()

    icon.stop()
    threading.Timer(0.3, safe_exit).start() 

def on_exit(icon, item):
    icon.stop()
    if root:
        root.destroy()
    sys.exit()

def create_tray_icon():
    """Tạo icon và menu tray"""
    image_path = resource_path("assets/window.png")
    image = Image.open(image_path)

    # Menu đúng callback — không gọi nhầm
    menu = pystray.Menu(
        pystray.MenuItem("Reset App", lambda icon, item: reset_app(icon, item)),
        pystray.MenuItem("Thoát", lambda icon, item: on_exit(icon, item))
    )

    tray_icon = pystray.Icon("AppName", image, "AppName", menu)
    tray_icon.run()

def check_fullscreen(root):
    def loop():
        while True:
            try:
                if is_any_window_fullscreen():
                    root.withdraw()  
                else:
                    root.deiconify()  
                root.after(1000, lambda: None)  
            except:
                pass
            time.sleep(0.1)
    
    threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    CoInitialize()
    try:
        print("==> Chương trình khởi động")

        # Tạo giao diện chính
        root, hwnd, label, battery_icon_label, battery_label, mute_icon_label, mic_mute_icon_label, bluetooth_icon_label, widgets_to_update = create_main_window()

        # Chạy tray icon ở thread riêng
        threading.Thread(target=create_tray_icon, daemon=True).start()

        # Đăng ký appbar
        root.after(200, lambda: register_appbar(hwnd, 25))

        # Cập nhật dữ liệu thời gian và biểu tượng
        update_time(root, label)
        start_battery_thread()
        check_fullscreen(root)
        start_window_monitor(root, widgets_to_update)
        update_battery_ui(root, battery_icon_label, battery_label)
        update_mute_icon(root, mute_icon_label)
        update_mic_mute_icon(root, mic_mute_icon_label)
        update_bluetooth_icon(root, bluetooth_icon_label)

        # Vòng lặp chính
        root.mainloop()

    except Exception as e:
        print(f"[Lỗi] {e}")
    finally:
        CoUninitialize()

