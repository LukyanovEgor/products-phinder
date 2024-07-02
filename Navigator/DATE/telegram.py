import telebot
bot = telebot.TeleBot('6723013452:AAGxlvSp5Deemgxuqbk0Cv4u9xVE2dBQhlU')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
  if message.text == "Привет":
    bot.send_message(message.from_user.id, "Привет!!!")

bot.polling(none_stop=True, interval=0)
print('FW')