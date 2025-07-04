# main.py
import tkinter as tk
import ctypes
from appbar import register_appbar, unregister_appbar
from ui import create_main_window
from time_display import update_time
from battery import start_battery_thread, update_battery_ui
from icon_status import update_mute_icon, update_mic_mute_icon, update_bluetooth_icon
from comtypes import CoInitialize, CoUninitialize

if __name__ == "__main__":
    CoInitialize() 
    try:
        root, hwnd, label, battery_icon_label, battery_label, mute_icon_label, mic_mute_icon_label, bluetooth_icon_label = create_main_window()
        register_appbar(hwnd, 25)
        update_time(root, label)
        start_battery_thread()
        update_battery_ui(root, battery_icon_label, battery_label)
        update_mute_icon(root, mute_icon_label) 
        update_mic_mute_icon(root, mic_mute_icon_label) 
        update_bluetooth_icon(root, bluetooth_icon_label)

        root.protocol("WM_DELETE_WINDOW", lambda: (
            unregister_appbar(hwnd),  
            root.destroy(), 
        ))
        
        root.mainloop()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        CoUninitialize()
        print("Liberation of resources!")