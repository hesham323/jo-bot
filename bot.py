import telebot
from telebot import types
import json
import os

# --- الإعدادات النهائية (هشام) ---
TOKEN = "8702007988:AAFTv9w2-2bsf-Wwv-6m7Q0VyXyDdaXjHHE" 
ADMIN_ID = 1433522207 
ORANGE_MONEY_INFO = "👤 الاسم: HESHAM3909\n📞 الرقم: 0779111936"

bot = telebot.TeleBot(TOKEN)
DATA_FILE = "tawseela_pro.json"

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

# --- الواجهة الرئيسية ---
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
    
    bot.send_message(message.chat.id, f"أهلاً بك {message.from_user.first_name} في بوت توصيلة الأردن 🇯🇴\nبإدارة: هشام\n\nاختر من القائمة أدناه:", reply_markup=markup)

# --- منطق الأزرار ---
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if message.text == "البحث عن رحلة 🔍":
        data = load_data()
        if not data["rides"]:
            bot.send_message(message.chat.id, "❌ لا توجد رحلات متوفرة حالياً.")
        else:
            res = "🔍 آخر الرحلات المنشورة:\n" + "-"*15 + "\n"
            for r in data["rides"][-5:]:
                res += f"👤 السائق: {r['driver']}\n📍 التفاصيل: {r['info']}\n" + "-"*10 + "\n"
            bot.send_message(message.chat.id, res)

    elif message.text == "نشر رحلة 🚗":
        msg = bot.send_message(message.chat.id, "اكتب تفاصيل رحلتك (مثلاً: من عمان لإربد، الساعة 4، متوفر 3 مقاعد):")
        bot.register_next_step_handler(msg, process_ride)

    elif message.text == "💳 اشترك الآن - 5 د.أ/شهر":
        bot.send_message(message.chat.id, f"للاشتراك المميز والنشر غير المحدود، يرجى التحويل لـ Orange Money:\n\n{ORANGE_MONEY_INFO}\n\nبعد التحويل أرسل صورة الوصل للمدير.")

    elif message.text == "المساعدة ℹ️":
        bot.send_message(message.chat.id, "هذا البوت لخدمة التوصيل بين المحافظات. للاستفسار تواصل مع @hesham_admin")

    else:
        bot.send_message(message.chat.id, "يرجى استخدام الأزرار بالأسفل.")

def process_ride(message):
    data = load_data()
    data["rides"].append({"driver": message.from_user.first_name, "info": message.text})
    save_data(data)
    bot.send_message(message.chat.id, "✅ تم نشر رحلتك بنجاح! سيتمكن الركاب من رؤيتها هسا.")

bot.infinity_polling()
