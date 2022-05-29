import random
import telebot
from telebot import types

API_TOKEN = '5166133359:AAHDTRN51Odhtpi9Bkn8BxbhfZrBTki9gJo'

bot = telebot.TeleBot(API_TOKEN)

storage = dict()


def init_storage(user_id):
    storage[user_id] = dict(attempt=None, random_digit=None)


def set_data_storage(user_id, key, value):
    storage[user_id][key] = value


def get_data_storage(user_id):
    return storage[user_id]


@bot.message_handler(func=lambda message: message.text.lower() == "привет")
def command_text_hi(m):
    bot.send_message(m.chat.id, "Ну привет)")


@bot.message_handler(func=lambda message: message.text.lower() == "как дела?")
def command_text_dela(m):
    bot.send_message(m.chat.id, "хорошо")


@bot.message_handler(func=lambda message: message.text.lower() == "угадай число")
def digitgames(message):
    init_storage(message.chat.id)  ### Инициализирую хранилище


    bot.send_message(message.chat.id, f'Игра "угадай число"!')

    random_digit = random.randint(1, 100)
    print(random_digit)

    set_data_storage(message.chat.id, "random_digit", random_digit)
    print(get_data_storage(message.chat.id))

    bot.send_message(message.chat.id, 'Готово! Загадано число от 1 до 100!')
    bot.send_message(message.chat.id, 'Введите число')
    bot.register_next_step_handler(message, process_digit_step)


def process_digit_step(message):
    user_digit = message.text

    if not user_digit.isdigit():
        msg = bot.reply_to(message, 'Вы ввели не цифры, введите пожалуйста цифры')
        bot.register_next_step_handler(msg, process_digit_step)
        return

    random_digit = get_data_storage(message.chat.id)["random_digit"]

    if int(user_digit) == random_digit:
        bot.send_message(message.chat.id, f'Ура! Ты угадал число! Это была цифра: {random_digit}')
        init_storage(message.chat.id)  ### Очищает значения из хранилище
        return
    elif int(user_digit) > random_digit:
        bot.send_message(message.chat.id, 'Меньше')
        bot.register_next_step_handler(message, process_digit_step)
        return
    else:
        bot.send_message(message.chat.id, 'Больше')
        bot.register_next_step_handler(message, process_digit_step)
        return

if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling()