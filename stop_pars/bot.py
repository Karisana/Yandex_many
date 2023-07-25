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

bot = telebot.TeleBot('6100241130:AAGKwSMsv3Gz0ZowQUuN73tIgGVlcBv_7mk')

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


def info_about_place():
    txt_files = glob.glob("*.txt")

    radius = {}
    for file in txt_files:

        if file in file_dict_place:
            value = file_dict_place[file]
            name_address = value
            try:
                with open(f'{file}', 'r+', encoding='utf-8') as line:
                    rest_data = line.read().splitlines()
                    if need_name in rest_data:
                        data = []
                        place = rest_data.index(need_name) + 1
                        data.append(place)
                        time = current_time
                        data.append(time)
                    else:
                        data = []
                        place = "отсутствует в рейтинге"
                        data.append(place)
                        time = current_time
                        data.append(time)
            except Exception as ex:
                print('->>>>!!!!', ex, '!!!!<<<<-')

            radius[name_address] = data
        path = file
        os.remove(path)
    print('рейтинг записан, файлы удалены')
    print(radius)

    mess_about_stop_list = []
    for k, v in radius.items():
        mess_about_stop_list.append([k, v[0], v[1]])
    print('..текст mess_about_stop_list записан')

    try:
        with open(f'day.txt', 'a+', encoding='utf-8') as line:
            data_text = str(mess_about_stop_list).replace('[', '').replace("'", '').replace(']', '')
            line.write(f'{data_text}\n')
        print('Запись дня выполнена')
    except Exception as ex:
        print(ex)

    return mess_about_stop_list

    # os.remove(path)

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

    for file_name in files:
        name_address = ''
        if file_name in file_dict_stop:
            value = file_dict_stop[file_name]
            name_address = value

        res = f'Стоп лист {name_address}:'

        res_list = []
        with open(os.path.join(latest_folder, file_name), 'r', encoding='utf-8') as file:
            lines = file.readlines()
            res_list.append(lines)
        yield res, res_list


def count_string_occurrences_in_file(file_path):
    occurrences = defaultdict(int)
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            occurrences[line.strip()] += 1
    return occurrences


def send_mess_about_stop_fow_week():
    file_list = os.listdir('stop_week')
    for file_name in file_list:
        file_path = os.path.join('stop_week', file_name)
        occurrences = count_string_occurrences_in_file(file_path)

        name_address = ''
        if file_name in file_dict_stop:
            value = file_dict_stop[file_name]
            name_address = value

        res = f' <b> Стоп лист за неделю {name_address}</b>'
        for id in id_users:
            time.sleep(1)
            bot.send_message(chat_id=id, text=res, parse_mode='HTML')

        sorted_occurrences = sorted(occurrences.items(), key=lambda x: x[0])
        result_mess = ''
        for value, count in sorted_occurrences:

            if value != '':
                res = value.strip().replace("'", ''), ' - ', count, ' из 38 проверок.'
                mess = [str(item) for item in res]
                result = ''.join(mess)
                result_mess += f'{result}\n'

        for id in id_users:
            time.sleep(1)
            bot.send_message(chat_id=id, text=result_mess)

    del_file('stop_week')
    del_file('txt')
    del_file('rating')


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
            bot.send_message(chat_id=id, text=message, parse_mode='HTML')


def send_mess_about_place():
    info = f'<b>Отправляю место в выдачи по ресторанам {need_name}:</b>  #местовыдачи'

    message_about_place = info_about_place()

    final_text = ''
    for i in message_about_place:
        text = f'{i[0]}, место выдачи — {i[1]}.\n'
        final_text += text

    print(final_text)
    for id in id_users:
        bot.send_message(chat_id=id, text=info, parse_mode='HTML')

    for id in id_users:
        bot.send_message(chat_id=id, text=final_text, parse_mode='HTML')


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
        bot.send_message(chat_id=id, text="<b>Отправляю РЕЙТИНГ по точкам:</b>", parse_mode='HTML')

    # Перебор файлов и их удаление
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()

                # Получение последних двух значений
                if file_name in file_dict_stop:
                    value = file_dict_stop[file_name]
                    name_address = value
                last_two_values = [(line.strip()) for line in lines[-2:]]
                if len(last_two_values) >= 2:
                    if last_two_values[0] == last_two_values[1]:
                        mess = f'{name_address} рейтинг не изменился, {last_two_values[1]}, {smile(last_two_values[1])}'

                    else:
                        mess = f'{name_address} рейтинг изменился: был {last_two_values[0]}, стал {last_two_values[1]}, ' \
                               f'{smile(last_two_values[1])}'
                    for id in id_users:
                        time.sleep(1)
                        bot.send_message(chat_id=id, text=mess)

                else:
                    mess = f' {name_address} {last_two_values[0]} {smile(last_two_values[0])}'
                    for id in id_users:
                        time.sleep(0.5)
                        bot.send_message(chat_id=id, text=mess)
