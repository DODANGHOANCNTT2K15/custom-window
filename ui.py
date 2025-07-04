import tkinter as tk
import ctypes
import os
import winreg
import getpass
from PIL import Image, ImageTk
from PIL import ImageDraw
import pyautogui
import subprocess

def is_windows_dark_theme():
    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
        key = winreg.OpenKey(reg, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return value == 0  # True nếu là dark mode
    except Exception:
        return False

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

def create_main_window():
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)

    # Theme
    if is_windows_dark_theme():
        bg_color = "#202020"
        fg_color = "white"
    else:
        bg_color = "#ffffff"
        fg_color = "black"

    root.configure(bg=bg_color)
    screen_width = root.winfo_screenwidth()
    bar_height = 30
    root.geometry(f"{screen_width}x{bar_height}+0+0")

    # Lấy handle
    root.update_idletasks()
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())

    # UI tổng
    bar_frame = tk.Frame(root, bg=bg_color)
    bar_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Frame trái
    frame_left = tk.Frame(bar_frame, bg=bg_color)
    frame_left.place(x=0, y=0, relheight=1)

    # Icon + User
    window_img = Image.open("assets/window.png").resize((15, 15), Image.LANCZOS)
    window_icon = ImageTk.PhotoImage(window_img)
    window_icon_label = tk.Label(frame_left, image=window_icon, bg=bg_color)
    window_icon_label.image = window_icon
    window_icon_label.pack(side="left", padx=(5, 2), pady=1)

    user_label = tk.Label(frame_left, text=get_microsoft_account(), font=("Segoe UI", 9), fg=fg_color, bg=bg_color)
    user_label.pack(side="left", padx=(0, 8), pady=1)

    # Frame phải
    frame_right = tk.Frame(bar_frame, bg=bg_color)
    frame_right.place(relx=1.0, x=0, y=0, anchor="ne", relheight=1)

    # Thêm biểu tượng ellipsis
    ellipsis_img = Image.open("assets/ellipsis.png").resize((20, 20), Image.LANCZOS)
    ellipsis_icon = ImageTk.PhotoImage(ellipsis_img)
    ellipsis_label = tk.Label(frame_right, image=ellipsis_icon, bg=bg_color, cursor="hand2")
    ellipsis_label.image = ellipsis_icon # Giữ tham chiếu để hình ảnh không bị thu hồi
    
    # Gán hàm press_windows_a() cho sự kiện click chuột trái (Button-1)
    ellipsis_label.bind("<Button-1>", lambda event: press_windows_a())
    ellipsis_label.pack(side="left", padx=(0, 8), pady=1)

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

    # Đồng hồ
    label = tk.Label(
        bar_frame,
        font=("Segoe UI", 9, "bold"),
        fg=fg_color,
        bg=bg_color,
        anchor="center"
    )
    label.place(relx=0.5, rely=0.5, anchor="center")

    # Trả về tất cả đối tượng cần dùng
    return root, hwnd, label, battery_icon_label, battery_label, mute_icon_label, mic_mute_icon_label, bluetooth_icon_label
