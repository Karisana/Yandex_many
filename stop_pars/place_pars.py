import shutil

import time

from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

from data import cafe_addresses

# настройки парсинга
user_agents = UserAgent()

# s = Service('home/stop_pars/chromedriver')
s = Service('C:/Users/RVR/PycharmProjects/ya_pars1/stop_pars/chromedriver.exe')

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
# options.add_argument("--headless")
options.add_argument(f'user-agent={user_agents.random}')
options.add_argument("--incognito")
options.add_argument("--window-size=1500,1500")


def restaurant_search():
    """Парсит сайт яндекс еды.

        driver -- при запуске через VPS нужно убрать подключение к proxy

        Стоит тайминг для прогрузки страницы.
        Парсинг медленно специально, чтобы страница успела прогрузиться.

        В конце запись файла == text
    """

    prev_key = None
    for key, values in cafe_addresses.items():
        address = values[1]
        if address == cafe_addresses.get(prev_key, [None, None, None])[1]:
            if prev_key is not None:
                prev_file_name = f'{prev_key}.txt'
                new_file_name = f'{key}.txt'
                shutil.copy(prev_file_name, new_file_name)
                print(f'Файл скопирован: {prev_file_name} -> {new_file_name}')
                break
            else:
                prev_key = key

        login = '4wZd45'
        password = 'A9Pooz'

        proxy = f"{login}:{password}@193.31.101.153:9348"

        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        capabilities['proxy'] = {
            "proxyType": "MANUAL",
            "httpProxy": proxy,
            "sslProxy": proxy
        }
        options.add_argument("--proxy-server=http://" + proxy)  # Установка прокси-сервера в опции

        # Установка прокси-сервера и опций веб-драйвера
        driver = webdriver.Chrome(options=options)

        driver.delete_all_cookies()

        driver.save_screenshot('scrin/1_место_открытие.png')

        try:
            driver.get(url='https://eda.yandex.ru/')
            time.sleep(5)
            driver.save_screenshot('scrin/2_место_скрин_страницы.png')
            print('open modalsls')

            driver.find_element(By.CSS_SELECTOR,
                                "span.DesktopAddressButton_address").click()

            time.sleep(1)
            driver.save_screenshot('scrin/3_место_скрин_модалки.png')

            time.sleep(2)
            print('search address')
            driver.save_screenshot('scrin/4_место_скрин ввод адреса.png')
            home_1 = driver.find_element(By.CSS_SELECTOR,
                                         "input.AppAddressInput_addressInput.AppAddressInput_modalStyle")

            time.sleep(2)
            direction_text = address
            for ch in direction_text:
                home_1.send_keys(ch)
                time.sleep(0.1)
            print('...Адрес введен:', address)

            driver.save_screenshot('scrin/5_место - адрес введен.png')
            time.sleep(6)

            print('клик по пикселям адреса')

            driver.save_screenshot('scrin/6_место клик по пикселям адреса.png')
            print('пробуем нажать на кнопку ОК')
            home_1.find_element('xpath', '/html/body/div[3]/div/div/div/div/div[1]/div[2]/button').click()
            driver.save_screenshot('scrin/7_место скрин Нажали на ок кнопку.png')

            print('Нажали на ок кнопку, прогружаем на скрол...')

            driver.save_screenshot('scrin/8_место-скролл попытка.png')
            time.sleep(2)

            top_res = driver.find_element(By.CSS_SELECTOR,
                                          "div.LayoutBdu_layout:nth-child(9) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)")
            scroll_origin = ScrollOrigin.from_element(top_res)

            # top_res = driver.find_element(By.CSS_SELECTOR,
            #                               "/html/body/div[1]/div/div/div[1]/div/div/div/div[8]/div/div/div")
            # scroll_origin = ScrollOrigin.from_element(top_res)

            all_rest = []
            time.sleep(15)

            for _ in range(150):
                ActionChains(driver).scroll_from_origin(scroll_origin, 0, 200).perform()
                time.sleep(0.1)

                try:
                    res_names = driver.find_elements(By.CLASS_NAME, "NewPlaceItem_title")

                    for item in res_names:
                        if item.text.split('\n') not in all_rest:
                            all_rest.append(item.text.split('\n'))
                except Exception as ex:
                    print(ex)

            driver.save_screenshot('scrin/9_место-скролл.png')
            text_file = name_rest

            with open(f'{text_file}.txt', 'w', encoding='utf-8') as file:
                for i in all_rest:
                    for name_rest in i:
                        file.write(f'{name_rest}\n')

                print('...записали файл')
            print('...парсинг адреса закончен <-')

        except Exception as ex:
            actions = ActionChains(driver)
            actions.move_by_offset(750, 750).perform()
            time.sleep(2)
            actions.double_click().perform()
            time.sleep(2)
            driver.save_screenshot('scrin/2_err.png')

            time.sleep(2)
            print(ex)

        finally:
            driver.close()
            driver.quit()
