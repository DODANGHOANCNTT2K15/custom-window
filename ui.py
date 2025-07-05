import tkinter as tk
import ctypes
import os
import winreg
import getpass
from PIL import Image, ImageTk
import pyautogui
import sys
import pyautogui
from PIL import ImageGrab
import threading
import win32gui
import win32process
import win32con
import psutil
import time

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_color_at_screen_position(x, y):
    try:
        screenshot = ImageGrab.grab()
        pixel_color = screenshot.getpixel((x, y)) 
        hex_color = f"#{pixel_color[0]:02X}{pixel_color[1]:02X}{pixel_color[2]:02X}"
        
        return hex_color
    except Exception as e:
        print(f"Đã xảy ra lỗi khi lấy mã màu: {e}")
        return "#202020"

def get_microsoft_account():
    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(reg, r"Software\Microsoft\IdentityCRL\UserExtendedProperties")
        email = winreg.EnumKey(key, 0)
        winreg.CloseKey(key)
        return email
    except Exception:
        return getpass.getuser()

def press_windows_a():
    pyautogui.hotkey('win', 'a')

def get_display_name():
    GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
    NameDisplay = 3  # NameDisplay là tên người dùng đầy đủ (VD: "Đỗ Đăng Hoàn")

    size = ctypes.pointer(ctypes.c_ulong(0))
    GetUserNameEx(NameDisplay, None, size)

    name_buffer = ctypes.create_unicode_buffer(size.contents.value)
    if GetUserNameEx(NameDisplay, name_buffer, size):
        return name_buffer.value
    return None

def create_main_window():
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)

    bg_color = "#202020"
    bg_color = get_color_at_screen_position(100, 30)
    fg_color = "white"

    root.configure(bg=bg_color)
    screen_width = root.winfo_screenwidth()
    bar_height = 30
    root.geometry(f"{screen_width}x{bar_height}+0+0")

    root.update_idletasks()
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())

    bar_frame = tk.Frame(root, bg=bg_color)
    bar_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Frame left
    frame_left = tk.Frame(bar_frame, bg=bg_color)
    frame_left.place(x=0, y=0, relheight=1)

    # Icon + User
    window_img = Image.open(resource_path("assets/window.png")).resize((15, 15), Image.LANCZOS)
    window_icon = ImageTk.PhotoImage(window_img)
    window_icon_label = tk.Label(frame_left, image=window_icon, bg=bg_color)
    window_icon_label.image = window_icon
    window_icon_label.pack(side="left", padx=(5, 2), pady=1)

    user_label = tk.Label(frame_left, text=get_display_name(), font=("Segoe UI", 9), fg=fg_color, bg=bg_color)
    user_label.pack(side="left", padx=(0, 8), pady=1)

    # Frame right
    frame_right = tk.Frame(bar_frame, bg=bg_color)
    frame_right.place(relx=1.0, x=0, y=0, anchor="ne", relheight=1)

    mute_icon_label = tk.Label(frame_right, bg=bg_color)
    mute_icon_label.pack(side="left", padx=(0, 2), pady=1)

    mic_mute_icon_label = tk.Label(frame_right, bg=bg_color)
    mic_mute_icon_label.pack(side="left", padx=(0, 2), pady=1)

    bluetooth_icon_label = tk.Label(frame_right, bg=bg_color)
    bluetooth_icon_label.pack(side="left", padx=(0, 2), pady=1)

    battery_icon_label = tk.Label(frame_right, bg=bg_color)
    battery_icon_label.pack(side="left", padx=(5, 2), pady=1)

    battery_label = tk.Label(frame_right, font=("Segoe UI", 9, "bold"), fg=fg_color, bg=bg_color)
    battery_label.pack(side="left", padx=(0, 8), pady=1)

    ellipsis_img = Image.open(resource_path("assets/ellipsis.png")).resize((20, 20), Image.LANCZOS)
    ellipsis_icon = ImageTk.PhotoImage(ellipsis_img)
    ellipsis_label = tk.Label(frame_right, image=ellipsis_icon, bg=bg_color, cursor="hand2")
    ellipsis_label.image = ellipsis_icon 

    ellipsis_label.bind("<Button-1>", lambda event: press_windows_a())
    ellipsis_label.pack(side="left", padx=(0, 8), pady=1)

    # clock
    label = tk.Label(
        bar_frame,
        font=("Segoe UI", 9, "bold"),
        fg=fg_color,
        bg=bg_color,
        anchor="center"
    )
    label.place(relx=0.5, rely=0.5, anchor="center")

    widgets_to_update = [
        root, bar_frame, frame_left, frame_right, user_label,
        mute_icon_label, mic_mute_icon_label, bluetooth_icon_label,
        battery_icon_label, battery_label, ellipsis_label, label
    ]
    return root, hwnd, label, battery_icon_label, battery_label, mute_icon_label, mic_mute_icon_label, bluetooth_icon_label, widgets_to_update

def is_window_maximized(hwnd):
    placement = win32gui.GetWindowPlacement(hwnd)
    return placement[1] == win32con.SW_MAXIMIZE

def get_foreground_info():
    hwnd = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    return hwnd, pid

def start_window_monitor(root, widgets_to_update):
    last_pid = None
    last_hwnd = None
    last_maximized = None

    def monitor():
        nonlocal last_pid, last_hwnd, last_maximized
        while True:
            try:
                hwnd, pid = get_foreground_info()
                maximized = is_window_maximized(hwnd)

                if (
                    pid != last_pid or
                    hwnd != last_hwnd or
                    maximized != last_maximized
                ):
                    if maximized:
                        time.sleep(0.2)
                        new_color = get_color_at_screen_position(100, 30)
                        root.after(0, lambda: update_background_color(new_color, widgets_to_update))
                    
                    last_pid = pid 
                    last_hwnd = hwnd
                    last_maximized = maximized

            except Exception:
                pass
            time.sleep(0.3)

    threading.Thread(target=monitor, daemon=True).start()

def update_background_color(new_color, widgets):
    if not widgets:
        return
    if is_bright_color(new_color):
        new_color = "#202020"  

    current_color = widgets[0].cget("bg")
    fade_background_color(widgets[0].winfo_toplevel(), widgets, current_color, new_color)

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02X}{:02X}{:02X}'.format(*rgb)

def interpolate_color(color1, color2, step, total_steps):
    return tuple(
        int(color1[i] + (color2[i] - color1[i]) * step / total_steps)
        for i in range(3)
    )

def fade_background_color(root, widgets, from_color, to_color, steps=20, delay=20):
    from_rgb = hex_to_rgb(from_color)
    to_rgb = hex_to_rgb(to_color)

    def update_step(step):
        if step > steps:
            return
        new_rgb = interpolate_color(from_rgb, to_rgb, step, steps)
        new_hex = rgb_to_hex(new_rgb)
        for widget in widgets:
            widget.configure(bg=new_hex)
        root.after(delay, lambda: update_step(step + 1))

    update_step(0)

def is_bright_color(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return luminance > 180 
