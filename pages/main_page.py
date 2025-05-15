import time
from base.base_class import Base
from utils.logger import Logger


class MainPage(Base):
    """ класс для методов авторизации """

    url = 'https://knsrussia.kns.ru/'

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

# Locators

# Getters

# Actions

    def click_menu_item(self, item_name):
        item_link_locator = f'//a[text()="{item_name}"]'
        menu_item_element = self.get_element(item_link_locator)
        self.scroll_to_element(menu_item_element)
        Logger.log_event(f'Скролл до элемента меню "{item_name}"')
        # time.sleep(1)
        menu_item_element.click()
        Logger.log_event(f'Нажата кнопка с локатором {item_link_locator}')
        # time.sleep(1)

    def hover_menu_item(self, item_name):
        item_link_locator = f'//a[text()="{item_name}"]'
        menu_item_element = self.get_element(item_link_locator)
        self.move_to_element(menu_item_element)
        Logger.log_event(f'Наводим фокус на элемент меню "{item_name}"')


# Methods

