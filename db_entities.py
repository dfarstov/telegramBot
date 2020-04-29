class User:
    def __init__(self):
        self.id = None
        self.name = None
        self.password = None
        self.age = None
        self.sex = None
        self.selected_places = list()

    def clear(self):
        self.__init__()


class FilmInfo:
    def __init__(self):
        self.id = None
        self.name = None
        self.country = None
        self.date = None
        self.box_office = None
        self.time = None
        self.screen_writer_name = None
        self.screen_writer_lastname = None
        self.producer_name = None
        self.producer_lastname = None
        self.poster = None
        self.description = None

    def __init__(self, id, name, country, date, box_office, time, screen_writer_name, screen_writer_lastname, producer_name, producer_lastname, poster, description):
        self.id = id
        self.name = name
        self.country = country
        self.date = date
        self.box_office = box_office
        self.time = time
        self.screen_writer_name = screen_writer_name
        self.screen_writer_lastname = screen_writer_lastname
        self.producer_name = producer_name
        self.producer_lastname = producer_lastname
        self.poster = poster
        self.description = description

    def __init__(self, data_list):
        self.id = data_list[0]
        self.name = data_list[1]
        self.country = data_list[2]
        self.date = data_list[3]
        self.box_office = data_list[4]
        self.time = data_list[5]
        self.screen_writer_name = data_list[6]
        self.screen_writer_lastname = data_list[7]
        self.producer_name = data_list[8]
        self.producer_lastname = data_list[9]
        self.poster = data_list[10]
        self.description = data_list[11]

    def get_film_info(self):
        return "Название: " + self.name + '\n' + \
               "Страна: " + self.country + '\n' + \
               "Дата выхода: " + str(self.date.strftime("%Y/%m/%d")) + '\n' + \
               "Сборы: " + str(self.box_office) + '$\n' + \
               "Продолжительность: " + str(self.time) + '\n' + \
               "Сценарист: " + self.screen_writer_name + ' ' + self.screen_writer_lastname + '\n' + \
               "Продюсер: " + self.producer_name + ' ' + self.producer_lastname + '\n' + \
               "Описание: " + self.description


class TicketInfo:
    def __init__(self):
        self.id = None
        self.name = None
        self.date = None
        self.time = None
        self.row = None
        self.place_number = None
        self.price = None

    def __init__(self, data_list):
        self.id = data_list[0]
        self.name = data_list[1]
        self.date = data_list[2]
        self.time = data_list[3]
        self.row = data_list[4]
        self.place_number = data_list[5]
        self.price = data_list[6]

    def get_ticket_info(self):
        return "№ билета: " + str(self.id) + '\n' + \
               "Название фильма: " + self.name + '\n' + \
               "Дата: " + self.date.strftime("%m/%d/%Y") + '\n' + \
               "Время: " + str(self.time) + '\n' + \
               "Ряд: " + str(self.row) + '\n' + \
               "Место: " + str(self.place_number) + '\n' + \
               "Цена: " + str(self.price)


class Seance:
    def __init__(self):
        self.id = None
        self.id_film = None
        self.id_hall = None
        self.date = None
        self.time = None

    def __init__(self, list):
        self.id = list[0]
        self.id_film = list[1]
        self.id_hall = list[2]
        self.date = list[3]
        self.time = list[4]


class Place:
    def __init__(self):
        self.id = None
        self.id_hall = None
        self.row = None
        self.place_number = None

    def __init__(self, list):
        self.id = list[0]
        self.id_hall = list[1]
        self.row = list[2]
        self.place_number = list[3]


class Hall:
    def __init__(self):
        self.id = None
        self.name = None
        self.row_count = None
        self.place_in_row = None

    def __init__(self, list):
        self.id = list[0]
        self.name = list[1]
        self.row_count = list[2]
        self.place_in_row = list[3]