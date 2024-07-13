import os
import telebot
import csv
from utils.classes import TodoManager
import logging

log_path = "/home/archit0994/misc/gitwork/log"

# Initialize the logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(message)s',
    handlers=[
        logging.FileHandler('{}/telegraminfo.log'.format(log_path)),
        logging.StreamHandler()
    ]
)
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if BOT_TOKEN is None:
    logging.info("Bot token not found")
else:
    logging.info("token found")


bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Kemnu chale?")

@bot.message_handler(func=lambda msg: True)
def update_todo(message):
    todo = TodoManager()
    try:
        action, info = message.text.split(":")

        if action.lower().strip() == todo.ADD:
            reply = todo.add_task(info)
            bot.reply_to(message, reply)
        elif action.lower().strip() == todo.VIEW:
            reply = todo.view_task()
            bot.reply_to(message,reply)
        elif action.lower().strip() == todo.DELETE:
            reply = todo.delete_task(info)
            if reply[0]:
                reply = "Here is the updated list:\n"
                reply += todo.view_task()
                bot.reply_to(message, reply)
            else:
                bot.reply_to(message, reply[1])
        else:
            bot.reply_to(message, "unknown action")
    
    except Exception as e: 
        bot.reply_to(message, "Error={}".format(e))
    
    # todo.add_task(message.text)

bot.infinity_polling()
