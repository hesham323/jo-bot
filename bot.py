import telebot
from telebot import types

# --- استخدم التوكن الجديد والمفعل حصراً ---
TOKEN = '8702007988:AAFTv9w2-2bsf-Wwv-6m7Q0VyXyDdaXjHHE'
bot = telebot.TeleBot(TOKEN)

# قاعدة بيانات مؤقتة للرحلات
trips = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('🚗 أنا سائق (إضافة رحلة)')
    btn2 = types.KeyboardButton('👤 أنا راكب (بحث عن رحلة)')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "أهلاً بك في بوت 'توصيلة الأردن' 🇯🇴\nبإدارة: هشام\nطريقك أسهل وأوفر!", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '🚗 أنا سائق (إضافة رحلة)')
def add_trip(message):
    msg = bot.send_message(message.chat.id, "أدخل مسار الرحلة (مثال: عمان إلى إربد):")
    bot.register_next_step_handler(msg, process_route)

def process_route(message):
    route = message.text
    msg = bot.send_message(message.chat.id, "كم عدد المقاعد المتاحة في سيارتك؟")
    bot.register_next_step_handler(msg, lambda m: process_seats(m, route))

def process_seats(message, route):
    try:
        seats = int(message.text)
        trip_id = message.chat.id
        trips[trip_id] = {'route': route, 'seats': seats, 'driver_name': message.from_user.first_name}
        
        markup = types.InlineKeyboardMarkup()
        btn_book = types.InlineKeyboardButton(f"حجز مقعد (المتبقي: {seats}) 💺", callback_data=f"book_{trip_id}")
        markup.add(btn_book)
        
        bot.send_message(message.chat.id, f"✅ تم نشر رحلتك بنجاح:\n📍 المسار: {route}\n💺 المقاعد المتوفرة: {seats}", reply_markup=markup)
    except:
        msg = bot.send_message(message.chat.id, "الرجاء إدخال رقم صحيح للمقاعد (مثلاً: 3):")
        bot.register_next_step_handler(msg, lambda m: process_seats(m, route))

@bot.callback_query_handler(func=lambda call: call.data.startswith('book_'))
def handle_booking(call):
    trip_id = int(call.data.split('_')[1])
    if trip_id in trips and trips[trip_id]['seats'] > 0:
        trips[trip_id]['seats'] -= 1
        new_seats = trips[trip_id]['seats']
        
        markup = types.InlineKeyboardMarkup()
        if new_seats > 0:
            btn_book = types.InlineKeyboardButton(f"حجز مقعد (المتبقي: {new_seats}) 💺", callback_data=f"book_{trip_id}")
            markup.add(btn_book)
        else:
            btn_book = types.InlineKeyboardButton("❌ ممتلئة بالكامل", callback_data="full")
            markup.add(btn_book)
        
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, "تم حجز مقعدك بنجاح! ✅")
        bot.send_message(trip_id, f"🔔 تنبيه: قام {call.from_user.first_name} بحجز مقعد معك. المتبقي عندك: {new_seats}")
    else:
        bot.answer_callback_query(call.id, "نعتذر، هذه الرحلة اكتملت. ❌")

# --- أمر التشغيل اللانهائي لـ Render ---
if __name__ == "__main__":
    bot.infinity_polling()
