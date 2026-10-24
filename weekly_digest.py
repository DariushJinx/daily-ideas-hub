import os
import sys
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import json
from datetime import datetime
import notifier
import storage

def run_weekly_review(week_num: int = 1, save_archive: bool = True):
    data = storage.load_data()
    shortlist = data.get("shortlist", [])
    today = datetime.now().strftime("%Y-%m-%d")
    
    if not shortlist:
        msg = (
            f"📊 <b>جلسه غربالگری هفتگی (هفته {week_num} - روز هفتم)</b>\n\n"
            "در ۶ روز گذشته هیچ ایده‌ای توسط شما نشانه‌گذاری (Like) نشده بود.\n"
            "می‌توانید آرشیو روزهای گذشته را مرور کرده یا منتظر شروع هفته جدید باشید."
        )
        notifier.send_telegram(msg)
        notifier.send_windows_toast("گزارش هفتگی ایده‌ها", "هیچ ایده‌ای در لیست منتخب‌های این هفته ثبت نشده بود.")
        if save_archive:
            md_content = f"# گزارش و غربالگری هفتگی - هفته {week_num} ({today})\n\nدر ۶ روز گذشته هیچ ایده‌ای نشانه‌گذاری نشده بود.\n"
            notifier.save_to_archive(md_content)
        return False

    # Format the review message
    review_text = (
        f"🏆 <b>جلسه ارزیابی و غربالگری ایده‌ها (پایان هفته {week_num} / روز هفتم)</b>\n"
        f"📅 تاریخ: {today}\n\n"
        f"در طول ۶ روز گذشته شما <b>{len(shortlist)} ایده تاپ</b> را پسندیدید:\n\n"
    )

    inline_buttons = []

    for i, item in enumerate(shortlist, 1):
        clean_title = item['title'].split('(')[0].strip()
        review_text += (
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>{i}. {item['title']}</b>\n"
            f"🔗 <a href='{item['url']}'>مشاهده مرجع خارجی</a>\n"
            f"📝 خلاصه: {item['summary']}\n"
            f"📅 تاریخ ثبت: {item['date']}\n\n"
        )
        # Ensure callback_data is well under Telegram's 64-byte limit
        cb_id = str(item['id'])[:40]
        inline_buttons.append([
            {"text": f"🚀 ساخت این ایده: {clean_title[:28]}", "callback_data": f"build_{cb_id}"}
        ])

    review_text += (
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💡 <b>اکنون کدام ایده را برای پیاده‌سازی انتخاب می‌کنید؟</b>\n"
        "با کلیک روی دکمه زیر، ایده برنده وارد تابلوی «در حال ساخت» (pipeline.md) می‌شود و باقی موارد در آرشیو برای آینده حفظ می‌گردند.\n"
        "از فردا هفته جدید با ایده‌های کاملاً تازه و متنوع آغاز خواهد شد!"
    )

    reply_markup = {"inline_keyboard": inline_buttons}
    
    # Send message in chunks if necessary (Telegram limit: 4096 characters)
    if len(review_text) > 4000:
        # Send first part without buttons, second part with buttons
        mid = review_text.rfind("━━━━━━━━━━━━━━━━━━━━", 0, 3800)
        if mid == -1:
            mid = 3800
        part1 = review_text[:mid]
        part2 = review_text[mid:]
        notifier.send_telegram(part1)
        tg_ok = notifier.send_telegram(part2, reply_markup=reply_markup)
    else:
        tg_ok = notifier.send_telegram(review_text, reply_markup=reply_markup)

    notifier.send_windows_toast(
        f"جلسه بررسی هفتگی ایده‌ها (هفته {week_num}) 🎯",
        f"{len(shortlist)} ایده منتخب آماده غربالگری و انتخاب برای پیاده‌سازی هستند!"
    )

    # Save Markdown Archive
    if save_archive:
        md_content = f"# 🏆 گزارش و غربالگری هفتگی (هفته {week_num}) - {today}\n\n---\n\n"
        md_content += f"در طول ۶ روز گذشته، تعداد {len(shortlist)} ایده در لیست منتخب‌ها ذخیره شدند:\n\n"
        for i, item in enumerate(shortlist, 1):
            md_content += f"### {i}. [{item['title']}]({item['url']})\n"
            md_content += f"- **خلاصه:** {item['summary']}\n"
            md_content += f"- **تاریخ ثبت:** {item['date']}\n"
            md_content += f"- **شناسه:** `{item['id']}`\n\n"
        notifier.save_to_archive(md_content, filename=f"{today}_review_week{week_num}.md")

    return tg_ok

if __name__ == "__main__":
    w_num = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    run_weekly_review(w_num)
