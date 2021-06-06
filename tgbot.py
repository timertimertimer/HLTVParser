import telebot
import json
from pprint import pprint

def getLiveMatches():
    with open('live.json') as f:
        live_data = json.load(f)
    return live_data
    pass

def getTTMatches():
    with open('today_and_tomorrow.json') as f:
        tt_data = json.load(f)
    pass


TOKEN = '1870652191:AAE5Ty1kHNGL0nOxv_NFJcHvSNqrzEMH9jc'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text', 'document', 'audio'])
def get_text_message(message):
    if message.text:
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
bot.polling(none_stop=True, interval=0)
