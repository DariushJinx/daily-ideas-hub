import os
import json
from datetime import datetime
import notifier
import storage

def run_weekly_review():
    data = storage.load_data()
    shortlist = data.get("shortlist", [])
    
    if not shortlist:
        msg = (
            "📊 <b>گزارش و غربالگری روز هفتم (Weekly Review)</b>\n\n"
            "در ۶ روز گذشته هیچ ایده‌ای توسط شما نشانه‌گذاری (Like) نشده بود.\n"
            "می‌توانید آرشیو روزهای گذشته را مرور کرده یا منتظر ایده‌های هفته جدید باشید."
        )
        notifier.send_telegram(msg)
        notifier.send_windows_toast("گزارش هفتگی ایده‌ها", "هیچ ایده‌ای در لیست منتخب‌های این هفته ثبت نشده بود.")
        return False

    # Format the review message
    review_text = (
        f"🏆 <b>جلسه ارزیابی و غربالگری هفتگی (روز هفتم)</b>\n"
        f"📅 تاریخ: {datetime.now().strftime('%Y-%m-%d')}\n\n"
        f"در طول ۶ روز گذشته شما <b>{len(shortlist)} ایده</b> را برای بررسی نهایی پسندیدید:\n\n"
    )

    inline_buttons = []

    for i, item in enumerate(shortlist, 1):
        review_text += (
            f"<b>{i}. {item['title']}</b>\n"
            f"🔗 <a href='{item['url']}'>مشاهده مرجع خارجی</a>\n"
            f"📝 خلاصه: {item['summary']}\n"
            f"📅 تاریخ ثبت: {item['date']}\n\n"
        )
        # Add a selection button for each idea
        inline_buttons.append([
            {"text": f"🚀 انتخاب نهایی برای پیاده‌سازی: {item['title'][:25]}...", "callback_data": f"build_{item['id']}"}
        ])

    review_text += (
        "💡 <b>اکنون کدام ایده را برای پیاده‌سازی انتخاب می‌کنید؟</b>\n"
        "با کلیک روی دکمه زیر، ایده برنده وارد تابلوی «در حال ساخت» می‌شود و باقی موارد برای همیشه در آرشیو در دسترس خواهند ماند."
    )

    reply_markup = {"inline_keyboard": inline_buttons}
    
    notifier.send_telegram(review_text, reply_markup=reply_markup)
    notifier.send_windows_toast(
        "جلسه بررسی هفتگی ایده‌ها (روز ۷) 🎯",
        f"{len(shortlist)} ایده منتخب آماده غربالگری و انتخاب برای پیاده‌سازی هستند!"
    )
    return True

if __name__ == "__main__":
    run_weekly_review()
