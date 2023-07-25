import time
from selenium.webdriver.common.proxy import Proxy, ProxyType

from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from seleniumwire import webdriver

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from secure_data import login_proxy, password_proxy
import os
import datetime

# настройки парсинга
user_agents = UserAgent()

# s = Service('home/stop_pars/chromedriver')
s = Service('C:/Users/RVR/PycharmProjects/ya_pars1/stop_pars/chromedriver.exe')

url = 'https://eda.yandex.ru/'
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument(f'user-agent={user_agents.random}')
options.add_argument("--incognito")
options.add_argument("--window-size=1500,1000")


# options.add_argument("--headless")

def search_stop_dishes(cafe_address: str):
    login = login_proxy
    password = password_proxy

    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = f"{login}:{password}@149.126.218.116:8000"
    proxy.ssl_proxy = f"{login}:{password}@149.126.218.116:8000"

    capabilities = webdriver.DesiredCapabilities.CHROME
    proxy.add_to_capabilities(capabilities)
    time.sleep(2)

    driver = webdriver.Chrome(service=s, options=options, desired_capabilities=capabilities)

    driver.get(url='https://eda.yandex.ru/moscow/r/dagestanskaya_lavka?')
    print('START пасринга стоп листа по адресу-', cafe_address)

    try:
        time.sleep(15)
        driver.save_screenshot('scrin/1_stop.png')
        # capcha_start = driver.find_element(By.CLASS_NAME, 'CheckboxCaptcha-Button')
        # try:
        #     capcha_start = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'CheckboxCaptcha-Button')))
        #     if capcha_start:
        #         print('Попали на стартовую капчу')
        #         capcha_start.click()
        #         time.sleep(10)
        #         print('captcha_element')
        #         captcha_element = driver.find_element(By.XPATH, '//*[@id="advanced-captcha-form"]/div/div[1]/img')
        #
        #         # получение URL изображения капчи
        #         print('получение URL изображения капчи')
        #         captcha_url = captcha_element.get_attribute("src")
        #
        #         # скачивание изображения капчи
        #         print('скачивание изображения капчи')
        #         response = requests.get(captcha_url)
        #         with open("captcha.png", "wb") as f:
        #             f.write(response.content)
        #
        #         # распознавание текста на изображении капчи
        #         print('распознавание текста на изображении капчи')
        #         captcha_text = pytesseract.image_to_string("captcha.png")
        #         time.sleep(100)
        #         print('ввод распознанного текста в поле для ввода капчи')
        #         # ввод распознанного текста в поле для ввода капчи
        #         captcha_input = driver.find_element(By.XPATH, '// *[ @ id = "xuniq-0-1"]')
        #         captcha_input.send_keys(captcha_text)
        #
        #         # нажатие на кнопку подтверждения
        #         submit_button = driver.find_element(By.XPATH,
        #                                             '// *[ @ id = "advanced-captcha-form"] / div / div[3] / button[3] / div / span / span')
        #
        #         submit_button.click()
        #
        # except Exception as ex:
        #     print(f'Ошибка в капче или ее нет')

        print(f'...{cafe_address} open modals - Стартовой капчи не было')
        print()
        driver.find_element(By.CSS_SELECTOR,
                            "span.DesktopAddressButton_address").click()

        time.sleep(5)
        driver.save_screenshot('scrin/2_stop.png')

        print(f'...search address - {cafe_address}')

        home_1 = driver.find_element(By.CSS_SELECTOR,
                                     "input.AppAddressInput_addressInput.AppAddressInput_modalStyle")

        time.sleep(2)
        driver.save_screenshot('scrin/3_stop.png')

        for ch in cafe_address:
            home_1.send_keys(ch)
            time.sleep(0.2)
        print(f'...input_address -DONE {cafe_address}')

        time.sleep(2)

        # print('клик по пикселям адреса')

        # ActionChains(driver).move_by_offset(1113, 339).contextClick().perform()

        try:
            home_1.find_element('xpath', '/html/body/div[4]/div/div/div/div/div[1]/div[2]/button').click()

            print('...пробуем нажать на кнопку ОК')
            time.sleep(5)
            driver.save_screenshot('scrin/4_stop.png')


        # ok = WebDriverWait(driver, 20).until( EC.presence_of_element_located((By.XPATH, '/html/body/div[
        # 3]/div/div/div/div/div[1]/div[2]/button/span')) ) ok.click() home_1.find_element('xpath', '/html/body/div[DFFFFFFFFFDESOPPPPPPPPPP9 GB
        # 3]/div/div/div/div/div[1]/div[2]/button/span').click()

        except:
            print('!!! не вышло нажать ок !!!')

        try:
            print(f'...{cafe_address} - проверяем наличие капчи')

            wait = WebDriverWait(driver, 10)
            captcha = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div/div/div/div[3]')))

            captcha.click()
            print(f'...{cafe_address}- клик капчи')

        except Exception as ex:
            print(f'...{cafe_address}. Капчи нет, ошибку не печатаю')

        finally:
            time.sleep(5)
            try:
                print(f'...{cafe_address}. Ищу рейтинг')
                time.sleep(5)
                rating = driver.find_element(By.XPATH,
                                             '//*[@id="root"]/div/div/div[1]/div/div/div/main/div[1]/div[3]/button[2]/div/div[1]')
                print(rating.text)

                try:
                    name_file = cafe_address.strip().replace(',', '_').replace('/', '_').replace(' ', '').replace('.',
                                                                                                                  '_').replace(
                        '\n', '')

                    folder_path = os.path.join('rating')

                    file_path = os.path.join(folder_path, name_file)
                    os.makedirs(folder_path, exist_ok=True)

                    with open(file_path, 'a+', encoding='utf-8') as line:
                        line.write(f'{rating.text}\n')

                    print('...Запись рейтинга выполнена <-')
                except Exception as ex:
                    print(ex)

            except Exception as ex:
                print(f'...{cafe_address} {ex}. Рейтинг не найден')
            print(f'...{cafe_address} скролим')
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
                name_file = cafe_address.strip().replace(',', '_').replace('/', '_').replace(' ', '').replace('.',
                                                                                                              '_').replace(
                    '\n', '')

                current_datetime = datetime.datetime.now()
                folder_name = current_datetime.strftime('%d-%m_%H')
                folder_path = os.path.join('txt', folder_name)

                file_path = os.path.join(folder_path, name_file)
                os.makedirs(folder_path, exist_ok=True)

                with open(file_path, 'w', encoding='utf-8') as line:
                    for name_menu in stop_menu:
                        line.write(f'{name_menu}\n')

                folder_path = os.path.join('stop_week')

                file_path = os.path.join(folder_path, name_file)
                os.makedirs(folder_path, exist_ok=True)

                with open(file_path, 'a+', encoding='utf-8') as line:
                    for name_menu in stop_menu:
                        line.write(f'{name_menu}\n')

                print('...Запись стоп листа выполнена <-')
            except Exception as ex:
                print(ex)

        print(f'{cafe_address} Парсинг адреса закончен <-')

    except Exception as ex:
        actions = ActionChains(driver)
        time.sleep(2)
        print(ex)

    finally:
        driver.close()
        driver.quit()
