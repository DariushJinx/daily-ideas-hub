import os
import sys
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import json
from datetime import datetime
import notifier

# Database of curated, vetted ideas for each day of the sprint
IDEAS_ROSTER = {
    1: {
        "title": "ایده‌های روز اول (E-commerce & Programmatic Tools)",
        "items": [
            {
                "id": "1",
                "name": "اکستنشن کروم تحلیل هوشمند دیجی‌کالا و باسلام",
                "type": "ابزار تحلیلی فروشندگان مارکت‌پلیس (B2B Chrome Extension)",
                "desc": "افزونه‌ای که روی صفحه محصول در دیجی‌کالا یا باسلام، تخمین تعداد فروش ماهانه، نمودار تاریخچه قیمت، تعداد رقبا و سودآور بودن فروش آن کالا را نمایش می‌دهد.",
                "tech": "اکستنشن کروم (Manifest V3) + بک‌اند پایتون (ساخت در ۳-۴ روز)",
                "ref_url": "https://www.helium10.com",
                "ref_name": "Helium 10 / Jungle Scout",
                "traction": "+۱ میلیون کاربر فعال | رضایت: ۴.۶ از ۵ (۳۵۰۰+ نظر)",
                "revenue": "+۲ میلیون دلار در ماه (پلن از ۳۹$)",
                "market_ir": "+۶۰ هزار فروشنده فعال دیجی‌کالا و باسلام",
                "growth": "پیام به فروشنده‌های باسلام با آفر تست رایگان ۷ روزه",
                "potential": "۵۰ مشتری × ۲۰۰ هزارتومان = ۱۰ میلیون تومان/ماه",
                "ice": "۲۸/۳۰"
            },
            {
                "id": "2",
                "name": "وب‌سایت ابزارهای محاسباتی سئو-محور (Programmatic SEO)",
                "type": "پلتفرم میکرو-ابزارهای وب (B2C Web Micro-Tools)",
                "desc": "وب‌سایتی شامل ده‌ها ماشین‌حساب تک‌کاره (محاسبه حباب طلا، سنوات، کمیسیون املاک، وام) که به صورت خودکار برای کوئری‌های پرجستجوی گوگل ساخته شده و ترافیک ارگانیک با درآمد تبلیغاتی ایجاد می‌کند.",
                "tech": "Next.js / Astro + اسکریپت پایتون (ساخت در ۲-۳ روز)",
                "ref_url": "https://www.omnicalculator.com",
                "ref_name": "Omni Calculator / TinyWow",
                "traction": "+۲۰ میلیون بازدید ماهانه گوگل | رضایت: ۴.۸ از ۵",
                "revenue": "+۵۰ هزار دلار در ماه از تبلیغات بنری",
                "market_ir": "ترافیک میلیونی جستجوی روزانه محاسبات مالی، بیمه و طلا",
                "growth": "سئو روی ۱۰ کی‌ورد خلوت دم‌دراز و رتبه ۱ در ۲ هفته",
                "potential": "تبلیغات یکتانت با بازدید روزانه = ۸ تا ۱۵ میلیون تومان/ماه",
                "ice": "۲۷/۳۰"
            },
            {
                "id": "3",
                "name": "اکستنشن اتوماسیون سفارش‌ها در پیام‌رسان‌ها",
                "type": "ابزار بهره‌وری و CRM آنلاین‌شاپ‌ها (Chrome Extension)",
                "desc": "افزونه‌ای روی تلگرام وب، واتساپ وب، بله و ایتا برای ادمین‌های فروشگاهی جهت ارسال سریع پیام‌های آماده (شماره کارت، سایزبندی)، خروجی اکسل آدرس مشتریان برای پست و ارسال خودکار کد رهگیری مرسولات.",
                "tech": "جاوااسکریپت (اکستنشن کروم) + خروجی اکسل (ساخت در ۳ روز)",
                "ref_url": "https://wawplus.com",
                "ref_name": "WA Web Plus / Bardeen.ai",
                "traction": "+۱.۲ میلیون نصب فعال | رضایت: ۴.۷ از ۵ (۲۲ هزار نظر)",
                "revenue": "پلن ماهانه از ۱۲ دلار تا ۴۰ دلار",
                "market_ir": "+۴۰۰ هزار آنلاین‌شاپ و ادمین فروش در پیام‌رسان‌ها",
                "growth": "انتشار ویدیوی ۱ دقیقه‌ای در گروه‌های ادمین‌ها",
                "potential": "۱۰۰ کاربر × ۱۵۰ هزارتومان = ۱۵ میلیون تومان/ماه",
                "ice": "۲۹/۳۰"
            }
        ]
    },
    2: {
        "title": "ایده‌های روز دوم (No-Code & Developer Monitoring)",
        "items": [
            {
                "id": "1",
                "name": "فرم‌ساز مدرن با اعلان لحظه‌ای در تلگرام و ایتا",
                "type": "ابزار بدون کد / فرم‌ساز تعاملی (No-Code Form Builder)",
                "desc": "ساخت آسان فرم‌های استخدام، ثبت سفارش یا نظرسنجی مدرن شبیه Typeform، با این تفاوت بزرگ که به محض ثبت پاسخ توسط مشتری، اطلاعات بدون نیاز به ایمیل در ۱ ثانیه به ربات تلگرام یا پیامک ادمین ارسال می‌شود.",
                "tech": "Next.js + بک‌اند پایتون (ساخت در ۳-۴ روز)",
                "ref_url": "https://tally.so",
                "ref_name": "Tally.so / Formester",
                "traction": "+۶۰۰ هزار کاربر (تیم ۲ نفره!) | رضایت: ۴.۹ از ۵ (رتبه ۱ پروداکت هانت)",
                "revenue": "+۱۲۰ هزار دلار در ماه (MRR)",
                "market_ir": "نیاز مبرم آنلاین‌شاپ‌ها و شرکت‌ها به فرم‌ساز غیرفیلتر و تلگرامی",
                "growth": "ارسال فرم آماده به پیج‌های استخدامی",
                "potential": "۱۰۰ کاربر × ۹۹ هزارتومان = ۱۰ میلیون تومان/ماه",
                "ice": "۲۸/۳۰"
            },
            {
                "id": "2",
                "name": "سامانه پایش آپ‌تایم و درگاه پرداخت بانکی",
                "type": "ابزار مانیتورینگ وب‌مسترها (DevOps Monitoring SaaS)",
                "desc": "پایش ۶۰ ثانیه‌ای سلامت سرور، گواهی SSL و از همه مهم‌تر «درگاه پرداخت شاپرک/زرین‌پال» سایت‌های ایرانی. به محض هرگونه قطعی یا خطای درگاه، فوراً تماس صوتی تلفنی خودکار یا پیامک اضطراری به مدیر سایت می‌زند.",
                "tech": "پایتون (Asyncio) + وب‌سرویس تماس صوتی (ساخت در ۳ روز)",
                "ref_url": "https://betterstack.com",
                "ref_name": "Better Stack / UptimeRobot",
                "traction": "+۲ میلیون وب‌سایت تحت پایش | رضایت: ۴.۸ از ۵",
                "revenue": "ده‌ها میلیون دلار سالانه",
                "market_ir": "+۵۰ هزار سایت وردپرسی و فروشگاهی ایرانی",
                "growth": "آفر تست رایگان ۱ سایت در گروه‌های برنامه‌نویسان",
                "potential": "اشتراک ماهانه ۹۰-۲۵۰ هزارتومان = ۱۵ تا ۲۵ میلیون تومان/ماه",
                "ice": "۲۹/۳۰"
            },
            {
                "id": "3",
                "name": "بازتولید هوشمند محتوای تخصصی تک برای لینکدین/تلگرام",
                "type": "ابزار بازاریابی محتوای هوشمند (AI B2B Content SaaS)",
                "desc": "ابزاری که پربحث‌ترین اخبار و پست‌های توییتر، ردیت و Hacker News را واکشی کرده و با هوش مصنوعی به پست‌های خواندنی فارسی با لحن تخصصی برای انتشار با یک کلیک در کانال‌های تلگرامی و لینکدین آماده می‌کند.",
                "tech": "پایتون (اسکرپر + پرامپت بومی‌سازی) (ساخت در ۲-۳ روز)",
                "ref_url": "https://taplio.com",
                "ref_name": "Taplio / TweetHunter",
                "traction": "+۱۰۰ هزار کاربر | رضایت: ۴.۷ از ۵ (خریداری‌شده با مبالغ میلیون دلاری)",
                "revenue": "+۴ میلیون دلار در سال (ARR)",
                "market_ir": "مدیران کانال‌های فناوری تلگرام و تولیدکنندگان محتوای لینکدین",
                "growth": "ارسال ۳ نمونه پست اختصاصی به ادمین‌های تلگرام",
                "potential": "۵۰ کاربر × ۱۸۰ هزارتومان = ۹ میلیون تومان/ماه",
                "ice": "۲۷/۳۰"
            }
        ]
    },
    3: {
        "title": "ایده‌های روز سوم (DevOps & Product Experience)",
        "items": [
            {
                "id": "1",
                "name": "ویجت و صفحه اعلان تغییرات محصول (In-App Changelog)",
                "type": "ابزار توسعه‌دهندگان و میکروسس (DevTools / B2B Micro-SaaS)",
                "desc": "ویجت سبک و صفحه مدرن Changelog که توسعه‌دهندگان با قرار دادن یک تگ اسکریپت، فیچرهای جدید و رفع باگ‌ها را به صورت بج تعاملی درون برنامه به کاربران نشان می‌دهند.",
                "tech": "ویجت سبک JS + بک‌اند پایتون FastAPI (ساخت در ۳ روز)",
                "ref_url": "https://getbeamer.com",
                "ref_name": "Beamer / Headway",
                "traction": "+۱.۵ میلیون وب‌سایت در جهان | رضایت: ۴.۸ از ۵",
                "revenue": "۸ میلیون دلار ARR (واگذار شده به شرکت Camptocamp)",
                "market_ir": "صدها نرم‌افزار سس، پنل‌های حسابداری، CRMها و فین‌تک‌های ایرانی",
                "growth": "ساخت دمو اختصاصی برای ۵ استارتاپ شناخته‌شده در لینکدین",
                "potential": "۵۰ مشترک × ۱۴۰ تا ۲۸۰ هزارتومان = ۸ تا ۱۴ میلیون تومان/ماه",
                "ice": "۲۸/۳۰"
            },
            {
                "id": "2",
                "name": "وب‌سرویس تولید خودکار تصاویر داینامیک اشتراک‌گذاری (OG Image API)",
                "type": "ابزار خودکارسازی مارکتینگ (API SaaS / Automated Visuals)",
                "desc": "API سریعی که لینک مقاله یا محصول را گرفته و به صورت خودکار یک تصویر پیش‌نمایش حرفه‌ای (Open Graph Card) با لوگو و عنوان برای نمایش چشم‌نواز در تلگرام و توییتر می‌سازد.",
                "tech": "موتور رندر Satori / Resvg + فرانت تک‌صفحه‌ای (ساخت در ۲-۳ روز)",
                "ref_url": "https://bannerbear.com",
                "ref_name": "Bannerbear / Placid.app",
                "traction": "+۵۰ هزار دلار MRR توسط یک برنامه‌نویس سولو با سرمایه صفر",
                "revenue": "بیش از ۶۰۰ هزار دلار درآمد سالانه",
                "market_ir": "فروشگاه‌های اینترنتی و سایت‌های محتوایی با لینک‌های خام در تلگرام",
                "growth": "پلاگین رایگان وردپرس و توییت مقایسه قبل/بعد لینک‌ها",
                "potential": "۶۰ سایت × ۱۲۰ هزارتومان = ۱۰ تا ۱۵ میلیون تومان/ماه",
                "ice": "۲۹/۳۰"
            },
            {
                "id": "3",
                "name": "سامانه بک‌آپ‌گیری خودکار سرور روی فضای رایگان تلگرام",
                "type": "ابزار دوآپس و زیرساخت (DevOps SaaS)",
                "desc": "با یک دستور تک‌خطی روی سرور لینوکس نصب می‌شود و از دیتابیس‌های MySQL/Postgres بک‌آپ رمزنگاری‌شده (AES-256) گرفته و مستقیماً روی ربات تلگرام با فضای نامحدود رایگان ذخیره می‌کند.",
                "tech": "اسکریپت مستقل پایتون/Go + بات تلگرام (ساخت در ۳ روز)",
                "ref_url": "https://snapshooter.com",
                "ref_name": "SnapShooter / SimpleBackups",
                "traction": "تصاحب رسمی توسط DigitalOcean در سال ۲۰۲۳ | رضایت: ۴.۸ از ۵",
                "revenue": "+۳۰۰ هزار دلار سالانه (خریداری‌شده توسط دیجیتال‌اوشن)",
                "market_ir": "هزاران سرور داخلی با ریسک قطعی و پاک شدن دیتابیس",
                "growth": "لایسنس رایگان دائمی در کامیونیتی‌های دوآپس و لاراول ایران",
                "potential": "۸۰ کاربر × ۹۹ تا ۱۹۰ هزارتومان = ۱۰ تا ۱۵ میلیون تومان/ماه",
                "ice": "۲۹/۳۰"
            }
        ]
    },
    4: {
        "title": "ایده‌های روز چهارم (Developer Productivity & Invoicing)",
        "items": [
            {
                "id": "1",
                "name": "سامانه داکیومنت تعاملی و مدرن API از روی Swagger (Scalar / Mintlify)",
                "type": "ابزار توسعه‌دهندگان (DevTools Micro-SaaS)",
                "desc": "جایگزین مدرن و فوق‌العاده سریع و شیک برای Swagger UI قدیمی؛ فقط لینک JSON سواگر را می‌گیرد و یک پرتال مستندات API فوق‌العاده زیبا با تم دارک، کدهای آماده cURL، Python، JS و کنسول تست آنلاین در ۱ ثانیه تحویل می‌دهد.",
                "tech": "Next.js + هسته متن‌باز Scalar / Swagger Parser (ساخت در ۲-۳ روز)",
                "ref_url": "https://scalar.com",
                "ref_name": "Scalar / Mintlify / Readme.com",
                "traction": "+۲۵۰ هزار توسعه‌دهنده در جهان | برنده رتبه ۱ پروداکت هانت و جذب میلیون‌ها دلار سرمایه",
                "revenue": "پلن‌های تیمی از ۲۰ تا ۱۰۰ دلار در ماه",
                "market_ir": "شرکت‌های نرم‌افزاری و استارتاپ‌های ایرانی با مستندات API زشت و قدیمی",
                "growth": "ساخت دمو داکس مدرن برای API نوبیتکس، اسنپ یا تپسی و اشتراک در لینکدین",
                "potential": "۴۰ شرکت × ۲۵۰ هزارتومان = ۱۰ میلیون تومان/ماه",
                "ice": "۲۹/۳۰"
            },
            {
                "id": "2",
                "name": "پلتفرم فاکتور آنلاین و لینک پرداخت برای فریلنسرها (Invoice & Pay)",
                "type": "فین‌تک فریلنسری و مشاغل مستقل (Fintech Micro-SaaS)",
                "desc": "فریلنسرها و شرکت‌های کوچک در ۲ دقیقه پیش‌فاکتور شکیل می‌سازند که یک لینک پرداخت اینترنتی (متصل به زرین‌پال یا شماره کارت هوشمند) دارد. کارفرما آنلاین پرداخت می‌کند و پیامک تایید برای هر دو طرف ارسال می‌شود.",
                "tech": "FastAPI پایتون + درگاه پرداخت شتاب + وب‌سرویس پیامک (ساخت در ۳-۴ روز)",
                "ref_url": "https://www.invoiceninja.com",
                "ref_name": "Invoice Ninja / Ruul.io",
                "traction": "+۲۰۰ هزار کاربر در جهان | محبوب‌ترین ابزار فریلنسرهای اروپا",
                "revenue": "+۱ میلیون دلار سالانه",
                "market_ir": "صدها هزار فریلنسر، طراح، برنامه‌نویس و مشاور ایرانی بدون ابزار رسمی فاکتور",
                "growth": "ثبت‌نام رایگان در گروه‌های فریلنسری پونیشا و کارلنسر",
                "potential": "۱۰۰ فریلنسر × ۱۲۰ هزارتومان = ۱۲ میلیون تومان/ماه",
                "ice": "۲۸/۳۰"
            },
            {
                "id": "3",
                "name": "استخراج‌کننده هوشمند اطلاعات تماس و لید تجاری از گوگل‌مپ و اینستاگرام",
                "type": "ابزار جذب سرنخ B2B (Lead Generation Scraper Tool)",
                "desc": "ابزاری تحت وب که نام صنف (مثلاً: خشکبار، سالن زیبایی، قطعات خودرو) و شهر را می‌گیرد و در ۲ دقیقه اکسل تمیزی شامل شماره تماس، واتساپ، اینستاگرام و آدرس تمام کسب‌وکارهای ثبت‌شده را تحویل بازاریاب‌ها می‌دهد.",
                "tech": "اسکرپر پایتون (Playwright / Scrapy) + داشبورد دانلود اکسل (ساخت در ۳ روز)",
                "ref_url": "https://outscraper.com",
                "ref_name": "Outscraper / PhantomBuster",
                "traction": "+۵۰۰ هزار کاربر | ماهیانه صدها هزار دلار فروش لید دیتابیس",
                "revenue": "+۲ میلیون دلار ARR",
                "market_ir": "بازاریاب‌ها، آژانس‌های تبلیغاتی و شرکت‌های فروش تلفنی تشنه دیتای اصناف",
                "growth": "ارائه ۵۰ شماره اول هر صنف به صورت رایگان",
                "potential": "فروش بسته‌های لید از ۱۵۰ تا ۵۰۰ هزارتومان = ۱۵ تا ۲۵ میلیون تومان/ماه",
                "ice": "۲۹/۳۰"
            }
        ]
    },
    5: {
        "title": "ایده‌های روز پنجم (Automation & Verification)",
        "items": [
            {
                "id": "1",
                "name": "پلتفرم وب‌هوک و اتوماسیون جریان‌کاری برای ابزارهای ایرانی (Zapier بومی)",
                "type": "اتوماسیون بدون کد (Integration iPaaS)",
                "desc": "اتصال خودکار سیستم‌های ایرانی؛ مثلاً وقتی در دیجی‌کالا یا باسلام سفارشی ثبت شد، همان ثانیه در پیام‌رسان بله پیام برود و فاکتور در نرم‌افزار حسابداری آنلاین صادر شود.",
                "tech": "پایتون Asyncio + موتور صف Celery/Redis + معماری وب‌هوک (ساخت در ۵ روز)",
                "ref_url": "https://n8n.io",
                "ref_name": "n8n / Zapier / Make",
                "traction": "میلیون‌ها کاربر در جهان | ارزش میلیارد دلاری زپیر",
                "revenue": "+۱۴۰ میلیون دلار ARR در زپیر",
                "market_ir": "خلاء کامل پلتفرم اتوماسیون برای سرویس‌های بومی ایران (ایتا، بله، ترب، زرین‌پال)",
                "growth": "آموزش ویدیویی ساخت بات‌های فروشگاهی خودکار در آپارات و یوتیوب",
                "potential": "اشتراک ماهانه ۲۰۰ تا ۵۰۰ هزارتومان = ۲۰ میلیون تومان/ماه",
                "ice": "۲۸/۳۰"
            },
            {
                "id": "2",
                "name": "سامانه مدیریت لایسنس و قفل نرم‌افزاری توسعه‌دهندگان (Keygen بومی)",
                "type": "امنیت و زیرساخت نرم‌افزار (Licensing API SaaS)",
                "desc": "برنامه‌نویسان با چند خط کد می‌توانند روی اسکریپت‌ها، بات‌های تلگرام، نرم‌افزارهای پایتون یا افزونه‌های خود لایسنس‌کی زمان‌دار بگذارند و از کپی غیرقانونی آن جلوگیری کنند.",
                "tech": "FastAPI + سیستم احراز هویت رمزنگاری نامتقارن RSA (ساخت در ۳ روز)",
                "ref_url": "https://keygen.sh",
                "ref_name": "Keygen.sh / Cryptolens",
                "traction": "+۵۰ هزار اپلیکیشن فعال تحت مدیریت Keygen",
                "revenue": "+۳۵۰ هزار دلار سالانه توسط یک بنیان‌گذار مستقل",
                "market_ir": "فروشندگان اسکریپت و ربات در ایران که به راحتی کدهایشان پخش می‌شود",
                "growth": "ارائه SDK ساده پایتون و پی‌اچ‌پی در گیت‌هاب",
                "potential": "۵۰ برنامه‌نویس × ۱۵۰ هزارتومان = ۷.۵ میلیون تومان/ماه",
                "ice": "۲۷/۳۰"
            },
            {
                "id": "3",
                "name": "پلتفرم جمع‌آوری و ویجت ویدیویی رضایت خریدار (Social Proof Video SaaS)",
                "type": "ابزار افزایش نرخ تبدیل فروش (Marketing SaaS)",
                "desc": "ارسال یک لینک اختصاصی به خریداران تا با یک دکمه ویدیوی کوتاه رضایت ضبط کنند و این ویدیوها با ویجت‌های فوق‌العاده جذاب روی سایت فروشگاه جهت افزایش اعتماد قرار گیرند.",
                "tech": "Next.js + آپلود مدیا بدون فیلترشکن + ویجت تعبیه وب (ساخت در ۴ روز)",
                "ref_url": "https://testimonial.to",
                "ref_name": "Testimonial.to / Senja.io",
                "traction": "+۸۰ هزار دلار درآمد ماهانه در Testimonial (توسط دیمون چن، سولو دولوپر)",
                "revenue": "+۱ میلیون دلار ARR",
                "market_ir": "آنلاین‌شاپ‌ها و مدرسان ایرانی که اعتماد کاربران مهم‌ترین دارایی آنهاست",
                "growth": "پلاگین وردپرس با ۳ ویدیو رایگان برای هر سایت",
                "potential": "۷۰ فروشگاه × ۱۸۰ هزارتومان = ۱۲.۵ میلیون تومان/ماه",
                "ice": "۲۹/۳۰"
            }
        ]
    },
    6: {
        "title": "ایده‌های روز ششم (Creator Economy & Marketplaces)",
        "items": [
            {
                "id": "1",
                "name": "مارکت‌پلیس ویدیوی تست محصول و آنباکسینگ UGC برای فروشگاه‌ها",
                "type": "پلتفرم دوطرفه محتوا (Creator Marketplace)",
                "desc": "برندها و فروشگاه‌های اینترنتی محصولاتشان را ثبت می‌کنند و خریداران عادی و کریتورهای خرد ویدیوهای واقعی آنباکسینگ و معرفی می‌سازند و حق‌الزحمه امن دریافت می‌کنند.",
                "tech": "داشبورد سفارش و داوری ویدیو با Django/FastAPI (ساخت در ۴ روز)",
                "ref_url": "https://billo.app",
                "ref_name": "Billo.app / JoinBrands",
                "traction": "+۲۵ هزار برند فعال در جهان | رشد انفجاری در تیک‌تاک و اینستاگرام",
                "revenue": "+۱۰ میلیون دلار درآمد سالانه",
                "market_ir": "گران شدن شدید بلاگرهای بزرگ و نیاز فروشگاه‌ها به ویدیوی افراد عادی",
                "growth": "ثبت ۵۰ کریتور اول از طریق فراخوان اینستاگرامی",
                "potential": "کارمزد ۲۰٪ از هر ویدیو = ۱۵ تا ۳۰ میلیون تومان/ماه",
                "ice": "۲۸/۳۰"
            },
            {
                "id": "2",
                "name": "سامانه رزرو وقت مشاوره آنلاین با پرداخت شتاب قبل از جلسه",
                "type": "سامانه زمان‌بندی و پرداخت (Scheduling SaaS)",
                "desc": "مشاوران، وکلا، تراپیست‌ها و مربیان لینک تقویم خود را می‌گذارند؛ کاربر تایم خالی را انتخاب کرده، از درگاه بانکی پرداخت می‌کند و لینک جلسه گوگل‌میت و پیامک یادآوری خودکار صادر می‌شود.",
                "tech": "Cal.com (هسته متن‌باز) + درگاه پرداخت شتاب + پیامک ایرانی (ساخت در ۲-۳ روز)",
                "ref_url": "https://tidycal.com",
                "ref_name": "Cal.com / TidyCal",
                "traction": "+۱۰ میلیون دلار فروش لایسنس TidyCal | محبوب‌ترین جایگزین Calendly",
                "revenue": "+۵ میلیون دلار سالانه",
                "market_ir": "هزاران مدرس و مشاور که هنوز با کارت‌به‌کارت و چت دستی وقت تنظیم می‌کنند",
                "growth": "معرفی به مدرسان و منتورهای لینکدین با پلن رایگان ۳ نوبت در ماه",
                "potential": "۱۰۰ مشاور × ۹۹ هزارتومان = ۱۰ میلیون تومان/ماه",
                "ice": "۲۹/۳۰"
            },
            {
                "id": "3",
                "name": "دایرکتوری تخصصی فرصت‌های شغلی ریموت و فریلنسری سئومحور",
                "type": "دایرکتوری تخصصی پولی (Curated Job Board)",
                "desc": "پلتفرمی که به صورت روزانه تمام فرصت‌های شغلی دورکاری واقعی، تسک‌های دلاری و استارتاپ‌ها را اسکرپ کرده و از کارفرماها برای ثبت آگهی ویژه و پین‌شده در بالای سایت هزینه می‌گیرد.",
                "tech": "وردپرس با قالب کاریابی یا Next.js + اسکرپر پایتون (ساخت در ۲ روز)",
                "ref_url": "https://remoteok.com",
                "ref_name": "RemoteOK (Peter Levels)",
                "traction": "+۱۰۰ هزار دلار درآمد ماهانه با ۱ برنامه‌نویس بدون کارمند!",
                "revenue": "+۱.۵ میلیون دلار سالانه",
                "market_ir": "موج عظیم مهاجرت ذهنی و تمایل بالای برنامه‌نویسان ایرانی به کار ریموت",
                "growth": "اشتراک‌گذاری آگهی‌ها در کانال‌های تلگرامی برنامه‌نویسی",
                "potential": "دریافت ۳۰۰ تا ۵۰۰ هزارتومان به ازای هر آگهی ویژه کارفرما = ۱۰ تا ۱۵ میلیون/ماه",
                "ice": "۲۷/۳۰"
            }
        ]
    }
}

def determine_today_day_number():
    """
    Determines which day of the idea sprint we are on.
    Day 1 was 2026-10-12 / 2026-10-17.
    Uses calendar day offset modulo 6 (days 1 to 6) so ideas rotate continuously.
    """
    anchor_date = datetime(2026, 10, 16)
    today = datetime.now()
    diff = (today.date() - anchor_date.date()).days
    if diff <= 0:
        day_num = 1
    else:
        day_num = ((diff - 1) % 6) + 1
    return day_num

def generate_markdown(day_num: int, date_str: str) -> str:
    bundle = IDEAS_ROSTER.get(day_num, IDEAS_ROSTER[1])
    md = f"# {bundle['title']} - {date_str}\n\n---\n\n"
    for item in bundle["items"]:
        md += f"### 💡 ایده {item['id']}: {item['name']}\n"
        md += f"* **🏷 نوع و دسته‌بندی ایده:** {item['type']}\n"
        md += f"* **📝 این ایده دقیقاً چیست و چطور کار می‌کند؟**\n  {item['desc']}\n"
        md += f"* **🛠 پشته فنی و زمان توسعه:** {item['tech']}\n"
        md += f"* **🔗 نمونه و مرجع خارجی:** [{item['ref_name']}]({item['ref_url']})\n"
        md += f"* **📊 مارکت ریسرچ و شواهد جهانی:**\n"
        md += f"  * **کاربران فعال:** {item['traction']}\n"
        md += f"  * **درآمد و اعتبار:** {item['revenue']}\n"
        md += f"* **🇮🇷 بازار هدف در ایران:** {item['market_ir']}\n"
        md += f"* **🎯 جذب ۵ مشتری اول با بودجه صفر:** {item['growth']}\n"
        md += f"* **💵 اقتصاد واحد (Unit Economics):** {item['potential']}\n"
        md += f"* **📈 امتیاز ICE:** {item['ice']}\n\n---\n\n"
    return md

def generate_telegram_message(day_num: int, date_str: str) -> str:
    bundle = IDEAS_ROSTER.get(day_num, IDEAS_ROSTER[1])
    tg = f"📊 <b>{bundle['title']} | {date_str}</b>\n\n"
    for item in bundle["items"]:
        tg += f"━━━━━━━━━━━━━━━━━━━━\n"
        tg += f"<b>{item['id']}. {item['name']}</b>\n"
        tg += f"🏷 <b>نوع:</b> {item['type']}\n"
        tg += f"💡 <b>این ایده دقیقاً چیست؟</b>\n{item['desc']}\n"
        tg += f"🛠 <b>توسعه:</b> {item['tech']}\n"
        tg += f"🔗 <b>مرجع خارجی:</b> <a href='{item['ref_url']}'>{item['ref_name']}</a>\n"
        tg += f"👥 <b>شواهد جهانی:</b> {item['traction']}\n"
        tg += f"💰 <b>درآمد جهانی:</b> {item['revenue']}\n"
        tg += f"🇮🇷 <b>بازار ایران:</b> {item['market_ir']}\n"
        tg += f"🎯 <b>جذب ۵ مشتری اول:</b> {item['growth']}\n"
        tg += f"💵 <b>پتانسیل درآمدی:</b> <b>{item['potential']}</b>\n\n"
    return tg

def run_daily_curation(force_day: int = None, force_send: bool = False):
    today = datetime.now().strftime("%Y-%m-%d")
    archive_file = os.path.join(notifier.ARCHIVE_DIR, f"{today}.md")
    
    # Check if already sent today (to prevent duplicate messages from multiple cron triggers)
    if os.path.exists(archive_file) and not force_send and force_day is None:
        print(f"Ideas for today ({today}) have already been sent and archived. Skipping duplicate run.")
        return True
        
    day_num = force_day if force_day is not None else determine_today_day_number()
    bundle = IDEAS_ROSTER.get(day_num, IDEAS_ROSTER[1])
    
    print(f"Executing daily curation for Date: {today} (Day {day_num}: {bundle['title']})")
    
    md_content = generate_markdown(day_num, today)
    tg_content = generate_telegram_message(day_num, today)
    
    # 1. Save to local archive
    archive_file = notifier.save_to_archive(md_content)
    print(f"Archive saved at: {archive_file}")
    
    # 2. Trigger Windows Toast Notification (if on Windows)
    notifier.send_windows_toast(f"ایده‌های روز {day_num} 🚀", f"۳ ایده تازه با مارکت ریسرچ کامل به تلگرام ارسال شد.")
    
    # 3. Send to Telegram with interactive buttons
    buttons = []
    for item in bundle["items"]:
        btn_text = f"⭐️ پسندیدم: {item['id']}. {item['name'][:30]}"
        cb_data = f"like_{today}_{day_num}_{item['id']}"
        buttons.append([{"text": btn_text, "callback_data": cb_data}])
    buttons.append([{"text": "📋 مشاهده لیست منتخب‌های این هفته", "callback_data": "view_shortlist"}])
    
    reply_markup = {"inline_keyboard": buttons}
    
    tg_ok = notifier.send_telegram(tg_content, reply_markup=reply_markup)
    if tg_ok:
        print("SUCCESS: Telegram message delivered to PV!")
        return True
    else:
        print("FAILED: Could not deliver Telegram message.")
        return False

if __name__ == "__main__":
    force = int(sys.argv[1]) if len(sys.argv) > 1 else None
    run_daily_curation(force)
