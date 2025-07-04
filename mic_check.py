from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

def is_mic_muted():
    """
    Kiểm tra xem mic mặc định của Windows có đang bị tắt tiếng (mute) hay không.
    Yêu cầu CoInitialize() đã được gọi ở luồng hiện tại trước khi gọi hàm này.
    """
    devices = None
    interface = None
    volume = None
    is_muted = None
    try:
        devices = AudioUtilities.GetMicrophone() # Hoặc phương pháp đúng để lấy mic
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        is_muted = volume.GetMute()
        return bool(is_muted)
    except Exception as e:
        print(f"Lỗi khi kiểm tra trạng thái mute mic: {e}")
        return None
    finally:
        if volume:
            del volume
            volume = None
        if interface:
            del interface
            interface = None
        if devices:
            del devices
            devices = None