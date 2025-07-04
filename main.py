# main.py
import tkinter as tk
import ctypes
from appbar import register_appbar, unregister_appbar
from ui import create_main_window
from time_display import update_time
from battery import start_battery_thread
from mute_status import update_mute_icon, update_mic_mute_icon, update_bluetooth_icon
from comtypes import CoInitialize, CoUninitialize

if __name__ == "__main__":
    CoInitialize() 
    try:
        # Tạo cửa sổ và đăng ký AppBar
        root, hwnd, label, battery_icon_label, battery_label, mute_icon_label, mic_mute_icon_label, bluetooth_icon_label = create_main_window()
        register_appbar(hwnd, 25)

        # Chạy các chức năng cập nhật (bao gồm cả các hàm kiểm tra mute)
        # Các hàm này sẽ sử dụng môi trường COM đã được CoInitialize() thiết lập
        update_time(root, label)
        start_battery_thread(root, battery_icon_label, battery_label)
        update_mute_icon(root, mute_icon_label) # Hàm này gọi is_system_muted()
        update_mic_mute_icon(root, mic_mute_icon_label) # Hàm này gọi is_mic_muted()
        update_bluetooth_icon(root, bluetooth_icon_label) # Hàm này gọi is_mic_muted() để kiểm tra kết nối Bluetooth

        # Xử lý khi đóng cửa sổ: hủy đăng ký AppBar, phá hủy cửa sổ và sau đó giải phóng COM
        root.protocol("WM_DELETE_WINDOW", lambda: (
            unregister_appbar(hwnd), 
            root.destroy(), 
            # Không gọi CoUninitialize() ở đây vì nó sẽ được gọi trong khối finally
        ))
        
        # Chạy vòng lặp sự kiện chính của Tkinter
        # Chương trình sẽ dừng ở đây cho đến khi cửa sổ bị đóng
        root.mainloop()

    except Exception as e:
        # Bắt bất kỳ lỗi nào xảy ra trong quá trình chạy ứng dụng chính
        print(f"Lỗi không mong muốn xảy ra trong ứng dụng chính: {e}")
    finally:
        # GIẢI PHÓNG COM MỘT LẦN DUY NHẤT KHI ỨNG DỤNG KẾT THÚC
        # Điều này đảm bảo tài nguyên COM được giải phóng sạch sẽ, ngay cả khi có lỗi
        CoUninitialize()
        print("Tài nguyên COM đã được giải phóng thành công.")