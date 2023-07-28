import time

from bot import send_mess_about_stop_list, send_mess_about_place, send_mess_about_rating
from data import cafe_addresses
from stop_pars import search_stop_dishes
from place_pars import restaurant_search
import pytz
import logging

from datetime import datetime

timezone = pytz.timezone('Asia/Yekaterinburg')


def job():
    current_time = datetime.now(timezone).time()
    if current_time.hour == 14 or current_time.hour == 17:
        print(current_time.hour)
        logging.info('### Запускаю поиск стоп лист ###')

        for name, data_list in cafe_addresses.items():
            name_rest = name
            url_rest = data_list[0]
            cafe_address = data_list[1]
            search_stop_dishes(cafe_address, url_rest, name_rest)

        print('### ПАРСИНГ стоп листа ЗАКОНЧЕН ### ')
        logging.info('### ПАРСИНГ стоп листа ЗАКОНЧЕН ###')
        send_mess_about_stop_list()

        logging.info('___отправляю инфу по стоп листу')
        print('___отправляю инфу по стоп листу')

        send_mess_about_rating()

        print('### Запускаю место выдачи ###')
        logging.info('### Запускаю место выдачи ###')

        for name, data_list in cafe_addresses.items():
            cafe_address = data_list[1]
            print(cafe_address)
            # добавила поиск  место выдачи
            restaurant_search()
            # добавила запись рейтинга
        print('### ПАРСИНГ места выдачи ЗАКОНЧЕН ### ')
        logging.info('### ПАРСИНГ места выдачи ЗАКОНЧЕН ### ')

        try:
            send_mess_about_place()
            logging.info('___отправляю инфу по место выдачи')
            print('___отправляю инфу по место выдачи')
        except Exception as ex:
            print(ex)

    # current_date = datetime.today().date()

    # if current_date.weekday() == 6 and current_time.hour == 22:  # 4 - пятница (понедельник - 0, воскресенье - 6)
    #     print(current_date.weekday())
    #     print('Воскресенье, отправляем данные за неделю')
    #     send_mess_about_stop_fow_week()

    time.sleep(3000)


while True:
    job()
