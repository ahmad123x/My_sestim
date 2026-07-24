import time
import os
import json
import threading
import requests
from datetime import datetime
from flask import Flask, render_template_string

app = Flask(__name__)

DB_FILE = "system_status.json"

TELEGRAM_BOT_TOKEN = "8762854326:AAEtIAjma2ZADr1PGZZ4_exW3ae6TCwy-hg"
ADMIN_CHAT_ID = 447831012

# === خطة الـ 6 أشهر الحقيقية ===
# 6 أشهر تقريباً = 180 يوماً (بالثواني)
TRIGGER_LIMIT = 60 * 60 * 24 * 180 
# ================================

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                pass
    return {
        "last_checkin": time.time(),
        "is_triggered": False,
        "last_reminder_date": ""
    }

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

TRUSTED_CONTACTS = [
    {"name": "حساب إنستغرام 1", "type": "Instagram", "link": "https://www.instagram.com/tp1_1?igsh=bnE0MW4yMHNvdzVi", "icon": "📸"},
    {"name": "حساب إنستغرام 2", "type": "Instagram", "link": "https://www.instagram.com/3i3_ij?igsh=NXY4c2U5ZHJwZ3hz", "icon": "📸"},
    {"name": "اتصال / واتساب", "type": "Direct Link", "link": "https://wa.me/9647710449291", "icon": "💬"}
]

@app.route("/")
def index():
    data = load_data()
    current_time = time.time()
    elapsed_time = current_time - data["last_checkin"]
    
    if elapsed_time > TRIGGER_LIMIT and not data["is_triggered"]:
        data["is_triggered"] = True
        save_data(data)

    # 1. الواجهة الأولى: وضع الأمان (فخمة وهادئة)
    if not data["is_triggered"]:
        return """
        <!DOCTYPE html>
        <html lang="ar" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Aegis | Secure Portal</title>
            <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500&display=swap" rel="stylesheet">
            <style>
                * { box-sizing: border-box; margin: 0; padding: 0; }
                body {
                    background-color: #08090d;
                    color: #94a3b8;
                    font-family: 'Tajawal', sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    overflow: hidden;
                    background-image: radial-gradient(circle at 50% 50%, #111827 0%, #08090d 100%);
                }
                .card {
                    background: rgba(17, 24, 39, 0.6);
                    backdrop-filter: blur(12px);
                    border: 1px solid rgba(255, 255, 255, 0.05);
                    padding: 40px 30px;
                    border-radius: 20px;
                    max-width: 480px;
                    width: 90%;
                    text-align: center;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.5);
                }
                .status-dot {
                    width: 8px;
                    height: 8px;
                    background-color: #10b981;
                    border-radius: 50%;
                    display: inline-block;
                    box-shadow: 0 0 10px #10b981;
                    margin-bottom: 20px;
                }
                p {
                    font-size: 15px;
                    line-height: 1.8;
                    color: #94a3b8;
                    font-weight: 300;
                }
            </style>
        </head>
        <body>
            <div class="card">
                <div class="status-dot"></div>
                <p>أهلاً بك. هذه البوابة الرقمية مخصصة للاستخدام الشخصي فقط وغير مرتبطة بأي خدمات عامة حالياً. شكراً لزيارتك، ونتمنى لك وقتاً طيباً.</p>
            </div>
        </body>
        </html>
        """

    # 2. الواجهة الثانية: وضع الطوارئ (راقية وحصرية)
    contacts_html = ""
    for contact in TRUSTED_CONTACTS:
        contacts_html += f"""
        <a href="{contact['link']}" target="_blank" class="contact-card">
            <div class="contact-info">
                <span class="icon">{contact['icon']}</span>
                <div>
                    <h3>{contact['name']}</h3>
                    <span class="type">{contact['type']}</span>
                </div>
            </div>
            <span class="arrow">←</span>
        </a>
        """

    emergency_template = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>System Notice | Recovery & Inquiry</title>
        <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap" rel="stylesheet">
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                background-color: #07080b;
                color: #f8fafc;
                font-family: 'Tajawal', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                padding: 20px;
                background-image: radial-gradient(circle at 50% 10%, #1a1d2d 0%, #07080b 80%);
            }}
            .container {{
                width: 100%;
                max-width: 500px;
                text-align: center;
            }}
            .alert-badge {{
                display: inline-block;
                background: rgba(245, 158, 11, 0.1);
                color: #fbbf24;
                border: 1px solid rgba(245, 158, 11, 0.2);
                padding: 6px 16px;
                border-radius: 30px;
                font-size: 13px;
                font-weight: 500;
                margin-bottom: 25px;
                letter-spacing: 0.5px;
            }}
            .desc {{
                color: #94a3b8;
                font-size: 15px;
                line-height: 1.8;
                margin-bottom: 35px;
                font-weight: 300;
            }}
            .contacts-wrapper {{
                display: flex;
                flex-direction: column;
                gap: 12px;
            }}
            .contact-card {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: rgba(18, 20, 32, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.06);
                padding: 16px 20px;
                border-radius: 14px;
                text-decoration: none;
                color: inherit;
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
            }}
            .contact-card:hover {{
                background: rgba(26, 30, 48, 0.9);
                border-color: rgba(255, 255, 255, 0.15);
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            }}
            .contact-info {{
                display: flex;
                align-items: center;
                gap: 15px;
                text-align: right;
            }}
            .icon {{
                font-size: 20px;
                background: rgba(255, 255, 255, 0.04);
                width: 40px;
                height: 40px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 10px;
            }}
            .contact-info h3 {{
                font-size: 15px;
                font-weight: 500;
                color: #f1f5f9;
                margin-bottom: 3px;
            }}
            .contact-info .type {{
                font-size: 12px;
                color: #64748b;
            }}
            .arrow {{
                color: #64748b;
                font-size: 16px;
                transition: transform 0.2s;
            }}
            .contact-card:hover .arrow {{
                transform: translateX(-4px);
                color: #38bdf8;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="alert-badge">قناة المتابعة والاطمئنان</div>
            <p class="desc">
                السلام عليكم. هذه الصفحة مخصصة لغرض المتابعة والاطمئنان. يرجى من الأصدقاء والراغبين بالسؤال التواصل مع الجهات الموثوقة المذكورة أدناه.
            </p>
            <div class="contacts-wrapper">
                {contacts_html}
            </div>
        </div>
    </body>
    </html>
    """
    return emergency_template

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": ADMIN_CHAT_ID, "text": text})

# مراقب الخلفية (لتنبيهات الجمعة والتكثيف يوم السبت + استقبال /alive)
def background_scheduler_and_listener():
    offset = 0
    get_updates_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    
    while True:
        current_time = datetime.now()
        current_date_str = current_time.strftime("%Y-%m-%d")
        current_weekday = current_time.weekday() # 4 = الجمعة، 5 = السبت
        
        data = load_data()
        last_rem_date = data.get("last_reminder_date", "")
        
        # 1. إشعار يوم الجمعة الأسبوعي
        if current_weekday == 4 and last_rem_date != current_date_str:
            send_telegram_message("⚠️ تذكير دوري: هل أنت بخير؟\nأرسل الأمر /alive لتجديد عداد الـ 6 أشهر.")
            data["last_reminder_date"] = current_date_str
            save_data(data)
            
        # 2. التكثيف يوم السبت إذا لم يتم الرد
        elif current_weekday == 5 and last_rem_date != current_date_str:
            send_telegram_message("🚨 تنبيه مكثف (1/3): لم يتم رصد ردك منذ إشعار الجمعة! يرجى إرسال /alive إذا كنت بخير.")
            time.sleep(5)
            send_telegram_message("🚨 تنبيه مكثف (2/3): النظام ينتظر تأكيدك لتفادي تفعيل حالة الطوارئ. أرسل /alive.")
            time.sleep(5)
            send_telegram_message("🚨 تنبيه مكثف (3/3): الرجاء تأكيد الوجود بإرسال الأمر /alive حالاً.")
            
            data["last_reminder_date"] = current_date_str
            save_data(data)

        # استقبال الأوامر من بوت تليجرام
        try:
            response = requests.get(get_updates_url, params={"offset": offset, "timeout": 10})
            if response.status_code == 200:
                result = response.json()
                for update in result.get("result", []):
                    offset = update["update_id"] + 1
                    message = update.get("message", {})
                    chat_id = message.get("chat", {}).get("id")
                    text = message.get("text", "")
                    
                    if chat_id == ADMIN_CHAT_ID and text == "/alive":
                        data = load_data()
                        data["last_checkin"] = time.time()
                        data["is_triggered"] = False
                        save_data(data)
                        
                        send_telegram_message("✅ تم تأكيد استجابتك بنجاح! تم تصفير عداد الـ 6 أشهر وإبقاء النظام في وضع الأمان.")
        except Exception as e:
            pass
        
        time.sleep(30) # فحص منتظم في الخلفية

if __name__ == "__main__":
    t = threading.Thread(target=background_scheduler_and_listener, daemon=True)
    t.start()
    
    app.run(host="0.0.0.0", port=5000)
