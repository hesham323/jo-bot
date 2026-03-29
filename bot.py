import telebot
from telebot import types
import json
import os

# --- إعدادات هشام (جاهزة 100%) ---
TOKEN = "8702007988:AAFTv9w2-2bsf-Wwv-6m7Q0VyXyDdaXjHHE" 
ADMIN_ID = 1433522207 
ORANGE_MONEY_INFO = "👤 الاسم: HESHAM3909\n📞 الرقم: 0779111936"

bot = telebot.TeleBot(TOKEN)
DATA_FILE = "tawseela_final.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return {"rides": [], "drivers": {}}
    return {"rides": [], "drivers": {}}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- واجهة البوت الرئيسية ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("نشر رحلة 🚗")
    btn2 = types.KeyboardButton("البحث عن رحلة 🔍")
    btn3 = types.KeyboardButton("ملفي الشخصي 👤")
    btn4 = types.KeyboardButton("رحلاتي 📋")
    btn5 = types.KeyboardButton("المساعدة ℹ️")
    btn6 = types.KeyboardButton("تقييم رحلة ⭐")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    markup.row(types.KeyboardButton("💳 اشترك الآن - 5 د.أ/شهر"))
    if message.from_user.id == ADMIN_ID:
        markup.row(types.KeyboardButton("📊 لوحة تحكم المدير (هشام)"))
    bot.send_message(message.chat.id, f"أهلاً بك {message.from_user.first_name} في بوت توصيلة الأردن 🇯🇴\nبإدارة: هشام\n\nاختر من القائمة:", reply_markup=markup)

# --- نظام النشر (مع ميزة المدير) ---
@bot.message_handler(func=lambda message: message.text == "نشر رحلة 🚗")
def publish(message):
    data = load_data()
    u_id = str(message.from_user.id)
    if message.from_user.id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "مرحباً يا مدير، اكتب تفاصيل الرحلة وعدد المقاعد:")
        bot.register_next_step_handler(msg, save_it)
        return
    if u_id not in data["drivers"]:
        data["drivers"][u_id] = {"count": 0, "is_pro": False}
    if not data["drivers"][u_id]["is_pro"] and data["drivers"][u_id]["count"] >= 3:
        bot.send_message(message.chat.id, "⚠️ وصلت للحد المجاني (3/3)!\nيرجى الاشتراك للنشر غير المحدود.")
    else:
        msg = bot.send_message(message.chat.id, "اكتب تفاصيل الرحلة وعدد المقاعد:")
        bot.register_next_step_handler(msg, save_it)

def save_it(message):
    data = load_data()
    data["rides"].append({"driver": message.from_user.first_name, "info": message.text})
    if message.from_user.id != ADMIN_ID:
        data["drivers"][str(message.from_user.id)]["count"] += 1
    save_data(data)
    bot.send_message(message.chat.id, "✅ تم نشر الرحلة بنجاح!")

# --- زر الاشتراك ---
@bot.message_handler(func=lambda message: message.text == "💳 اشترك الآن - 5 د.أ/شهر")
def pay(message):
    bot.send_message(message.chat.id, f"💳 لتفعيل الاشتراك المميز:\n\n{ORANGE_MONEY_INFO}")

print("البوت شغال...")
bot.infinity_polling()
