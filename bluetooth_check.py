import subprocess
import json
import re

def get_connected_bluetooth_devices():
    """
    Lấy danh sách các thiết bị Bluetooth đang kết nối.
    
    Returns:
        list: Danh sách tên thiết bị đang kết nối
    """
    connected_devices = []
    
    try:
        # Lệnh PowerShell để lấy danh sách thiết bị Bluetooth đã kết nối
        cmd = [
            'powershell', '-Command',
            '''
            $devices = Get-PnpDevice -Class Bluetooth | Where-Object {$_.Status -eq "OK"}
            foreach ($device in $devices) {
                $device.FriendlyName
            }
            '''
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            output = result.stdout.strip()
            if output:
                devices = [line.strip() for line in output.split('\n') if line.strip()]
                connected_devices = devices
        
        # Phương pháp bổ sung: Sử dụng netsh để kiểm tra
        cmd_netsh = ['netsh', 'bluetooth', 'show', 'devices']
        result_netsh = subprocess.run(cmd_netsh, capture_output=True, text=True, timeout=15)
        
        if result_netsh.returncode == 0:
            output = result_netsh.stdout
            # Tìm thiết bị đã kết nối (Connected)
            lines = output.split('\n')
            for line in lines:
                if 'Connected' in line or 'Đã kết nối' in line:
                    # Trích xuất tên thiết bị
                    device_match = re.search(r'"([^"]+)"', line)
                    if device_match:
                        device_name = device_match.group(1)
                        if device_name not in connected_devices:
                            connected_devices.append(device_name)
    
    except Exception as e:
        print(f"Lỗi khi lấy danh sách thiết bị: {e}")
    
    return connected_devices

def check_bluetooth_connection_detailed():
    try:
        # Lệnh PowerShell chi tiết để kiểm tra Bluetooth
        cmd = [
            'powershell', '-Command',
            '''
            $bluetoothRadios = Get-PnpDevice -Class Bluetooth | Where-Object {$_.Status -eq "OK"}
            $result = @{
                "TotalDevices" = $bluetoothRadios.Count
                "ConnectedDevices" = @()
            }
            
            foreach ($device in $bluetoothRadios) {
                $deviceInfo = @{
                    "Name" = $device.FriendlyName
                    "Status" = $device.Status
                    "DeviceID" = $device.DeviceID
                }
                $result.ConnectedDevices += $deviceInfo
            }
            
            $result | ConvertTo-Json -Depth 3
            '''
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
                return {
                    'connected': 1 if data.get('TotalDevices', 0) > 0 else 0,
                    'device_count': data.get('TotalDevices', 0),
                    'devices': data.get('ConnectedDevices', [])
                }
            except json.JSONDecodeError:
                pass
        
        # Fallback method
        devices = get_connected_bluetooth_devices()
        return {
            'connected': 1 if len(devices) > 0 else 0,
            'device_count': len(devices),
            'devices': [{'Name': device} for device in devices]
        }
        
    except Exception as e:
        return {
            'connected': 0,
            'device_count': 0,
            'devices': [],
            'error': str(e)
        }

def is_bluetooth_enabled():
    detailed_info = check_bluetooth_connection_detailed()
    if detailed_info['connected'] == 1:
        return 1
    else:
        return 0