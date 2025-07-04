from PIL import Image, ImageTk
from volumn_check import is_system_muted
from mic_check import is_mic_muted
from bluetooth_check import is_bluetooth_enabled
import tkinter as tk
from comtypes import CLSCTX_ALL, CoInitialize, CoUninitialize

def update_mute_icon(root, mute_icon_label):
    def loop():
        if is_system_muted():
            mute_img = Image.open("assets/volumn_mute.png").resize((12, 12), Image.LANCZOS)
            mute_icon = ImageTk.PhotoImage(mute_img)
            mute_icon_label.config(image=mute_icon)
            mute_icon_label.image = mute_icon
        else:
            mute_icon_label.config(image=None)
            mute_icon_label.image = None
        root.after(200, lambda: update_mute_icon(root, mute_icon_label))
    loop()

def update_mic_mute_icon(root, mic_mute_icon_label):
    def loop():
        if is_mic_muted():
            mic_img = Image.open("assets/mic_mute.png").resize((15, 15), Image.LANCZOS)
            mic_icon = ImageTk.PhotoImage(mic_img)
            mic_mute_icon_label.config(image=mic_icon)
            mic_mute_icon_label.image = mic_icon
        else:
            mic_mute_icon_label.config(image=None)
            mic_mute_icon_label.image = None
        root.after(200, lambda: update_mic_mute_icon(root, mic_mute_icon_label))
    loop()

def update_bluetooth_icon(root, bluetooth_icon_label):
    def loop():
        if is_bluetooth_enabled():
            blue_img = Image.open("assets/bluetooth_connected.png").resize((12, 12), Image.LANCZOS)
            blue_icon = ImageTk.PhotoImage(blue_img)
            bluetooth_icon_label.config(image=blue_icon)
            bluetooth_icon_label.image = blue_icon
        else:
            bluetooth_icon_label.config(image=None)
            bluetooth_icon_label.image = None
        root.after(200, lambda: update_bluetooth_icon(root, bluetooth_icon_label))
    loop()