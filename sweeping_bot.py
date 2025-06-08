import os
import telebot

# Use environment variable or direct token
BOT_TOKEN = os.environ.get("BOT_TOKEN") or "7967256524:AAF48mFN3UjOiWaKD-crtkRvc5oBHvF1LN4"

bot = telebot.TeleBot(BOT_TOKEN)

# Sweeping schedule
schedule = [
    "Week 1: Likola Misheck",
    "Week 2: Kasakula George",
    "Week 3: Milimo Musaka",
    "Week 4: Temba Leadway",
    "Week 5: Likola Misheck",
    "Week 6: Kasakula George",
    "Week 7: Milimo Musaka",
    "Week 8: Temba Leadway",
    # (Continue up to Week 50)
]

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome to the Sweeping Schedule Bot! Type /schedule to see who is cleaning.")

@bot.message_handler(commands=['schedule'])
def send_schedule(message):
    response = "\n".join(schedule)
    bot.send_message(message.chat.id, f"🧹 Sweeping Schedule:\n\n{response}")

bot.infinity_polling()
