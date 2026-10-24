import os
import json
import base64
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
ARCHIVE_DIR = os.path.join(os.path.dirname(__file__), "ideas_archive")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

import sys

def send_windows_toast(title: str, message: str) -> bool:
    """Send native Windows toast notification via PowerShell WinRT API."""
    if sys.platform != "win32":
        return False
    try:
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
        res = subprocess.run(["powershell", "-NoProfile", "-EncodedCommand", encoded], capture_output=True, text=True)
        return res.returncode == 0
    except Exception as e:
        print(f"Windows Toast Error: {e}")
        return False

def send_telegram(text: str, parse_mode: str = "HTML", reply_markup: dict = None) -> bool:
    """Send message to user's Telegram PV via the configured bot."""
    cfg = load_config()
    token = os.environ.get("TELEGRAM_BOT_TOKEN") or cfg.get("telegram", {}).get("bot_token")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID") or cfg.get("telegram", {}).get("chat_id")
    
    if not token or not chat_id:
        print("Telegram not configured: missing token or chat_id.")
        return False
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": False
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    
    import time
    for attempt in range(1, 4):
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=25) as resp:
                res_data = json.loads(resp.read().decode())
                return res_data.get("ok", False)
        except Exception as e:
            print(f"Telegram Attempt {attempt} failed: {e}")
            if attempt < 3:
                time.sleep(2)
            else:
                return False

def save_to_archive(content: str, filename: str = None) -> str:
    """Save the day's ideas to a markdown file in ideas_archive/."""
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    if not filename:
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"{today}.md"
    filepath = os.path.join(ARCHIVE_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    return filepath

if __name__ == "__main__":
    print("Testing notifier modules...")
    toast_ok = send_windows_toast("تست سیستم نوتیفیکیشن", "سیستم نوتیفیکیشن ویندوز به درستی متصل شد!")
    print(f"Windows Toast: {'OK' if toast_ok else 'Failed'}")
