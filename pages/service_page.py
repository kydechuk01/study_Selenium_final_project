import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from base.base_class import Base


class ServicePage(Base):
    """ класс для методов авторизации """

    url = 'https://knsrussia.kns.ru/service.html'

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

# Locators

    login_locator = '//input[@id="login"]'
    password_locator = '//input[@id="pass"]'
    enter_btn_locator = '//input[@type="submit" and @value="Войти"]'
    logout_link_locator = '//a[@href="/service.html?logoff=1"]'
    alert_login_locator = '//small[contains(@class, "alert-danger")]'
    alert_wrong_login_message = 'Не верно указан логин или пароль'
    cabinet_orders_list_locator = '//h3[contains(text(), "Список Ваших заказов")]'
    cabinet_orders_list_message = 'Список Ваших заказов'

# Getters

    def get_input_login(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.login_locator)))

    def get_input_password(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.password_locator)))

    def get_button_enter(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.enter_btn_locator)))

    def get_logout_link(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.logout_link_locator)))

    def get_login_alert(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.alert_login_locator)))

    def get_cabinet_orderslist_title(self):
        return WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.cabinet_orders_list_locator)))

# Actions

    def enter_login_password(self, login, password):
        input_login = self.get_input_login()
        input_password = self.get_input_password()
        input_login.send_keys(login)
        time.sleep(2)
        input_password.send_keys(password)

    def click_enter(self):
        enter_button = self.get_button_enter()
        enter_button.click()

    def open_page(self):
        self.driver.get(self.url)
        self.get_current_url()

    def assert_wrong_login(self):
        """ тест на заведомо некорректный логин"""
        assert self.get_login_alert().text == self.alert_wrong_login_message, \
            'Сообщение об неверном логине или пароле не обнаружено!'
        print(f'Авторизация не пройдена. Обнаружено сообщение "{self.alert_wrong_login_message}".')

    def assert_good_login(self):
        """ попытка успешной авторизации"""
        assert self.get_cabinet_orderslist_title().text == self.cabinet_orders_list_message, \
            'Авторизация не прошла. Ошибка в логине или пароле.'
        print(f'Авторизация успешно пройдена.')


    def logout(self):
        logout_link = self.get_logout_link()
        logout_link.click()
        print(f'Нажата ссылка logoff')
        self.get_current_url()

# Methods

    def authorize(self, login, password, bad_login=False):
        """ если bad_login==True, то тестируется негативный сценарий с неверным логином"""
        if bad_login:
            print('Авторизация по негативному сценарию')
        else:
            print('Авторизация по позитивному сценарию')

        self.open_page()
        self.enter_login_password(login, password)
        time.sleep(1)
        self.click_enter()
        time.sleep(1)
        if bad_login:
            self.assert_wrong_login()
        else:
            self.assert_good_login()
        time.sleep(3)