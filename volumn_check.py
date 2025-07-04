from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

def is_system_muted():
    devices = None 
    interface = None 
    volume = None 
    is_muted = None 
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        is_muted = volume.GetMute()
        return bool(is_muted)
    except Exception as e:
        print(f"Error: {e}")
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
        