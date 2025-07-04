import subprocess

def is_bluetooth_enabled():
    try:
        # Chạy lệnh PowerShell để lấy trạng thái Bluetooth
        output = subprocess.check_output(
            ['powershell', '-Command',
             "(Get-PnpDevice -Class Bluetooth -Status 'OK') -ne $null"],
            stderr=subprocess.DEVNULL,
            text=True
        )
        return True if output.strip() else False
    except subprocess.CalledProcessError:
        return False
