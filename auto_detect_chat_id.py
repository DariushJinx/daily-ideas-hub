import json
import urllib.request
import os
import notifier

def detect_and_register():
    cfg = notifier.load_config()
    token = cfg.get("telegram", {}).get("bot_token")
    if not token:
        print("Error: bot_token not found in config.json")
        return False
        
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            updates = data.get("result", [])
            
            if not updates:
                print("NO_UPDATES_YET")
                return False
                
            last_msg = None
            for upd in reversed(updates):
                if "message" in upd and "chat" in upd["message"]:
                    last_msg = upd["message"]
                    break
                    
            if not last_msg:
                print("NO_MESSAGE_FOUND")
                return False
                
            chat_id = last_msg["chat"]["id"]
            user_name = last_msg["from"].get("first_name", "User")
            
            # Save chat_id
            cfg["telegram"]["chat_id"] = chat_id
            notifier.save_config(cfg)
            print(f"SUCCESS: Registered chat_id={chat_id} for user '{user_name}'")
            
            # Send welcome message
            welcome_text = (
                f"سلام {user_name} عزیز! 🚀\n\n"
                "ربات <b>ایده‌های روزانه کسب‌وکار</b> با موفقیت به پی‌وی شما متصل شد!\n\n"
                "از این پس هر روز راس ساعت <b>۱۳:۰۰</b> ایده‌های گلچین‌شده و بکر اینترنتی "
                "همراه با تحلیل و لینک اختصاصی مستقیماً به اینجا ارسال خواهند شد."
            )
            notifier.send_telegram(welcome_text)
            notifier.send_windows_toast("اتصال موفق تلگرام ✅", f"ربات تلگرام با موفقیت به پی‌وی شما متصل شد!")
            return True
            
    except Exception as e:
        print(f"Detection Error: {e}")
        return False

if __name__ == "__main__":
    detect_and_register()
