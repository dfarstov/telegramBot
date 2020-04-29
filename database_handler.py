import config
import pymysql
from db_entities import *
from datetime import date

connect = pymysql.connect(host=config.dbHost,
                          user=config.dbUser,
                          password=config.dbPass,
                          db=config.dbName,
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)


# login/reg user
def check_password(password):
    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM tbcinema.users WHERE tbcinema.users.password = '{}';".format(password))
        res = cursor.fetchone()
        if res is None:
            return True
        return False


def reg_user(user):
    with connect.cursor() as cursor:
        cursor.execute("INSERT INTO tbcinema.users"
                       "(name,"
                       "password,"
                       "age,"
                       "sex) "
                       "VALUES"
                       "(%s,"
                       "%s,"
                       "%s,"
                       "%s);", (user.name, user.password, user.age, user.sex))
        connect.commit()


def login_user(password):
    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM tbcinema.users WHERE tbcinema.users.password = '{}'".format(password))
        res = cursor.fetchone()
        if res is None:
            raise Exception('Ошибка! Пользователь с таким паролем не найден!')
        user = User()
        user.id = res['id_user']
        user.name = res['name']
        user.password = res['password']
        user.age = res['age']
        user.sex = res['sex']
        return user


# get info
def get_today_films():
    result = list()
    with connect.cursor() as cursor:
        cursor.execute("SELECT DISTINCT "
                       "f.name "
                       "FROM "
                       "seances s "
                       "JOIN films f ON s.id_film = f.id_film "
                       "WHERE s.date = '{}'".format(date.today().strftime("%Y%m%d")))
        while True:
            res = cursor.fetchone()
            if res is None:
                break
            result.append(res['name'])
        if result is None:
            raise Exception("На сегодня сеансов нет!")
    return result


def get_week_films():
    result = list()
    with connect.cursor() as cursor:
        cursor.execute("SELECT DISTINCT "
                       "f.name "
                       "FROM "
                       "seances s "
                       "JOIN films f ON s.id_film = f.id_film "
                       "WHERE s.date > '{}'".format(date.today().strftime("%Y%m%d")))
        while True:
            res = cursor.fetchone()
            if res is None:
                break
            result.append(res['name'])
        if result is None:
            raise Exception("Сеансов нет!")
    return result


def get_film(film_name):
    with connect.cursor() as cursor:
        cursor.execute("SELECT "
                       "f.id_film,"
                       "f.name,"
                       "c.name,"
                       "f.date,"
                       "f.box_office,"
                       "f.time,"
                       "s1.name,"
                       "s1.lastname,"
                       "s2.name,"
                       "s2.lastname,"
                       "f.poster,"
                       "f.description "
                       "FROM tbcinema.films f "
                       "JOIN countries c on f.id_country = c.id_country "
                       "JOIN screenwriters_directors s1 on f.id_screen_writer  = s1.id_screenwriter_director "
                       "JOIN screenwriters_directors s2 on f.id_screen_writer  = s2.id_screenwriter_director "
                       'WHERE f.name = "{}"'.format(film_name))
        res = cursor.fetchone()
        if res is None:
            raise Exception("Ошибка! Вы выбрали несуществующий фильм.")
        res = get_element_item(res)
        return FilmInfo(res)


def get_today_seances(film_id):
    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM tbcinema.seances WHERE tbcinema.seances.id_film = {}".format(
            film_id) + " AND tbcinema.seances.date = '{}'".format(date.today().strftime("%Y%m%d")))
        seances_list = list()
        for seance in resdict_to_list(cursor.fetchall()):
            seances_list.append(Seance(seance))
        return seances_list


def get_week_seances_dates(film_id):
    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM tbcinema.seances WHERE tbcinema.seances.id_film = {}".format(
            film_id) + " AND tbcinema.seances.date > '{}'".format(date.today().strftime("%Y%m%d")))
        seances_list = list()
        for seance in resdict_to_list(cursor.fetchall()):
            seances_list.append(Seance(seance))
        return seances_list


def select_date_seance(film_id, date):
    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM tbcinema.seances WHERE tbcinema.seances.id_film = {}".format(
            film_id) + " AND tbcinema.seances.date = '{}'".format(date))
        seances_list = list()
        for seance in resdict_to_list(cursor.fetchall()):
            seances_list.append(Seance(seance))
        return seances_list


def get_places(hall_id):
    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM places p  WHERE p.id_hall = {}".format(hall_id))
        place_list = list()
        for place in resdict_to_list(cursor.fetchall()):
            place_list.append(Place(place))
        return place_list


def get_hall_info(hall_id):
    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM halls h  WHERE h.id_hall = {}".format(hall_id))
        hall = Hall(get_element_item(cursor.fetchone()))
        return hall


def get_order(seance_id, selected_place):
    with connect.cursor() as cursor:
        cursor.execute(
            "SELECT "
            "t.id_ticket, "
            "f1.name,  "
            "s.date,  "
            "s.time, "
            "p1.row, "
            "p2.place_number, "
            "pr.price "
            "FROM "
            "tbcinema.tickets t "
            "JOIN "
            "tbcinema.seances s ON t.id_seance = s.id_seance "
            "JOIN "
            "tbcinema.films f1 ON s.id_film = f1.id_film "
            "JOIN "
            "tbcinema.films f2 ON s.id_film = f2.id_film "
            "JOIN "
            "tbcinema.places p1 ON t.id_place = p1.id_place "
            "JOIN "
            "tbcinema.places p2 ON t.id_place = p2.id_place "
            "JOIN "
            "tbcinema.ticket_prices pr ON t.id_price = pr.id_price "
            "JOIN "
            "tbcinema.users u ON t.id_user = u.id_user "
        "WHERE t.id_seance = {} AND t.id_place = {}".format(seance_id, selected_place))
        res = TicketInfo(get_element_item(cursor.fetchone()))
        return res.get_ticket_info()
    raise Exception("Ошибка!")


def is_place_free(place_id, seance_id):
    with connect.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM tbcinema.tickets WHERE id_seance = {} AND id_place = {}".format(seance_id, place_id))
        if cursor.fetchone() is None:
            return True
        else:
            return False


def order_ticket(id_seance, id_place, id_price, id_user):
    with connect.cursor() as cursor:
        cursor.execute("INSERT INTO tbcinema.tickets"
                       "(id_seance,"
                       "id_place,"
                       "id_price,"
                       "id_user) "
                       "VALUES"
                       "({},"
                       "{},"
                       "{},"
                       "{});".format(id_seance, id_place, id_price, id_user))
        connect.commit()


def get_ticket_info(user_id):
    with connect.cursor() as cursor:
        cursor.execute(
            "SELECT "
            "t.id_ticket, "
            "f1.name,  "
            "s.date,  "
            "s.time, "
            "p1.row, "
            "p2.place_number, "
            "pr.price "
            "FROM "
            "tbcinema.tickets t "
            "JOIN "
            "tbcinema.seances s ON t.id_seance = s.id_seance "
            "JOIN "
            "tbcinema.films f1 ON s.id_film = f1.id_film "
            "JOIN "
            "tbcinema.films f2 ON s.id_film = f2.id_film "
            "JOIN "
            "tbcinema.places p1 ON t.id_place = p1.id_place "
            "JOIN "
            "tbcinema.places p2 ON t.id_place = p2.id_place "
            "JOIN "
            "tbcinema.ticket_prices pr ON t.id_price = pr.id_price "
            "JOIN "
            "tbcinema.users u ON t.id_user = u.id_user "
            "WHERE u.id_user = {}".format(user_id))
        tickets = list()
        for ticket in resdict_to_list(cursor.fetchall()):
            tickets.append(TicketInfo(ticket))
        return tickets


def get_user_id(user_password):
    with connect.cursor() as cursor:
        cursor.execute("SELECT id_user FROM tbcinema.users  WHERE tbcinema.users.password = '{}'".format(user_password))
        user = cursor.fetchone()
        return user['id_user']


def get_price(seance):
    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM tbcinema.ticket_prices")
        prices = cursor.fetchall()
        for price in prices:
            if price['time_from'] <= seance.time < price['time_to']:
                return price['id_price']


# result to list
def resdict_to_list(res_dict):
    res_list = list()
    for element in res_dict:
        res_list.append(get_element_item(element))
    return res_list


def get_element_item(element):
    item_list = list()
    for key, item in element.items():
        item_list.append(item)
    return item_list