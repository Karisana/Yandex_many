import time
from datetime import datetime
import telebot
import glob
import os
import pytz
from datetime import datetime

from place_pars import *
from data import *
from collections import defaultdict

# bot = telebot.TeleBot('6100241130:AAGKwSMsv3Gz0ZowQUuN73tIgGVlcBv_7mk')
bot = telebot.TeleBot('6424489351:AAF97PMhVjedczz4pGLKYeHUvhfokvytS64')

timezone = pytz.timezone('Europe/Moscow')
current_time = datetime.now(timezone).time().hour


def del_file(folder_path):
    # удаление всех файлов, чтобы начать с нуля новую неделю
    folder_path = folder_path

    # Получение списка файлов в папке
    file_list = os.listdir(folder_path)

    # Перебор файлов и их удаление
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Файл {file_name} удален.")


def last_file():
    """ Формирование выдачи для бота по стоп листам кафе.

        file_dict -- словарь где ключ адрес в формате записанного файла, а ключ - название для удобства
        --> Москва_Театральнаяаллея_1с1': 'Динамо'

        Далее мы находим последнюю созданную папку в папке txt
        Собираем данные из этой папки
        Далее берем значение из словаря по ключу, где ключ - название файла в папке.
        res -- это строка с name_address, где name_address - название адреса
        res_list -- это вложенный список из блюд, которые на стопе

        :yield res, res_list

    """

    folder_path = 'txt'
    directories = glob.glob(os.path.join(folder_path, '*'))
    directories.sort(key=os.path.getctime, reverse=True)

    if len(directories) == 0:
        print("Не найдены папки с txt файлами.")

    latest_folder = directories[0]
    folder_name = latest_folder.split("\\")[-1]
    folder_path = os.path.join(folder_path, folder_name)  # Full path to the folder

    files = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            files.append(item)

    for name, data_list in cafe_addresses.items():
        name_address = name
        res = f'Стоп лист {name_address}:'

        res_list = []
        with open(os.path.join(latest_folder, name_address), 'r', encoding='utf-8') as file:
            lines = file.readlines()
            res_list.append(lines)
        yield res, res_list


def count_string_occurrences_in_file(file_path):
    occurrences = defaultdict(int)
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            occurrences[line.strip()] += 1
    return occurrences


# def send_mess_about_stop_fow_week():
#     file_list = os.listdir('stop_week')
#     for file_name in file_list:
#         file_path = os.path.join('stop_week', file_name)
#         occurrences = count_string_occurrences_in_file(file_path)
#
#         name_address = ''
#         if file_name in file_dict_stop:
#             value = file_dict_stop[file_name]
#             name_address = value
#
#         res = f' <b> Стоп лист за неделю {name_address}</b>'
#         for id in id_users:
#             time.sleep(1)
#             bot.send_message(chat_id=id, text=res, parse_mode='HTML')
#
#         sorted_occurrences = sorted(occurrences.items(), key=lambda x: x[0])
#         result_mess = ''
#         for value, count in sorted_occurrences:
#
#             if value != '':
#                 res = value.strip().replace("'", ''), ' - ', count, ' из 38 проверок.'
#                 mess = [str(item) for item in res]
#                 result = ''.join(mess)
#                 result_mess += f'{result}\n'
#
#         for id in id_users:
#             time.sleep(1)
#             bot.send_message(chat_id=id, text=result_mess)
#
#     del_file('stop_week')
#     del_file('txt')
#     del_file('rating')


def send_mess_about_stop_list():
    """ Формирование и отправка итогово сообщения по id пользователя

        mes_stop_list -- результат фу last_file()
        name_string -- название ресторана
        menu_string -- список стоп блюд в формате строки

    """
    mes_stop_list = last_file()

    for i in mes_stop_list:
        name_string = i[0]

        menu_string = i[1]
        for j in menu_string:
            j.sort(key=str.lower)
        result_string = ''.join([str(item) for sublist in menu_string for item in sublist])

        message = f'<b>{name_string}</b>\n\n{result_string}\n  #стоплист'

        for id in id_users:
            print('->  -> Отправка данных по стоп листам id-пользователя - ', id)
            time.sleep(1)

            try:
                bot.send_message(chat_id=id, text=message, parse_mode='HTML')
            except Exception as ex:
                print(id, 'не найден в боте')


def info_place_parsing(file_name: str):
    need_name_in_dict = cafe_addresses[file_name][2]

    try:
        with open(f'{file_name}.txt', 'r+', encoding='utf-8') as line:
            rest_data = line.read().splitlines()
            if need_name_in_dict in rest_data:
                data = []
                place = rest_data.index(need_name_in_dict) + 1
                data.append(place)
                time = current_time
                data.append(time)
            else:
                data = []
                place = "отсутствует в рейтинге"
                data.append(place)
                time = current_time
                data.append(time)

        # Находим значение этого ключа (списка) под индексом 2

        # Записываем значение в формате строки: ключ, индексовый номер в файле num
        data_str = f'{file_name} место: {place}'
        yield data_str

    except Exception as ex:
        print('->>>>!!!!', ex, '!!!!<<<<-')


def send_mess_about_place():
    message_about_place = ''
    for key in cafe_addresses.keys():
        result = info_place_parsing(key)
        for text in result:
            total_text = f'{text} \n'
            message_about_place += total_text

        try:
            # Удаляем файл после обработки
            os.remove(f'{key}.txt')
            print(f'Файл {key}.txt удален.')
        except Exception as ex:
            print(f'Не удалось удалить файл {key}.txt:', ex)

    info = f'<b>Отправляю место в выдачи.</b>  #местовыдачи'

    for id in id_users:
        try:
            bot.send_message(chat_id=id, text=info, parse_mode='HTML')
        except Exception as ex:
            print(id, 'не найден в боте')

    for id in id_users:
        try:
            bot.send_message(chat_id=id, text=message_about_place, parse_mode='HTML')
        except Exception as ex:
            print(id, 'не найден в боте')


def send_mess_about_rating():
    folder_path = 'rating'

    # Получение списка файлов в папке
    file_list = os.listdir(folder_path)

    def smile(rating):
        smile_1 = '\U0001f929'
        smile_2 = '\U0001F600'
        smile_3 = '\U0001F610'
        smile_4 = '\U0001F615'
        smile_5 = '\U0001F621'
        if rating == '4.9':
            emoji = smile_1.encode('utf-16', 'surrogatepass').decode('utf-16')
            return emoji
        elif rating == '4.8':
            emoji = smile_2.encode('utf-16', 'surrogatepass').decode('utf-16')
            return emoji
        elif rating == '4.7':
            emoji = smile_3.encode('utf-16', 'surrogatepass').decode('utf-16')
            return emoji
        elif rating == '4.6':
            emoji = smile_4.encode('utf-16', 'surrogatepass').decode('utf-16')
            return emoji
        else:
            emoji = smile_5.encode('utf-16', 'surrogatepass').decode('utf-16')
            return emoji

    for id in id_users:
        time.sleep(1)
        try:
            bot.send_message(chat_id=id, text="<b>Отправляю РЕЙТИНГ:</b>", parse_mode='HTML')
        except Exception as ex:
            print(id, 'не найден в боте')

    # Перебор файлов
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        print(file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()

                # Получение последних двух значений для каждого файла
                last_two_values = [(line.strip()) for line in lines[-2:]]
                if len(last_two_values) >= 2:

                    if last_two_values[0] == last_two_values[1]:
                        mess = f'<b>{file_name}</b> рейтинг не изменился, {last_two_values[1]}, {smile(last_two_values[1])}'
                    else:
                        mess = f'<b>{file_name}</b> рейтинг изменился: был {last_two_values[0]}, стал {last_two_values[1]}, ' \
                               f'{smile(last_two_values[1])}'

                for id in id_users:
                    time.sleep(0.5)
                    try:
                        bot.send_message(chat_id=id, text=mess, parse_mode='HTML')
                    except Exception as ex:
                        print(id, 'не найден в боте')

                else:
                    mess = f' <b>{file_name}</b> {last_two_values[0]} {smile(last_two_values[0])}'
                    print(mess)
                    for id in id_users:
                        time.sleep(0.5)
                        try:
                            bot.send_message(chat_id=id, text=mess, parse_mode='HTML')
                        except Exception as ex:
                            print(id, 'не найден в боте')
