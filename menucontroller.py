import database_handler
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove


class MenuController:
    def __init__(self, bot, user):
        self.bot = bot
        self.user = user
        self.markup = ReplyKeyboardMarkup()
        self.film = None
        self.seances_list = None
        self.selected_seance = None
        self.count = 0

    def show_menu(self, message):
        self.menu_choice(['Сегодня в кино', 'На этой неделе', 'Мои билеты', 'Выйти'], False, message, 'Выберите '
                                                                                                      'действие:',
                         self.show_menu_step)

    # menu steps
    def show_menu_step(self, message):
        try:
            answer = message.text
            if answer == u'Сегодня в кино':
                self.menu_choice(database_handler.get_today_films(), True, message, 'Выберите фильм:',
                                 self.menu_today_step)
            elif answer == u'На этой неделе':
                self.menu_choice(database_handler.get_week_films(), True, message, 'Выберите фильм:',
                                 self.menu_week_step)
            elif answer == u'Мои билеты':
                self.show_tickets(message)
            elif answer == u'Выйти':
                self.menu_choice(['Да', 'Нет'], False, message, 'Вы уверены?', self.menu_exit_step)
            else:
                raise Exception("Ошибка! Выберите один из предложенных вариантов")
        except Exception as e:
            msg = self.bot.reply_to(message, e)
            self.bot.register_next_step_handler(msg, self.show_menu_step)

    def menu_today_step(self, message):
        answer = message.text
        try:
            if answer == 'Назад':
                self.menu_choice(['Сегодня в кино', 'На этой неделе', 'Мои билеты', 'Выйти'], False, message,
                                 'Выберите '
                                 'действие:',
                                 self.show_menu_step)
                return
            self.film = database_handler.get_film(answer)
            self.seances_list = database_handler.get_today_seances(self.film.id)
            msg = self.bot.send_photo(message.chat.id, self.film.poster, caption=self.film.get_film_info(),
                                      reply_markup=self.markup)
            self.menu_choice(self.get_seances_time(), True, msg, 'Выберите один из предложенных сеансов: ',
                             self.show_seances_step)
        except Exception as e:
            msg = self.bot.reply_to(message, e)
            self.bot.register_next_step_handler(msg, self.menu_today_step)

    def show_seances_step(self, message):
        answer = message.text
        try:
            if answer == 'Назад':
                self.menu_choice(database_handler.get_today_films(), True, message, 'Выберите фильм:',
                                 self.menu_today_step)
                return
            self.selected_seance = self.get_seance(answer)
            self.show_places(message)
        except Exception as e:
            msg = self.bot.reply_to(message, e)
            self.bot.register_next_step_handler(msg, self.show_seances_step)

    def show_places(self, message):
        self.bot.send_message(message.chat.id, "Выберите место:", reply_markup=ReplyKeyboardRemove())
        self.bot.send_message(message.chat.id, "X-N. X-ряд, N-место", reply_markup=self.place_markup())

    def show_tickets(self, message):
        tickets = database_handler.get_ticket_info(self.user.id)
        for ticket in tickets:
            self.bot.send_message(message.chat.id, ticket.get_ticket_info())
        self.menu_choice(['Сегодня в кино', 'На этой неделе', 'Мои билеты', 'Выйти'], False, message,
                         'Выберите '
                         'действие:',
                         self.show_menu_step)

    def menu_week_step(self, message):
        answer = message.text
        try:
            if answer == 'Назад':
                self.menu_choice(['Сегодня в кино', 'На этой неделе', 'Мои билеты', 'Выйти'], False, message,
                                 'Выберите '
                                 'действие:',
                                 self.show_menu_step)
                return
            self.film = database_handler.get_film(answer)
            self.seances_list = database_handler.get_week_seances_dates(self.film.id)
            msg = self.bot.send_photo(message.chat.id, self.film.poster, caption=self.film.get_film_info(),
                                      reply_markup=self.markup)
            self.menu_choice(self.get_seances_dates(), True, msg, 'Выберите дату сеанса: ',
                             self.select_date_step)
        except Exception as e:
            msg = self.bot.reply_to(message, e)
            self.bot.register_next_step_handler(msg, self.menu_week_step)

    def select_date_step(self, message):
        answer = message.text
        try:
            if answer == 'Назад':
                self.menu_choice(['Сегодня в кино', 'На этой неделе', 'Мои билеты', 'Выйти'], False, message,
                                 'Выберите '
                                 'действие:',
                                 self.show_menu_step)
                return
            self.seances_list = database_handler.select_date_seance(self.film.id, answer)
            self.menu_choice(self.get_seances_time(), True, message, 'Выберите сеанс: ',
                             self.show_seances_step)
        except Exception as e:
            msg = self.bot.reply_to(message, e)
            self.bot.register_next_step_handler(msg, self.select_date_step)

    def menu_exit_step(self, message):
        answer = message.text
        try:
            if answer == u'Да':
                self.user.clear()
                msg = self.bot.send_message(message.chat.id, "Для регистрации используйте команду /reg!",
                                            reply_markup=ReplyKeyboardRemove())
            elif answer == u'Нет':
                self.menu_choice(['Сегодня в кино', 'На этой неделе', 'Мои билеты', 'Выйти'], False, message,
                                 'Выберите '
                                 'действие:',
                                 self.show_menu_step)
            else:
                raise Exception("Ошибка! Выберите 'Да' или 'Нет': ")
        except Exception as e:
            msg = self.bot.reply_to(message, e)
            self.bot.register_next_step_handler(msg, self.show_menu)

    def place_markup(self):
        hall = database_handler.get_hall_info(self.selected_seance.id_hall)
        places = database_handler.get_places(hall.id)
        markup = InlineKeyboardMarkup(row_width=hall.place_in_row)
        markup.row(InlineKeyboardButton("Экран", callback_data="screen"))
        for i in range(0, hall.row_count):
            markup.row(InlineKeyboardButton('Ряд №' + str(i + 1), callback_data='row'))
            button_list = list()
            for place in places:
                if place.row == i + 1:
                    if database_handler.is_place_free(place.id, self.selected_seance.id):
                        button_list.append(InlineKeyboardButton(place.place_number, callback_data=place.id))
                    else:
                        button_list.append(InlineKeyboardButton('X', callback_data='reserved'))
            markup.add(button_list)
        markup.row(
            InlineKeyboardButton("Отмена", callback_data="back"),
            InlineKeyboardButton("Заказать", callback_data="order")
        )
        return markup

    def get_seance(self, time):
        for seance in self.seances_list:
            if time == str(seance.time):
                return seance
        raise Exception("Ошибка! Выберите предложенный сеанс: ")

    def get_seances_time(self):
        time_list = list()
        for seance in self.seances_list:
            time_list.append(str(seance.time))
        return time_list

    def get_seances_dates(self):
        date_list = list()
        for seance in self.seances_list:
            if not date_list.__contains__(str(seance.date)):
                date_list.append(str(seance.date))
        return date_list

    def set_markup(self, row_list, add_back):
        self.markup = ReplyKeyboardMarkup()
        for row in row_list:
            self.markup.row(str(row))
        if add_back:
            self.markup.row('Назад')

    def menu_choice(self, markup, add_back, message, text, func):
        self.set_markup(markup, add_back)
        msg = self.bot.send_message(message.chat.id, text, reply_markup=self.markup)
        self.bot.register_next_step_handler(msg, func)
