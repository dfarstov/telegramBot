import re
import database_handler
from telebot import types


class RegistrationController:
    def __init__(self, bot, user):
        self.bot = bot
        self.user = user

    # user_login
    def login_user(self, message):
        msg = self.bot.send_message(message.chat.id, "Введите ваш логин указанный при регистрации: ")
        self.bot.register_next_step_handler(msg, self.login_next_step)

    def login_next_step(self, message):
        try:
            user = database_handler.login_user(message.text)
            self.user.id = user.id
            self.user.name = user.name
            self.user.password = user.password
            self.user.age = user.age
            self.user.sex = user.sex
            self.bot.send_message(message.chat.id, "Вы успешно авторизованы, " + self.user.name + ".\nДля начала "
                                                                                                   "работы "
                                                                                                   "воспользуйтесь "
                                                                                                   "командой /menu")
        except Exception as e:
            msg = self.bot.reply_to(message, e)
            self.bot.register_next_step_handler(msg, self.login_next_step)

    # user_reg
    def reg_user(self, message):
        msg = self.bot.send_message(message.chat.id, "Придумайте уникальный логин для повторной авторизацииё("
                                                     "используйте только буквы латинского алфавита): ")
        self.bot.register_next_step_handler(msg, self.reg_login_step)

    def reg_login_step(self, message):
        try:
            if not re.search(r'[A-Za-z0-9]', message.text):
                raise Exception("Ошибка! Вы ввели некорректный логин! Попробуйте еще раз: ")
            if not database_handler.check_password(message.text):
                raise Exception("Ошибка! Данный пользователь уже зарегистрирован! Попробуйте еще раз: ")
            self.user.password = message.text
            msg = self.bot.send_message(message.chat.id, "Введите свое имя: ")
            self.bot.register_next_step_handler(msg, self.reg_name_step)
        except Exception as e:
            msg = self.bot.reply_to(message, e)
            self.bot.register_next_step_handler(msg, self.reg_login_step)

    def reg_name_step(self, message):
        self.user.name = message.text
        msg = self.bot.send_message(message.chat.id, "Введите свой возраст(только цифры): ")
        self.bot.register_next_step_handler(msg, self.reg_age_step)

    def reg_age_step(self, message):
        try:
            if not message.text.isdigit():
                raise Exception("Ошибка! Укажите возраст цифрой: ")
            self.user.age = message.text
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add("Мужской", "Женский")
            msg = self.bot.send_message(message.chat.id, "Выберите ваш пол: ", reply_markup=markup)
            self.bot.register_next_step_handler(msg, self.reg_sex_step)
        except Exception as e:
            msg = self.bot.reply_to(message, e)
            self.bot.register_next_step_handler(msg, self.reg_age_step)

    def reg_sex_step(self, message):
        try:
            sex = message.text
            if (sex == u"Мужской") or (sex == u"Женский"):
                self.user.sex = sex
                database_handler.reg_user(self.user)
                self.user.id = database_handler.get_user_id(self.user.password)
                self.bot.send_message(message.chat.id, "Вы успешно зарегистрированы!\nДля начала работы "
                                                       "воспользуйтесь командой /menu")
            else:
                raise Exception("Ошибка! Выберите один из предложенных вариантов: ")
        except Exception as e:
            msg = self.bot.reply_to(message, e)
            self.bot.register_next_step_handler(msg, self.reg_sex_step)