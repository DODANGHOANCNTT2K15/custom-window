from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

def is_system_muted():
    """
    Kiểm tra xem hệ thống Windows có đang bị tắt tiếng (mute) hay không.
    Yêu cầu CoInitialize() đã được gọi ở luồng hiện tại trước khi gọi hàm này.
    """
    devices = None # Khởi tạo None
    interface = None # Khởi tạo None
    volume = None # Khởi tạo None
    is_muted = None # Khởi tạo None
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        is_muted = volume.GetMute()
        return bool(is_muted)
    except Exception as e:
        print(f"Lỗi khi kiểm tra trạng thái mute hệ thống: {e}")
        return None
    finally:
        # Quan trọng: Đảm bảo giải phóng các đối tượng COM
        # Setting to None allows Python's garbage collector to potentially release them.
        # Although __del__ is still triggered, this helps ensure proper state.
        if volume:
            del volume
            volume = None
        if interface:
            del interface
            interface = None
        if devices:
            del devices
            devices = None
        