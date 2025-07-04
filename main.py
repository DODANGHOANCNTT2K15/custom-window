import tkinter as tk
import time
import ctypes
from ctypes import wintypes
import winreg
import os
import getpass
from PIL import Image, ImageTk
import psutil
import threading
import glob
from volumn_check import is_system_muted
from mic_check import is_mic_muted

# Windows API constants
ABM_NEW = 0x00000000
ABM_REMOVE = 0x00000001
ABM_SETPOS = 0x00000003
ABE_TOP = 1

class APPBARDATA(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('hWnd', wintypes.HWND),
        ('uCallbackMessage', wintypes.UINT),
        ('uEdge', wintypes.UINT),
        ('rc', wintypes.RECT),
        ('lParam', wintypes.LPARAM),
    ]

def register_appbar(hwnd, height):
    abd = APPBARDATA()
    abd.cbSize = ctypes.sizeof(APPBARDATA)
    abd.hWnd = hwnd
    abd.uEdge = ABE_TOP

    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    abd.rc.left = 0
    abd.rc.top = 0
    abd.rc.right = screen_width
    abd.rc.bottom = height

    ctypes.windll.shell32.SHAppBarMessage(ABM_NEW, ctypes.byref(abd))
    ctypes.windll.shell32.SHAppBarMessage(ABM_SETPOS, ctypes.byref(abd))

def unregister_appbar(hwnd):
    abd = APPBARDATA()
    abd.cbSize = ctypes.sizeof(APPBARDATA)
    abd.hWnd = hwnd
    ctypes.windll.shell32.SHAppBarMessage(ABM_REMOVE, ctypes.byref(abd))

def update_time():
    now = time.localtime()
    # Lấy 3 chữ cái đầu của thứ và tháng
    weekday = time.strftime("%a", now)  # Mon, Tue, ...
    day = time.strftime("%d", now)
    month = time.strftime("%b", now)    # Jan, Feb, ...
    hour_min = time.strftime("%I:%M %p", now)
    # Ghép chuỗi
    time_str = f"{weekday} {day} {month}, {hour_min}"
    label.config(text=time_str)
    root.after(1000, update_time)

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

def get_user_avatar():
    account_pictures = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\AccountPictures")
    if os.path.exists(account_pictures):
        files = glob.glob(os.path.join(account_pictures, "*.accountpicture-ms"))
        # Nếu không có file .accountpicture-ms, thử lấy file ảnh png/jpg/bmp
        if not files:
            files = glob.glob(os.path.join(account_pictures, "*.png")) + \
                    glob.glob(os.path.join(account_pictures, "*.jpg")) + \
                    glob.glob(os.path.join(account_pictures, "*.bmp"))
        if files:
            return files[0]
    return None

# Tạo cửa sổ
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)

# Lấy theme Windows
if is_windows_dark_theme():
    bg_color = "#202020"
    fg_color = "white"
else:
    bg_color = "#ffffff"
    fg_color = "black"

root.configure(bg=bg_color)

screen_width = root.winfo_screenwidth()
bar_height = 25
root.geometry(f"{screen_width}x{bar_height}+0+0")

# Lấy handle và đăng ký AppBar
root.update_idletasks()
hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
register_appbar(hwnd, bar_height)

user_name = get_microsoft_account()

# Frame tổng
bar_frame = tk.Frame(root, bg=bg_color)
bar_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# Trái: icon window + tên user, không avatar
frame_left = tk.Frame(bar_frame, bg=bg_color)
frame_left.place(x=0, y=0, relheight=1)

# Thêm icon window.png vào trước tên user
window_img = Image.open("assets/window.png").resize((15, 15), Image.LANCZOS)
window_icon = ImageTk.PhotoImage(window_img)
window_icon_label = tk.Label(frame_left, image=window_icon, bg=bg_color)
window_icon_label.pack(side="left", padx=(5, 2), pady=1)

user_label = tk.Label(frame_left, text=user_name, font=("Segoe UI", 9), fg=fg_color, bg=bg_color)
user_label.pack(side="left", padx=(0, 8), pady=1)

# Phải: icon + phần trăm pin
frame_right = tk.Frame(bar_frame, bg=bg_color)
frame_right.place(relx=1.0, x=0, y=0, anchor="ne", relheight=1)

# Thêm label icon mute vào frame_right (trước battery_icon_label)
mute_icon_label = tk.Label(frame_right, bg=bg_color)
mute_icon_label.pack(side="left", padx=(0, 2), pady=1)

# Thêm label icon mic mute vào frame_right (trước mute_icon_label)
mic_mute_icon_label = tk.Label(frame_right, bg=bg_color)
mic_mute_icon_label.pack(side="left", padx=(0, 2), pady=1)

battery_icon_label = tk.Label(frame_right, bg=bg_color)
battery_icon_label.pack(side="left", padx=(5, 2), pady=1)
battery_label = tk.Label(frame_right, font=("Segoe UI", 9, "bold"), fg=fg_color, bg=bg_color)
battery_label.pack(side="left", padx=(0, 8), pady=1)

settings_img = Image.open("assets/settings.png").resize((15, 15), Image.LANCZOS)
settings_icon = ImageTk.PhotoImage(settings_img)
settings_label = tk.Label(frame_right, image=settings_icon, bg=bg_color, cursor="hand2")
settings_label.pack(side="left", padx=(0, 8), pady=1)

# Nếu muốn gán sự kiện click mở Settings Windows:
def open_settings(event=None):
    os.system("start ms-settings:")

settings_label.bind("<Button-1>", open_settings)

# Giữa: đồng hồ
label = tk.Label(
    bar_frame,
    font=("Segoe UI", 10, "bold"),
    fg=fg_color,
    bg=bg_color,
    anchor="center"
)
label.place(relx=0.5, rely=0.5, anchor="center")

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
        time.sleep(1)  # cập nhật mỗi 30 giây

# Chạy thread cập nhật pin
battery_thread = threading.Thread(target=update_battery_loop, daemon=True)
battery_thread.start()

update_time()

def update_mute_icon():
    if is_system_muted():
        try:
            mute_img = Image.open("assets/volumn_mute.png").resize((12, 12), Image.LANCZOS)
            mute_icon = ImageTk.PhotoImage(mute_img)
            mute_icon_label.config(image=mute_icon)
            mute_icon_label.image = mute_icon
        except Exception:
            mute_icon_label.config(image=None)
            mute_icon_label.image = None
    else:
        mute_icon_label.config(image=None)
        mute_icon_label.image = None
    root.after(1000, update_mute_icon)  # kiểm tra mỗi giây

update_mute_icon()

def update_mic_mute_icon():
    if is_mic_muted():
        try:
            mic_img = Image.open("assets/mic_mute.png").resize((15, 15), Image.LANCZOS)
            mic_icon = ImageTk.PhotoImage(mic_img)
            mic_mute_icon_label.config(image=mic_icon)
            mic_mute_icon_label.image = mic_icon
        except Exception:
            mic_mute_icon_label.config(image=None)
            mic_mute_icon_label.image = None
    else:
        mic_mute_icon_label.config(image=None)
        mic_mute_icon_label.image = None
    root.after(1000, update_mic_mute_icon)  # kiểm tra mỗi giây

update_mic_mute_icon()

def on_close():
    unregister_appbar(hwnd)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
