import win32gui
import win32api

def is_any_window_fullscreen():
    try:
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd:
            return False

        # Lấy tên class của cửa sổ (để lọc Desktop)
        class_name = win32gui.GetClassName(hwnd)
        window_title = win32gui.GetWindowText(hwnd)

        # Bỏ qua Desktop hoặc không có tiêu đề (rất có thể là desktop hoặc shell)
        if class_name in ["WorkerW", "Progman"] or window_title.strip() == "":
            return False

        # Lấy kích thước màn hình
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)

        # Lấy kích thước cửa sổ
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        width = right - left
        height = bottom - top

        # Nếu cửa sổ chiếm toàn màn hình
        return width >= screen_width and height >= screen_height
    except:
        return False
