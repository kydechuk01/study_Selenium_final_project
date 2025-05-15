from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from utils.logger import Logger


@pytest.fixture()
def conftest_driver():
    options = webdriver.ChromeOptions()  # настройки браузера
    options.add_experimental_option('detach', True)  # опция, которая не позволит Chrome закрыться
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # отключает лишние сообщения в консоли
    options.add_argument("--guest")  # отключение оповещения с просьбой смены пароля
    options.add_argument('--disable-translate')  # отключаем предложение перевести страницу
    options.add_argument('--disable-features=Translate')  # отключаем предложение перевести страницу
    options.add_argument("--log-level=1")  # подавляем сообщение в консоли "TensorFlow Lite XNNPACK delegate for CPU."
    options.add_argument('--window-size=1728,1080')
    # options.add_argument('--headless')  # <---- бесшумный режим
    service = ChromeService(ChromeDriverManager().install())
    chromedriver = webdriver.Chrome(service=service, options=options)

    Logger.log_event('|-->> Start test')
    yield chromedriver
    Logger.log_event('-->>| Finish test')

    chromedriver.close()