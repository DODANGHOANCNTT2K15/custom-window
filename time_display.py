import time
import tkinter as tk

def update_time(root, label):
    def refresh():
        now = time.localtime()
        weekday = time.strftime("%a", now)  
        day = time.strftime("%d", now)
        month = time.strftime("%b", now)   
        hour_min = time.strftime("%I:%M %p", now)
        time_str = f"{weekday} {day} {month}, {hour_min}"
        label.config(text=time_str)
        root.after(1000, refresh)

    refresh()
