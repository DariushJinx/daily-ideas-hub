import subprocess
import base64

def send_windows_toast(title: str, message: str):
    ps_script = f"""
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
$template = @"
<toast>
    <visual>
        <binding template="ToastGeneric">
            <text>{title}</text>
            <text>{message}</text>
        </binding>
    </visual>
</toast>
"@
$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml($template)
$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Daily Ideas Hub").Show($toast)
"""
    encoded = base64.b64encode(ps_script.encode("utf-16le")).decode("utf-8")
    result = subprocess.run(["powershell", "-NoProfile", "-EncodedCommand", encoded], capture_output=True, text=True)
    if result.returncode == 0:
        print("SUCCESS: Windows notification sent!")
    else:
        print("ERROR:", result.stderr)

if __name__ == "__main__":
    send_windows_toast("ایده‌های روزانه کسب‌وکار 🚀", "سیستم نوتیفیکیشن ویندوز با موفقیت فعال شد!")
