import ctypes
from ctypes import wintypes

# Constants
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
