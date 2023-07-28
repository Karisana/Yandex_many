import time
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from secure_data import login_proxy, password_proxy
import os
import datetime


def search_stop_dishes(cafe_address: str, url_rest: str, name_rest: str):
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

    # login = login_proxy
    # password = password_proxy
    #
    # proxy = f"{login}:{password}@149.126.218.116:8000"
    #
    # capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    # capabilities['proxy'] = {
    #     "proxyType": "MANUAL",
    #     "httpProxy": proxy,
    #     "sslProxy": proxy
    # }
    # options.add_argument("--proxy-server=http://" + proxy)  # Установка прокси-сервера в опции
    #
    # # Установка прокси-сервера и опций веб-драйвера
    driver = webdriver.Chrome(options=options)

    try:
        driver = webdriver.Chrome(options=options)
        driver.delete_all_cookies()
        driver.get(url=url_rest)

        print('START парcинга ~~стоп лист ~~рейтинг ресторана — ', name_rest)
        print(f'...{name_rest}— открываю страницу ресторана, прогружаю')
        time.sleep(10)
        driver.save_screenshot('scrin/1_stop.png')

        print(f'...{name_rest}— капчи блока не было')
        print()

        driver.save_screenshot('scrin/3_stop.png')

        try:
            print(f'...{name_rest}— проверяем наличие капчи "Пиковая нагрузка"')

            wait = WebDriverWait(driver, 10)
            captcha = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div/div[3]')))

            captcha.click()
            print(f'...{name_rest}— клик капчи "Пиковая нагрузка"')

        except Exception as ex:
            print(f'...{name_rest}— капчи "Пиковая нагрузка" нет, ошибку не печатаю')

        finally:
            time.sleep(5)
            try:
                print(f'...{name_rest}— Ищу рейтинг')
                time.sleep(5)
                rating = driver.find_element(By.XPATH,
                                             '/html/body/div[1]/div/div/div[1]/div/div/div/main/div[1]/div[3]/button['
                                             '1]/div/div[1]')
                print(rating.text)

                try:
                    name_file = name_rest
                    folder_path = os.path.join('rating')

                    file_path = os.path.join(folder_path, name_file)
                    os.makedirs(folder_path, exist_ok=True)

                    with open(file_path, 'a+', encoding='utf-8') as line:
                        line.write(f'{rating.text}\n')

                    print(f'...{name_rest}— Запись рейтинга выполнена <-')
                except Exception as ex:
                    print(ex)

            except Exception as ex:
                print(f'...{name_rest} {ex}. Рейтинг не найден')

            print(f'...{name_rest}— скролим')
            top_res = driver.find_element(By.CLASS_NAME, "DesktopPlaceLayout_content")
            scroll_origin = ScrollOrigin.from_element(top_res)
            stop_menu_all = []
            for _ in range(60):
                ActionChains(driver).scroll_from_origin(scroll_origin, 0, 300).perform()

                time.sleep(1)
                try:
                    menu_not_active = driver.find_elements(By.CSS_SELECTOR,
                                                           ".UiKitDesktopProductCard_unavailable")
                    for item in menu_not_active:
                        if item.text.split('\n') not in stop_menu_all:
                            stop_menu_all.append(item.text.split('\n'))
                except Exception as ex:
                    print(ex)

            stop = [x[1] for x in stop_menu_all]
            stop_menu = list(set(stop))

            try:
                name_file = name_rest

                current_datetime = datetime.datetime.now()
                folder_name = current_datetime.strftime('%d-%m_%H')
                folder_path = os.path.join('txt', folder_name)

                file_path = os.path.join(folder_path, name_file)
                os.makedirs(folder_path, exist_ok=True)

                with open(file_path, 'w', encoding='utf-8') as line:
                    print(stop_menu)
                    for name_menu in stop_menu:
                        print(name_menu)
                        line.write(f'{name_menu}\n')

                folder_path = os.path.join('stop_week')

                file_path = os.path.join(folder_path, name_file)
                os.makedirs(folder_path, exist_ok=True)

                with open(file_path, 'a+', encoding='utf-8') as line:
                    for name_menu in stop_menu:
                        line.write(f'{name_menu}\n')

                print(f'{name_menu}...Запись стоп листа выполнена <-')
            except Exception as ex:
                print(f'{ex}...Запись стоп листа НЕ выполнена. Стоп лист пуст! <-')

        print(f'{name_menu} Парсинг адреса закончен <-')

    except Exception as ex:
        actions = ActionChains(driver)
        time.sleep(2)
        print(ex)

    finally:
        driver.close()
        driver.quit()
