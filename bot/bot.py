import telebot


token = '398480915:AAF8B5F-R7hkB_8cMoOwnmABaXy76J7sD28'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def start_mes(message):
    print(message)
    bot.send_message(message.chat.id, "привет, лшюп!")


@bot.message_handler(content_types=['photo'])
def start_mes(message):
    print(message)
    bot.send_message(message.chat.id, "это картинка")


bot.polling()
