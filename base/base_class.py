import time
from typing import List

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

from utils.logger import Logger


class Base:
    """ ОСНОВНОЙ КЛАСС ПРОЕКТА
        здесь хранятся локаторы и методы, универсальные для нескольких страниц сайта
    """

    url = 'https://knsrussia.kns.ru/'

    def __init__(self, driver: WebDriver):
        self.driver = driver

    # Locators

    # кнопка принять куки
    cookie_agree_button_locator = '//a[contains(@onclick, "CreateCookie")]'

    # единый попап с саммари поиска для всех страниц каталога
    search_popup_locator = '//div[@id="SearchExtPopup"]'  # появляется на 3 сек
    search_popup_link_locator = '//div[@id="SearchExtPopup"]/a[text()="Показать"]'  # кликабельно

    # локатор кнопки "Выбрать" (применить все фильтры)
    filter_choice_locator = '//a[text()="Выбрать"]'

    # локатор полей фильтра: цена от, цена до
    price_from_locator = '//input[@type="text" and @aria-label="Цена от" and @name="s_price1"]'
    price_until_locator = '//input[@type="text" and @aria-label="Цена до" and @name="s_price2"]'

    # локатор кнопки сортировки товаров
    sort_locator = '//div[@class="choice-sort-type"]'
    sort_by_price_locator = '//div[@class="choice-sort-type"]/a[@data-id="Price"]'

    # список единиц товара в каталоге (many):
    goods_itemlist_node_locator = '//div[contains(@class,"item") and @itemscope="itemscope"]'

    # суб-локаторы для ноды товара:
    goods_item_name_sub_locator = './/span[@itemprop="name"]'
    goods_item_url_sub_locator = '//a[@itemprop="url"]'
    goods_item_desc_sub_locator = './/div[@itemprop="description"]'
    goods_item_price_sub_locator = './/meta[@itemprop="price"]'
    goods_item_sku_sub_locator = './/span[@itemprop="sku"]'
    goods_item_add_to_basket_sub_locator = './/a[contains(@class,"basket-add") and @data-ga-event="add_to_cart"]'

    # локатор нажатия "Оформить заказ" (добавить товар в корзину)
    # <button type="button" class="btn btn-link btn-sm" data-dismiss="modal">Продолжить покупки</button>
    basket_modal_continue_shopping_locator = '//button[@data-dismiss="modal"]'

    # Getters

    def get_current_url(self):
        url = self.driver.current_url
        Logger.log_event('Текущий url = ' + url)
        return url


    def get_element(self, locator) -> WebElement:
        """ На входе принимает текстовый XPATH-локатор, на выходе возвращает WebElement """
        """ после неудачных попыток определить элемент, скрытый за пределами скролл-бокса, 
            меняем element_to_be_clickable на presence_of_element_located"""
        return WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, locator)))

    def get_elements(self, locator) -> List[WebElement]:
        """ На входе принимает текстовый XPATH-локатор, на выходе возвращает WebElement """
        return WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, locator)))


    def get_cookie_button(self):
        # вернем веб-элемент с кнопкой закрытия куки или None, если ее нет на странице
        try:
            return WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH,self.cookie_agree_button_locator))
            )
        except (NoSuchElementException, TimeoutException):
            return None

# Actions

    @staticmethod
    def assert_webelement_text(webelement, expected_text):
        """ Проверка соответствия значения .text для элемента ожидаемому """
        textvalue = webelement.text
        assert textvalue == expected_text, f"Значение {textvalue} не соответствует ожидаемому {expected_text}"
        Logger.log_event(f'Проверка значения элемента {textvalue} - ОК')


    def scroll_to_element(self, element: WebElement):
        if self.driver is None or element is None:
            Logger.log_event("Ошибка scroll_to_element: driver или element = None")
            raise ValueError("Driver/element не может быть None")
        try:
            # actions = ActionChains(self.driver)
            # actions.scroll_to_element(element).perform()
            # [!] для блока фильтров у сайта kns почему-то лучше работает скролл через js, иначе через раз вываливается
            # очень странная ошибка ElementClickInterceptedException с причиной "элемент перекрывает сам себя"
            # [!] причем наиважнейший аргумент в скролле - это block:'center'
            # Logger.log_event(f'scroll до элемента {element.text}')
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)  # js-прокрутка
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(element))

        except (StaleElementReferenceException,
                NoSuchElementException,
                ElementNotInteractableException,
                AttributeError) as err:
            Logger.log_event(f'Ошибка scroll_to_element {element.text}: {err}')
            return


    def move_to_element(self, element: WebElement):
        if self.driver is None or element is None:
            Logger.log_event("Ошибка move_to_element: driver или element = None")
            raise ValueError("Driver/element не может быть None")
        try:
            actions = ActionChains(self.driver)
            # Logger.log_event(f'Перемещение курсора к элементу {element.text}')
            actions.move_to_element(element).perform()
        except (StaleElementReferenceException,
                NoSuchElementException,
                ElementNotInteractableException,
                AttributeError) as err:
            Logger.log_event(f'Ошибка move_to_element {element.text}: {err}')
            return


    def click_cookie(self):
        """ кликаем куку при открытии страницы, или пропуск, если ее нет """
        cookie_button = self.get_cookie_button()
        if cookie_button is not None:
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(cookie_button))
            cookie_button.click()
            Logger.log_event('Нажата кнопка "Принять" для cookie-alert')


    def js_click(self, element: WebElement):
        # для некоторых случаев, когда кнопка не нажимается обычным методом
        Logger.log_event('Запущено нажатие на кнопку при помощи js.click()')
        self.driver.execute_script("arguments[0].click();", element)


    def expand_filter(self, locator):
        expand_node = self.get_element(locator)
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(expand_node))
        expand_node.click()
        Logger.log_event(f'Нажата категория фильтра: {expand_node.text}')


    def click_search_popup_show_link(self):
        """ клик на всплывашке с итогами поиска,
        которая появляется на 3 секунды после изменения фильтров"""
        try:
            search_popup_node = self.get_element(self.search_popup_locator)
            search_summary = str(search_popup_node.text)
            search_summary = search_summary.split('\n')[0]
        except TimeoutException:
            Logger.log_event('Попап не появился')
        else:
            search_popup_link = self.get_element(self.search_popup_link_locator)
            self.scroll_to_element(search_popup_link)
            Logger.log_event(f"Нажимается кнопка '{search_popup_link.text}' на всплывающем попапе с сообщением {search_summary}")
            # self.js_click(search_popup_link)
            WebDriverWait(self.driver, 2).until(EC.element_to_be_clickable(search_popup_link))
            search_popup_link.click()


    def click_finish_choice(self):
        """ Клик на кнопке подтверждения выбора всех фильтров """
        finish_choice_link = self.get_element(self.filter_choice_locator)
        self.scroll_to_element(finish_choice_link)
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(finish_choice_link))
        Logger.log_event("Нажимается кнопка 'Выбрать' для подтверждения всех фильтров")
        finish_choice_link.click()


    def enter_price_value_from(self, value: int):
        """ ввод ЗНАЧЕНИЯ в поле ЦЕНА ОТ """
        price_from_element = self.get_element(self.price_from_locator)
        price_until_element = self.get_element(self.price_until_locator)
        price_value_min = int(price_from_element.get_attribute("data-value-min"))
        price_value_max = int(price_until_element.get_attribute("data-value-max"))
        if price_value_min < value < price_value_max:
            Logger.log_event(f'Фильтр "ЦЕНА ОТ/ДО" содержит мин/макс значения: {price_value_min}/{price_value_max}. '
                             f'Устанавливаем новое значение ОТ = {value}')
            self.scroll_to_element(price_from_element)
            price_from_element.send_keys(str(value))
            price_from_element.send_keys(Keys.RETURN)
            self.click_search_popup_show_link()

            price_from_element = self.get_element(self.price_from_locator)
            price_from_value = int(price_from_element.get_attribute("data-value"))

            # тест успешности метода
            assert price_from_value == value, f'Не получилось установить поле фильтра: ЦЕНА ОТ = {value}'
            Logger.log_event(f"Новое значение фильтра ЦЕНА ОТ: {price_from_value}")

        else:
            Logger.log_event(f'Новое значение ЦЕНА ОТ = {value} выходит за границы диапазона "ЦЕНА ОТ/ДО": '
                             f'{price_value_min}/{price_value_max}. Установка значения невозможна.')


    def enter_price_value_until(self, value: int):
        """ вводим ЗНАЧЕНИЕ в поле ЦЕНА ДО """
        price_from_element = self.get_element(self.price_from_locator)
        price_until_element = self.get_element(self.price_until_locator)
        price_value_min = int(price_from_element.get_attribute("data-value-min"))
        price_value_max = int(price_until_element.get_attribute("data-value-max"))
        if price_value_min < value < price_value_max:
            Logger.log_event(f'Фильтр "ЦЕНА ОТ/ДО" содержит мин/макс значения: {price_value_min}/{price_value_max}. '
                             f'Устанавливаем новое значение ДО = {value}')
            self.scroll_to_element(price_until_element)
            price_until_element.send_keys(str(value))
            price_until_element.send_keys(Keys.RETURN)
            self.click_search_popup_show_link()

            time.sleep(10)
            price_until_element = self.get_element(self.price_until_locator)
            price_until_value = int(price_until_element.get_attribute("data-value"))

            # тест успешности метода
            assert price_until_value == value, f'Не получилось установить поле фильтра: ЦЕНА ДО = {value}'
            Logger.log_event(f"Новое значение фильтра ЦЕНА ОТ: {price_until_value}")

        else:
            Logger.log_event(f'Новое значение ЦЕНА ДО = {value} выходит за границы диапазона "ЦЕНА ОТ/ДО": '
                             f'{price_value_min}/{price_value_max}. Установка значения невозможна.')


    def set_sort_by_price(self, sort_order:str = "ASC"):
        """ Установка сортировки по цене и выбранному порядку
            особенность сценария в том, что при установке типа или порядка сортировки
            страница перезагружается и надо:
             а) искать локаторы заново,
             б) заново анализировать и ставить порядок сортировки """

        sort_node = self.get_element(self.sort_locator)
        sort_by_price = self.get_element(self.sort_by_price_locator)
        current_sort_type = sort_node.get_attribute("data-sort-type")  # "Price"
        current_sort_order = sort_node.get_attribute("data-id")  # "ASC", "DESC"
        Logger.log_event(f'Текущий режим сортировки: по {current_sort_type}:{current_sort_order}')
        Logger.log_event(f'Попытка установить сортировку: по ЦЕНА:{sort_order}')

        # проверяем случай, когда настройки сортировки уже те, которые нужны
        if current_sort_type == "Price" and current_sort_order == sort_order:
            Logger.log_event(f'Сортировка: по ЦЕНА:{sort_order} задана успешно.')
            return

        if current_sort_type != "Price":
            # сначала надо установить Price в качестве целевой сортировки,
            # помним, что это действие сбрасывает порядок сортировки
            sort_by_price.click()
            Logger.log_event(f"Тип сортировки не соответствует. Нажата кнопка сортировки: по ЦЕНА.")
            # time.sleep(1)

            # перечитываем состояние узла сортировки
            sort_node = self.get_element(self.sort_locator)
            sort_by_price = self.get_element(self.sort_by_price_locator)
            current_sort_type = sort_node.get_attribute("data-sort-type")
            current_sort_order = sort_node.get_attribute("data-id")

        if current_sort_order != sort_order:
            inverse_sort_order = sort_node.get_attribute("data-inverse")
            Logger.log_event(f'Меняем порядок сортировки на: {inverse_sort_order}')
            sort_by_price.click()  # повторный клик для инверсии сортировки
            # time.sleep(1)
            # еще раз перечитываем состояние узла сортировки
            sort_node = self.get_element(self.sort_locator)
            current_sort_type = sort_node.get_attribute("data-sort-type")
            current_sort_order = sort_node.get_attribute("data-id")

        # финальная проверка
        assert current_sort_type == "Price" and current_sort_order == sort_order, f"Ошибка выбора сортировки: по " \
                                                                                  f"ЦЕНА:{sort_order}"
        Logger.log_event(f'Сортировка: по ЦЕНА:{sort_order} задана успешно.')
        return

# Methods

    def open_page(self):
        self.driver.get(self.url)
        self.get_current_url()
        self.click_cookie()  # кликаем куку при открытии страницы, или пропуск, если ее нет


    def get_goods_items_list(self) -> List:
        """ Получаем товар №1 в отфильтрованном каталоге
            возвращаем объект с товаром"""
        # список с товарами на странице
        goods_itemlist_node = self.get_elements(self.goods_itemlist_node_locator)
        itemlist = []
        for item in goods_itemlist_node:
            name = item.find_element(By.XPATH, self.goods_item_name_sub_locator).text
            url = item.find_element(By.XPATH, self.goods_item_url_sub_locator).get_attribute('href')
            desc = item.find_element(By.XPATH, self.goods_item_desc_sub_locator).text
            price = item.find_element(By.XPATH, self.goods_item_price_sub_locator).get_attribute('content')
            sku = item.find_element(By.XPATH, self.goods_item_sku_sub_locator).text
            add_to_basket_link = item.find_element(By.XPATH, self.goods_item_add_to_basket_sub_locator)  # webelement
            product_item = {
                'name': name,
                'url': url,
                'desc': desc,
                'price': price,
                'sku': sku,
                'add_to_basket_link': add_to_basket_link
                }
            itemlist.append(product_item)
        return itemlist

    @staticmethod
    def print_goods_items_list(goods_list):
        """ вывод в консоль списка товаров """
        if len(goods_list) < 1:
            return Logger.log_event('Список товаров пуст.')
        for i, item in enumerate(goods_list):
            output = f'Товар # {i}: {item["name"]} (sku:{item["sku"]}). Цена: {item["price"]}.'
            output += f'\n Ссылка: {item["url"]}'
            Logger.log_event(output)


    def add_to_basket(self, add_to_basket_button: WebElement):
        """ 1) нажатие на кнопку "добавить в корзину"
            2) закрыть модальное окно (продолжить покупки)
            """
        add_to_basket_button.click()
        time.sleep(0.85)
        continue_shopping_link = self.get_element(self.basket_modal_continue_shopping_locator)
        continue_shopping_link.click()
