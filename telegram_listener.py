import time
import json
import urllib.request
import urllib.parse
from datetime import datetime
import notifier
import storage
import weekly_digest

IDEAS_CATALOG = {
    # Day 2 Ideas (2026-10-13)
    "2026-10-13_1": {
        "title": "فرم‌ساز مدرن با اعلان در تلگرام و ایتا (Tally)",
        "type": "ابزار بدون کد / فرم‌ساز تعاملی (No-Code Form Builder)",
        "url": "https://tally.so",
        "summary": "فرم‌ساز مدرن با ارسال لحظه‌ای لیدها به بات تلگرام و پیامک ادمین | +۶۰۰ هزار کاربر جهانی (رضایت ۴.۹/۵) | پتانسیل: ۱۰ میلیون ت/ماه"
    },
    "2026-10-13_2": {
        "title": "سامانه پایش آپ‌تایم و درگاه پرداخت بانکی (BetterStack)",
        "type": "ابزار مانیتورینگ وب‌مسترها (DevOps Monitoring SaaS)",
        "url": "https://betterstack.com",
        "summary": "پایش ۶۰ ثانیه‌ای سرور و درگاه پرداخت شاپرک با تماس صوتی و پیامک اضطراری | +۲ میلیون وب‌سایت | پتانسیل: ۱۵ تا ۲۵ میلیون ت/ماه"
    },
    "2026-10-13_3": {
        "title": "بازتولید هوشمند محتوای تک برای لینکدین/تلگرام (Taplio)",
        "type": "ابزار هوشمند تولید محتوای مارکتینگ (AI B2B Content SaaS)",
        "url": "https://taplio.com",
        "summary": "استخراج ترندهای ردیت/توییتر و بازتولید فارسی با هوش مصنوعی برای کانال‌های تلگرام و لینکدین | +۱۰۰ هزار کاربر | پتانسیل: ۹ میلیون ت/ماه"
    },
    # Generic fallbacks
    "1": {
        "title": "فرم‌ساز مدرن با اعلان در تلگرام و ایتا (Tally)",
        "type": "No-Code Form Builder",
        "url": "https://tally.so",
        "summary": "فرم‌ساز مدرن با نوتیفیکیشن تلگرام برای ادمین‌ها | ۶۰۰k کاربر"
    },
    "2": {
        "title": "سامانه پایش آپ‌تایم و درگاه پرداخت بانکی (BetterStack)",
        "type": "DevOps Monitoring SaaS",
        "url": "https://betterstack.com",
        "summary": "پایش ۶۰ ثانیه‌ای سرور و درگاه پرداخت با تماس و پیامک | ۲M سایت"
    },
    "3": {
        "title": "بازتولید هوشمند محتوای تک برای لینکدین/تلگرام (Taplio)",
        "type": "AI Content SaaS",
        "url": "https://taplio.com",
        "summary": "بازتولید فارسی هوشمند اخبار و ترندهای تک برای تلگرام و لینکدین"
    }
}

def answer_callback(token: str, callback_id: str, text: str, show_alert: bool = False):
    url = f"https://api.telegram.org/bot{token}/answerCallbackQuery"
    payload = {
        "callback_query_id": callback_id,
        "text": text,
        "show_alert": show_alert
    }
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"Error answering callback: {e}")

def run_listener():
    cfg = notifier.load_config()
    token = cfg.get("telegram", {}).get("bot_token")
    if not token:
        print("Bot token not found in config.json")
        return

    print("Starting Telegram interactive button listener...")
    offset = None

    while True:
        try:
            url = f"https://api.telegram.org/bot{token}/getUpdates?timeout=20"
            if offset:
                url += f"&offset={offset}"

            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
                updates = data.get("result", [])

                for upd in updates:
                    offset = upd["update_id"] + 1

                    # Handle Callback Query (Button clicks)
                    if "callback_query" in upd:
                        cq = upd["callback_query"]
                        cq_id = cq["id"]
                        cb_data = cq.get("data", "")
                        from_user = cq["from"].get("first_name", "کاربر")
                        chat_id = cq["message"]["chat"]["id"]

                        print(f"Callback received: {cb_data} from {from_user}")

                        if cb_data.startswith("like_"):
                            idea_key = cb_data.replace("like_", "")
                            idx = idea_key.rsplit("_", 1)[-1] if "_" in idea_key else idea_key
                            info = IDEAS_CATALOG.get(idx, {
                                "title": f"ایده {idea_key}",
                                "type": "Micro-SaaS / Web Tool",
                                "url": "https://www.producthunt.com",
                                "summary": "ایده ذخیره‌شده از گزارش روزانه"
                            })

                            success, msg = storage.add_to_shortlist(
                                idea_id=idea_key,
                                title=f"{info['title']} ({info.get('type', '')})",
                                date_str=idea_key.rsplit("_", 1)[0] if "_" in idea_key else datetime.now().strftime("%Y-%m-%d"),
                                summary=info["summary"],
                                url=info["url"]
                            )

                            if success:
                                answer_callback(token, cq_id, f"⭐️ {msg}", show_alert=True)
                                notifier.send_windows_toast("⭐️ ایده منتخب ذخیره شد", f"'{info['title']}' به لیست منتخب‌های هفتگی اضافه شد.")
                                confirm_msg = (
                                    f"✅ <b>ایده با موفقیت ذخیره شد!</b>\n\n"
                                    f"📌 <b>{info['title']}</b>\n"
                                    f"در روز هفتم، تمام ایده‌های لایک‌شده شما با هم مقایسه شده و برای پیاده‌سازی نهایی انتخاب خواهند شد."
                                )
                                notifier.send_telegram(confirm_msg)
                            else:
                                answer_callback(token, cq_id, f"ℹ️ این ایده قبلاً در لیست منتخب‌ها ذخیره شده است.", show_alert=True)
                                notifier.send_telegram(f"ℹ️ <b>قبلاً ثبت شده:</b> ایده <b>{info['title']}</b> هم‌اکنون در لیست منتخب‌های این هفته شما موجود است.\n(برای دیدن همه موارد دستور /list را بفرستید)")

                        elif cb_data.startswith("build_"):
                            idea_id = cb_data.replace("build_", "")
                            success, msg = storage.select_for_implementation(idea_id)
                            answer_callback(token, cq_id, "🚀 ایده انتخاب شد!", show_alert=True)

                            win_msg = (
                                f"🎉 <b>تبریک! ایده برای پیاده‌سازی انتخاب شد</b> 🚀\n\n"
                                f"{msg}\n\n"
                                "این ایده در فایل <code>pipeline.md</code> در تابلوی 'در حال پیاده‌سازی' قرار گرفت و باقی موارد در آرشیو بایگانی شدند.\n"
                                "اکنون می‌توانیم فاز توسعه فنی (MVP) را با هم استارت بزنیم!"
                            )
                            notifier.send_telegram(win_msg)
                            notifier.send_windows_toast("🚀 شروع فاز پیاده‌سازی!", f"ایده برای پیاده‌سازی انتخاب شد. تابلوی Kanban به‌روز شد.")

                        elif cb_data == "view_shortlist":
                            stored = storage.load_data()
                            shortlist = stored.get("shortlist", [])
                            if not shortlist:
                                answer_callback(token, cq_id, "هنوز ایده‌ای در این هفته لایک نشده است.", show_alert=True)
                                notifier.send_telegram("📋 <b>لیست منتخب‌های این هفته خالی است.</b>\nروی دکمه '⭐️ پسندیدم' زیر هر ایده کلیک کنید تا به این لیست اضافه شود.")
                            else:
                                text = f"📋 <b>لیست ایده‌های منتخب این هفته ({len(shortlist)} مورد):</b>\n\n"
                                for i, itm in enumerate(shortlist, 1):
                                    text += f"{i}. <b>{itm['title']}</b>\n🔗 <a href='{itm['url']}'>مشاهده مرجع</a>\n\n"
                                text += "در روز هفتم، از بین این موارد، برنده نهایی را برای ساخت انتخاب خواهیم کرد."
                                answer_callback(token, cq_id, f"📋 {len(shortlist)} ایده منتخب دارید", show_alert=False)
                                notifier.send_telegram(text)

                    # Handle Text Commands
                    elif "message" in upd and "text" in upd["message"]:
                        msg_text = upd["message"]["text"].strip()
                        if msg_text in ["/list", "/shortlist"]:
                            stored = storage.load_data()
                            shortlist = stored.get("shortlist", [])
                            if not shortlist:
                                notifier.send_telegram("📋 لیست منتخب‌های شما در حال حاضر خالی است.")
                            else:
                                text = f"📋 <b>ایده‌های منتخب تا این لحظه ({len(shortlist)} مورد):</b>\n\n"
                                for i, itm in enumerate(shortlist, 1):
                                    text += f"{i}. <b>{itm['title']}</b> ({itm['date']})\n🔗 {itm['url']}\n\n"
                                notifier.send_telegram(text)

                        elif msg_text in ["/review", "/day7"]:
                            notifier.send_telegram("⏳ در حال تولید گزارش روز هفتم و مقایسه ایده‌های منتخب...")
                            weekly_digest.run_weekly_review()

                        elif msg_text == "/pipeline":
                            stored = storage.load_data()
                            in_prog = stored.get("in_progress", [])
                            archived = stored.get("archived", [])
                            text = (
                                f"📊 <b>وضعیت پایپ‌لاین ایده‌ها:</b>\n\n"
                                f"🎯 در حال پیاده‌سازی: {len(in_prog)} مورد\n"
                                f"⭐️ منتخب این هفته: {len(stored.get('shortlist', []))} مورد\n"
                                f"📦 بایگانی‌شده: {len(archived)} مورد\n\n"
                                "فایل کامل Kanban در پروژه با نام <code>pipeline.md</code> موجود است."
                            )
                            notifier.send_telegram(text)

                        # Divar Car Inspector Feature
                        elif "divar.ir" in msg_text or msg_text.startswith("/car "):
                            import sys
                            car_inspector_path = r"C:\Users\salimi\.gemini\antigravity\scratch\divar-car-inspector"
                            if car_inspector_path not in sys.path:
                                sys.path.append(car_inspector_path)
                            import divar_scraper
                            import inspector_engine

                            url_or_token = msg_text.replace("/car", "").strip()
                            notifier.send_telegram("🔍 <b>در حال واکشی آگهی دیوار و آنالیز مشخصات و تصاویر...</b>")
                            
                            try:
                                post = divar_scraper.fetch_divar_post(url_or_token)
                                rep = inspector_engine.analyze_car_post(post)
                                
                                report_text = (
                                    f"🚗 <b>نتیجه راستی‌آزمایی آگهی: {rep['title'][:40]}</b>\n"
                                    f"💰 قیمت: <b>{rep['price']}</b> | 📸 عکس‌ها: <b>{rep['image_count']} عدد</b>\n\n"
                                    f"🎯 <b>شاخص ریسک معامله:</b> {rep['risk_level']} (نمره: <b>{rep['risk_score']}/۱۰</b>)\n\n"
                                )
                                if rep.get("verified_points"):
                                    report_text += "✅ <b>شواهد تأیید شده:</b>\n"
                                    for v in rep["verified_points"]:
                                        report_text += f"  • {v}\n"
                                    report_text += "\n"
                                if rep.get("suspicious_points"):
                                    report_text += "⚠️ <b>مغایرت‌ها و نقاط مشکوک:</b>\n"
                                    for s in rep["suspicious_points"]:
                                        report_text += f"  • {s}\n"
                                    report_text += "\n"
                                if rep.get("buyer_questions"):
                                    report_text += "❓ <b>سوالات مهم برای تماس با فروشنده:</b>\n"
                                    for q in rep["buyer_questions"]:
                                        report_text += f"  • {q}\n"
                                    report_text += "\n"
                                report_text += "🛡 <i>این گزارش بر اساس مقایسه هوشمند ادعاهای آگهی با تصاویر است.</i>"
                                
                                notifier.send_telegram(report_text)
                                notifier.send_windows_toast("آنالیز خودرو دیوار آماده شد 🚗", f"{rep['title'][:30]}: {rep['risk_level']}")
                            except Exception as ex:
                                notifier.send_telegram(f"❌ خطا در پردازش آگهی: {ex}")

        except Exception as e:
            time.sleep(3)

if __name__ == "__main__":
    run_listener()
