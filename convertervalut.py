import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('')
currency = CurrencyConverter()
amount = 0
user_state = {}



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, введите сумму')
    bot.register_next_step_handler(message, summa)


def summa(message):

    user_state[message.chat.id] = False

    global amount
    try:
        amount = int(message.text.strip())
    except ValueError: 
        bot.send_message(message.chat.id, 'Неверный формат. Впишите сумму')
        bot.register_next_step_handler(message, summa)
        return
    
    if amount > 0:
        marcup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        marcup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=marcup)
    else:
        bot.send_message(message.chat.id, 'Число должно быть > 0. Впишите сумму')
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call:True)
def callback(call):

    user_id = call.message.chat.id

    if call.data != 'else':

        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму')

        # Зарегистрировать следующий шаг только если еще не зарегистрирован
        if not user_state.get(user_id):
            user_state[user_id] = True  # устанавливаем флаг
            bot.register_next_step_handler(call.message, summa)

    else:
        bot.send_message(call.message.chat.id, 'Введите пару значений через слэш /')
        bot.register_next_step_handler(call.message, mycurrency)


def mycurrency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: {round(res, 2)}. Можете заново вписать сумму')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'Что то не так. Впишите значение заново')
        bot.register_next_step_handler(message, summa)




bot.polling(none_stop = True)
