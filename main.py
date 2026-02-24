import telebot
from telebot import types

TOKEN = '8000457608:AAEmrrhrKUf1-qRM-JDR1Ux8db3ia_v3zKw'
ADMIN_ID = 8421694319 

bot = telebot.TeleBot(TOKEN)

# --- حط رابط الفيديو تاعك هنا ---
# تقدر تجيب الرابط إذا رفعت الفيديو في قناتك (Copy Post Link)
WELCOME_VIDEO = "https://t.me/YourChannel/123" 

data = {
    'channels': [],
    'welcome_msg': "مرحباً بك في البوت!" 
}

def check_sub(user_id):
    if not data['channels']: return True
    for ch in data['channels']:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status in ['left', 'kicked']: return False
        except: continue
    return True

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    
    if user_id == ADMIN_ID:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📢 القنوات", "📝 الترحيب")
        bot.send_message(message.chat.id, "أهلاً بك يا مطور..", reply_markup=markup)
        return

    if not check_sub(user_id):
        markup = types.InlineKeyboardMarkup()
        for ch in data['channels']:
            markup.add(types.InlineKeyboardButton(f"اشترك هنا {ch}", url=f"https://t.me/{ch[1:]}"))
        markup.add(types.InlineKeyboardButton("تم الاشتراك ✅", callback_data="verify"))
        bot.send_message(message.chat.id, "⚠️ لازم تشترك أولاً:", reply_markup=markup)
    else:
        # هنا البوت يبعث الفيديو مع النص للناس كامل
        bot.send_video(message.chat.id, WELCOME_VIDEO, caption=data['welcome_msg'])

# باقي الكود (نفسه اللي عندك) ...
# [كمل باقي الأجزاء تاع handle_query و admin_actions]

bot.remove_webhook()
bot.infinity_polling()
