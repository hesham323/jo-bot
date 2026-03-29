import telebot
from telebot import types
import json
import os
from datetime import datetime, timedelta

# التوكن والمعلومات الأساسية
TOKEN = "8702007988:AAFTv9w2-2bsf-Wwv-6m7Q0VyXyDdaXjHHE"
bot = telebot.TeleBot(TOKEN)
DATA_FILE = "rides_data.json"

# إعدادات هشام (المدير)
ADMIN_IDS = ["1433522207"]
CLIQ_ALIAS = "HESHAM3909"
CLIQ_PHONE = "0779111936"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"rides": [], "users": {}}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- لوحة تحكم الأدمن (هشام) ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🚗 نشر رحلة")
    btn2 = types.KeyboardButton("🔍 البحث عن رحلة")
    btn3 = types.KeyboardButton("👤 ملفي الشخصي")
    markup.add(btn1, btn2)
    markup.add(btn3)
    
    welcome_text = "أهلاً بك في بوت توصيلة الأردن! 🇯🇴\n"
    if user_id in ADMIN_IDS:
        welcome_text += "\n✅ تم التعرف عليك كمدير للنظام (صلاحيات كاملة)."
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🚗 نشر رحلة")
def post_ride(message):
    user_id = str(message.from_user.id)
    data = load_data()
    user_info = data["users"].get(user_id, {"trips": 0})
    
    # فحص الاشتراك (هشام مستثنى)
    if user_id not in ADMIN_IDS and user_info["trips"] >= 3:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("💳 اشترك الآن – 5 د.أ/شهر", callback_data="subscribe_info")
        markup.add(btn)
        bot.send_message(message.chat.id, "⚠️ وصلت للحد المجاني!\n\nاستخدمت 3/3 رحلات مجانية هذا الشهر.\n\nاشترك بـ 5 د.أ/شهر للنشر غير المحدود + ظهور رحلاتك في أعلى القائمة 👑", reply_markup=markup)
        return

    bot.send_message(message.chat.id, "اكتب تفاصيل رحلتك (من وين، لوين، متى، والسعر):")
    bot.register_next_step_handler(message, process_ride_details)

def process_ride_details(message):
    user_id = str(message.from_user.id)
    data = load_data()
    
    new_ride = {
        "id": len(data["rides"]) + 1,
        "user_id": user_id,
        "details": message.text,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    data["rides"].append(new_ride)
    if user_id not in data["users"]:
        data["users"][user_id] = {"trips": 0}
    data["users"][user_id]["trips"] += 1
    
    save_data(data)
    bot.send_message(message.chat.id, "✅ تم نشر رحلتك بنجاح!")

@bot.callback_query_handler(func=lambda call: call.data == "subscribe_info")
def subscribe_info(call):
    msg = f"🌟 مميزات الحساب المميز:\n- نشر رحلات غير محدود.\n- تمييز رحلاتك بلون خاص.\n\nللدفع أرسل 5 دانيير عبر كليك:\n\nالاسم المستعار: {CLIQ_ALIAS}\nرقم الهاتف: {CLIQ_PHONE}\n\nبعد الدفع، أرسل صورة الإيصال للمدير."
    bot.send_message(call.message.chat.id, msg)

print("Bot is running... Booking system fixed!")
bot.infinity_polling()
