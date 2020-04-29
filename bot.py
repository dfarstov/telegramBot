import telebot
import config
import database_handler
from db_entities import User
from registrationcontroller import RegistrationController
from menucontroller import MenuController

bot = telebot.TeleBot(config.token)
user = User()
reg_controller = RegistrationController(bot, user)
menu_controller = MenuController(bot, user)
msg = None


@bot.message_handler(commands=['start', 'help', 'reg', 'auth', 'menu'])
def handle_command(message):
    if message.text == '/start':
        welcome_user(message)
    elif message.text == '/help':
        help_user(message)
    elif message.text == '/reg':
        reg_user(message)
    elif message.text == '/auth':
        auth_user(message)
    elif message.text == '/menu':
        menu(message)
    else:
        msg = bot.send_message(message.chat.id, "Ошибка! Вы ввели неверную команду!")
        help_user(msg)


def welcome_user(message):
    bot.send_message(message.chat.id,
                     "Курсовая работа студента 3 курса Физико-Технического факультета группы ИВТ-4 Яманко Дмитрия.\n"
                     "Для начала работы с ботом необходимо зарегистрироваться введя команду /reg для входа - /auth")


def help_user(message):
    bot.send_message(message.chat.id, "1) /reg - регистрация\n"
                                      "2) /auth - авторизация\n"
                                      "3) /menu - меню действий\n")


def reg_user(message):
    global msg
    msg = message
    reg_controller.reg_user(message)


def auth_user(message):
    global msg
    msg = message
    reg_controller.login_user(message)


def menu(message):
    try:
        if user.name is None:
            raise Exception("Ошибка! Для работы с ботом нужно зарегистрироваться /reg или авторизоваться /auth")
        menu_controller.show_menu(message)
    except Exception as e:
        bot.reply_to(message, e)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "screen":
        pass
    elif call.data == "row":
        pass
    elif call.data == "back":
        if len(user.selected_places) == 0:
            bot.send_message(msg.chat.id, "Для продолжения работы введите команду /menu")
        else:
            bot.answer_callback_query(call.id, "Выбор отменен")
            user.selected_places.pop()
    elif call.data == "order":
        if len(user.selected_places) == 0:
            bot.answer_callback_query(call.id, "Выберите место")
        else:
            price_id = database_handler.get_price(menu_controller.selected_seance)
            for place_id in user.selected_places:
                database_handler.order_ticket(menu_controller.selected_seance.id, place_id, price_id, user.id)
                bot.send_message(msg.chat.id, database_handler.get_order(menu_controller.selected_seance.id, place_id))
            bot.send_message(msg.chat.id, "Ваш заказ оформлен. Для продолжения работы введите команду /menu")
            user.selected_places = list()
    elif call.data == "reserved":
        bot.answer_callback_query(call.id, "Место забронированно")
    else:
        if user.selected_places.__contains__(call.data):
            bot.answer_callback_query(call.id, "Место уже выбрано")
        else:
            bot.answer_callback_query(call.id, "Место выбрано")
            user.selected_places.append(call.data)

import os
from flask import Flask, request

@server.route('/' + tokenBot.TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://test-new-new.herokuapp.com/' + tokenBot.TOKEN)
    return "!", 200


if __name__ == '__main__':
    server.debug = True
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    bot.polling(none_stop=True)