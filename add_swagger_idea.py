import sys
sys.stdout.reconfigure(encoding='utf-8')
import storage
import notifier

success, msg = storage.add_to_shortlist(
    idea_id="swagger-to-frontend",
    title="سامانه تولید خودکار کدها و تایپ‌های فرانت‌اند از روی Swagger (Orval / Fern)",
    date_str="2026-10-13",
    summary="تولید خودکار هوک‌های React Query، کلاینت‌های Axios، تایپ‌های TypeScript و اسکیماهای Zod مستقیماً از روی لینک Swagger/OpenAPI | کاهش ۸۰٪ زمان هماهنگی بین فرانت‌اند و بک‌اند | مراجع خارجی: Orval.dev و Buildwithfern.com",
    url="https://orval.dev"
)

print("Add status:", success, msg)

tg_text = (
    "⭐️ <b>ایده با موفقیت به لیست منتخب‌های هفتگی اضافه شد!</b>\n\n"
    "📌 <b>سامانه تبدیل خودکار Swagger به کدهای فرانت‌اند (Swagger to Frontend SDK)</b>\n"
    "🏷 <b>نوع ایده:</b> Developer Tool / B2B Micro-SaaS\n"
    "🔗 <b>مراجع خارجی:</b> <a href='https://orval.dev'>Orval.dev</a> | <a href='https://buildwithfern.com'>Fern</a>\n"
    "💡 <b>مکانیزم:</b> دریافت لینک یا فایل Swagger/OpenAPI از برنامه‌نویس بک‌اند و تولید خودکار تایپ‌های TypeScript، هوک‌های React Query، سرویس‌های Axios و دیتای ساختگی (Mock) در ۱ ثانیه برای تیم فرانت‌اند.\n\n"
    "📋 این ایده در تابلوی هفتگی ذخیره شد و در روز هفتم برای ارزیابی و انتخاب نهایی پیاده‌سازی ارائه می‌شود."
)

notifier.send_telegram(tg_text)
notifier.send_windows_toast("⭐️ ایده منتخب ذخیره شد", "ایده تبدیل سواگر به فرانت‌اند به لیست هفتگی اضافه شد.")
print("Notification dispatched.")
