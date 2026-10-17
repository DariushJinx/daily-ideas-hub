import os
import json
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), "saved_ideas.json")
PIPELINE_MD_PATH = os.path.join(os.path.dirname(__file__), "pipeline.md")

def load_data():
    if os.path.exists(DATA_PATH):
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"shortlist": [], "in_progress": [], "archived": []}
    return {"shortlist": [], "in_progress": [], "archived": []}

def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    update_pipeline_markdown(data)

def add_to_shortlist(idea_id: str, title: str, date_str: str, summary: str, url: str):
    data = load_data()
    # Check if already added
    for item in data.get("shortlist", []):
        if item.get("id") == idea_id:
            return False, "این ایده قبلاً به لیست منتخب‌ها اضافه شده است."
            
    item = {
        "id": idea_id,
        "title": title,
        "date": date_str,
        "summary": summary,
        "url": url,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "shortlisted"
    }
    data.setdefault("shortlist", []).append(item)
    save_data(data)
    return True, "با موفقیت به لیست منتخب‌های هفتگی اضافه شد!"

def select_for_implementation(idea_id: str):
    data = load_data()
    selected_item = None
    remaining_shortlist = []
    
    for item in data.get("shortlist", []):
        if item.get("id") == idea_id:
            selected_item = item
        else:
            remaining_shortlist.append(item)
            
    if not selected_item:
        return False, "ایده مورد نظر در لیست هفتگی یافت نشد."
        
    selected_item["status"] = "in_progress"
    selected_item["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data.setdefault("in_progress", []).append(selected_item)
    # The others remain in archive
    for other in remaining_shortlist:
        other["status"] = "archived"
        data.setdefault("archived", []).append(other)
        
    data["shortlist"] = [] # Cleared for the next cycle
    save_data(data)
    return True, f"ایده '{selected_item['title']}' برای پیاده‌سازی انتخاب شد و فاز توسعه آغاز شد!"

def update_pipeline_markdown(data=None):
    if data is None:
        data = load_data()
        
    content = f"""# 🚀 تابلوی مدیریت و پایپ‌لاین ایده‌ها (Kanban Pipeline)
*آخرین به‌روزرسانی: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

---

## 🎯 در حال پیاده‌سازی و ساخت (In Progress / Ready to Build)
"""
    if data.get("in_progress"):
        for item in data["in_progress"]:
            content += f"- **[{item['title']}]({item['url']})** (انتخاب‌شده در: {item.get('started_at')})\n  - خلاصه: {item['summary']}\n\n"
    else:
        content += "_در حال حاضر هیچ ایده‌ای در فاز ساخت نیست._\n\n"

    content += "## ⭐️ منتخب‌های این هفته (Weekly Shortlist)\n"
    if data.get("shortlist"):
        for item in data["shortlist"]:
            content += f"- **[{item['title']}]({item['url']})** (ذخیره‌شده در: {item['saved_at']})\n  - خلاصه: {item['summary']}\n\n"
    else:
        content += "_هنوز ایده‌ای برای این هفته لایک نشده است._\n\n"

    content += "## 📦 بایگانی ایده‌های گذشته (Archived Ideas)\n"
    if data.get("archived"):
        for item in data["archived"]:
            content += f"- [{item['title']}]({item['url']}) ({item['date']})\n"
    else:
        content += "_بایگانی خالی است._\n"

    with open(PIPELINE_MD_PATH, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    update_pipeline_markdown()
    print("Storage module initialized successfully.")
