import time
from base.base_class import Base
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MonitoryPage(Base):
    """ класс для методов авторизации """

    url = 'https://knsrussia.kns.ru/catalog/monitory/'

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

# Locators

    mon_model_type_ultrawide = '//label[@data-path="Мониторы}LG}UltraWide"]'
    mon_matrix_type_locator = '//li[@data-name="Тип матрицы"]'
    mon_matrix_type_IPS_locator = '//div[@class="fv-container"]//label/a[text()="IPS"]'

# Getters

# Actions


    def select_filter_ultrawide(self):
        filter_subrubricks_ultrawide = self.get_element(self.mon_model_type_ultrawide)
        print(f'Нажат чекбокс-линк для фильтра "Подрубрики: Ultrawide" с локатором {self.mon_model_type_ultrawide}')
        filter_subrubricks_ultrawide.click()
        time.sleep(1)


    def expand_category_matrix_type(self):
        self.expand_filter(self.mon_matrix_type_locator)


    def select_filter_IPS(self):

        filter_IPS = self.get_element(self.mon_matrix_type_IPS_locator)
        print(f'Нажат чекбокс-линк для фильтра "Подрубрики: Ultrawide" с локатором {self.mon_matrix_type_IPS_locator}')
        filter_IPS.click()
        time.sleep(1)


# Methods