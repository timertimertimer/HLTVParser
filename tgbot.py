# - *- coding: utf- 8 - *-
import telebot
import json
import configure
from telebot import types


def matchInfo(match, live):
    s = match["team1"][0] + ' (' + match["team1"][1] + ') vs ' + \
        match["team2"][0] + ' (' + match["team2"][1] + ')\n'
    s += 'bo: ' + match['bo'] + '\n'
    if live:
        s += 'Карты: ' + match["maps"] + '\n'
    else:
        s += match['time'] + '\n'
    s += match["event"] + '\n'
    s += match['url']
    return s


bot = telebot.TeleBot(configure.config["TOKEN"])


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    refresh = types.KeyboardButton("Обновить")
    glm = types.KeyboardButton("Лайвы")
    gttm = types.KeyboardButton("Сегодня и завтра")
    markup.add(glm, gttm, refresh)
    bot.send_message(message.chat.id, 'Настройки:\nТоп 50, Бо3+')
    bot.send_message(message.chat.id, 'Нажми на одну из кнопок', reply_markup=markup)


@bot.message_handler(content_types=['text', 'document', 'audio'])
def get_text_message(message):
    if message.text == 'Лайвы':
        with open('live.json', encoding='utf-8') as live:
            live = json.load(live)
            if live["live"]:
                bot.send_message(message.chat.id, '*ЛАЙВЫ*', parse_mode="MarkdownV2")
                for match in live["live"]:
                    s = matchInfo(match, True)
                    bot.send_message(message.chat.id, s)
            else:
                bot.send_message(message.chat.id, 'На данный момент лайвов нет')
    elif message.text == 'Сегодня и завтра':
        with open('today_and_tomorrow.json', encoding='utf-8') as tt:
            tt = json.load(tt)
            for day in tt:
                bot.send_message(message.chat.id, day)
                for match in tt[day]:
                    s = matchInfo(match, False)
                    bot.send_message(message.chat.id, s)
    elif message.text == 'Обновить':
        import hltvParse


bot.polling(none_stop=True, interval=0)
