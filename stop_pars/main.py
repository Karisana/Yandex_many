import time

from bot import send_mess_about_stop_list, send_mess_about_place, send_mess_about_stop_fow_week, send_mess_about_rating
from data import cafe_addresses
from data import directions
from place_pars import restaurant_search
from stop_pars import search_stop_dishes
import pytz
from datetime import datetime

timezone = pytz.timezone('Europe/Moscow')


def job():
    current_time = datetime.now(timezone).time()
    if current_time.hour == 10 or current_time.hour == 12 or current_time.hour == 14\
            or current_time.hour == 17 or current_time.hour == 21:
        print(current_time.hour)

        print('### Запускаю стоп лист ###')
        for name in cafe_addresses:
            search_stop_dishes(name)
        print('### ПАРСИНГ стоп листа ЗАКОНЧЕН ### ')
        send_mess_about_stop_list()

        print('___отправляю инфу по стоп листу')

        send_mess_about_rating()

        print('### Запускаю место выдачи ###')
        for address in directions:
            print(address)
            # добавила поиск  место выдачи
            restaurant_search(address)
            # добавила запись рейт инга
        print('### ПАРСИНГ места выдачи ЗАКОНЧЕН ### ')
        try:
            send_mess_about_place()
            print('___отправляю инфу по место выдачи')
        except Exception as ex:
            print(ex)

    current_date = datetime.today().date()

    if current_date.weekday() == 6 and current_time.hour == 22:  # 4 - пятница (понедельник - 0, воскресенье - 6)
        print(current_date.weekday())
        print('Воскресенье, отправляем данные за неделю')
        send_mess_about_stop_fow_week()

    time.sleep(3000)


while True:
    job()

