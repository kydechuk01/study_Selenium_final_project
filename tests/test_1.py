import time
import pytest
from selenium.webdriver.remote.webelement import WebElement

from pages.main_page import MainPage
from pages.service_page import ServicePage
from pages.catalog.monitory import MonitoryPage
from pages.catalog.kompyutery import KompyuteryPage
from pages.basket import BasketPage
from utils.logger import Logger


class Test_smoke:

    @pytest.mark.last
    def test_critical_path(self, conftest_driver):

        """ проверка критического пути заказа товаров из разных категорий с фильтрами"""

        # [!] бОльшая часть задержек time.sleep нужна для визуальной демонстрации, чтобы не мелькало

        # переменные my_login, my_pass хранятся в .\auth_info\login_pass.py,
        # исключенном из проекта через .gitignore
        try:
            from auth_info.login_pass import my_login, my_pass
        except ImportError:
            my_login, my_pass = None, None  # Если модуль не был найден, задаем пустые значения

        driver = conftest_driver  # получили драйвер из фикстуры

        """ подключаем классы СТРАНИЦ """

        service_page = ServicePage(driver)  # подключили класс страницы логина
        mp = MainPage(driver)  # подключили класс заглавной страницы /
        cat_mon = MonitoryPage(driver)  # класс каталог/мониторы
        cat_komp = KompyuteryPage(driver)  # класс каталог/компьютеры
        basket = BasketPage(driver)  # класс корзины

        # скипаем процедуру авторизации, если у нас не подгрузились логин и пароль
        if my_login and my_pass:
            Logger.log_event(f'Попытка логина с данными: {my_login} : {my_pass[:2]}{"*" * (len(my_pass) - 2)}')
            service_page.authorize(my_login, my_pass)
            time.sleep(1)
        else:
            Logger.log_event('Файл auth_info\\login_pass.py отсутствует. Пропускаем этап авторизации. ')

        # service_page.logout()  # пока отключено за ненадобностью в этом тесте

        # будущий список заказов
        ordered_items = []

        mp.open_page()
        time.sleep(1)

        mp.click_cookie()
        time.sleep(0.5)

        """ Подтест-1: добавляем МОНИТОРЫ """

        category_monitors_itemname = 'Мониторы'
        sub_cat_monitors_lg_itemname = 'Мониторы LG'

        mp.hover_menu_item(category_monitors_itemname)
        time.sleep(0.5)
        mp.hover_menu_item(sub_cat_monitors_lg_itemname)
        time.sleep(0.5)
        mp.click_menu_item(sub_cat_monitors_lg_itemname)
        time.sleep(0.5)
        mp.get_current_url()

        cat_mon.select_filter_ultrawide()
        cat_mon.click_search_popup_show_link()
        mp.get_current_url()
        time.sleep(0.5)

        """ Установка фильтров МОНИТОРЫ: BEGIN """

        cat_mon.expand_category_matrix_type()
        time.sleep(0.5)

        cat_mon.select_filter_IPS()
        cat_mon.click_search_popup_show_link()
        cat_mon.get_current_url()
        time.sleep(0.5)

        cat_mon.enter_price_value_until(50000)
        cat_mon.enter_price_value_from(20000)
        cat_mon.get_current_url()
        time.sleep(1)

        cat_mon.set_sort_by_price("DESC")
        time.sleep(0.5)

        """ Установка фильтров МОНИТОРЫ: END """

        monitors_list = mp.get_goods_items_list()
        Logger.log_event(f'\nПолучено {len(monitors_list)} товаров:')
        cat_mon.print_goods_items_list(monitors_list)

        Logger.log_event("\nДобавляем 3 монитора в список заказанных товаров:")

        monitors_ordered = []  # пустой список для логической точки отсчета
        monitors_ordered += monitors_list[0:3]  # добавляем заказанное в список
        cat_mon.print_goods_items_list(monitors_ordered)

        Logger.log_event("\nДобавляем товары в корзину:")
        for item in monitors_ordered:
            basket_element: WebElement = item['add_to_basket_link']
            Logger.log_event(f"Добавление к корзину: {item['name']}, цена {item['price']}")
            mp.add_to_basket(basket_element)

        ordered_items += monitors_ordered  # добавляем заказанные мониторы в общий список

        time.sleep(1)
        basket.open_page()
        basket.compare_order_with_basket(ordered_items)
        basket.compare_order_summ_with_basket(ordered_items)

        Logger.log_event("Проверка функционала Выбор МОНИТОРА завершена. <--|")

        """ Подтест-2: добавляем КОМПЬЮТЕР """

        Logger.log_event("Начало проверки функционала Выбор ПК |-->.")

        cat_komp.open_page()
        cat_komp.get_current_url()

        """ Установка фильтров КОМПЬЮТЕРЫ: BEGIN """

        cat_komp.filter_i9_i7_processors()
        time.sleep(0.5)
        cat_komp.filter_32_64_ram()
        time.sleep(0.5)
        cat_komp.filter_4070_videocards()
        time.sleep(0.5)
        cat_komp.click_finish_choice()
        time.sleep(0.5)

        cat_komp.enter_price_value_from(100000)
        cat_komp.enter_price_value_until(250000)
        cat_komp.get_current_url()
        cat_komp.set_sort_by_price("ASC")

        """ Установка фильтров КОМПЬЮТЕРЫ: BEGIN """

        cat_komp.get_current_url()

        computers_list = mp.get_goods_items_list()
        Logger.log_event(f'\nПолучено {len(computers_list)} товаров:')
        cat_komp.print_goods_items_list(computers_list)

        Logger.log_event("\nДобавляем первые два в списке Компьютер в список заказанных товаров:")
        computers_ordered = [computers_list[0]]  # создаем список из 1 товара
        cat_komp.print_goods_items_list(computers_ordered)

        Logger.log_event("\nДобавляем товары в корзину:")
        for item in computers_ordered:
            basket_element: WebElement = item['add_to_basket_link']
            Logger.log_event(f"Добавление к корзину: {item['name']}, цена {item['price']}")
            mp.add_to_basket(basket_element)

        ordered_items += computers_ordered  # добавляем выбранные компьютеры в общий список товаров

        time.sleep(1.5)
        basket.open_page()
        basket.compare_order_with_basket(ordered_items)
        basket.compare_order_summ_with_basket(ordered_items)

        Logger.log_event("Проверка функционала Выбор ПК завершена. <--|")
        Logger.log_event("Тест критического пути завершен. <--|")

    # @pytest.mark.skip(reason="Пропускаем этот тест на время основной отладки")
    @pytest.mark.tryfirst
    def test_wrong_authorization(self, conftest_driver):
        """ проверка заведомо некорректного логина """

        my_login = 'test_login'
        my_pass = 'test_pass'
        driver = conftest_driver
        service_page = ServicePage(driver)
        Logger.log_event(f'Попытка логина с несуществующими данными: {my_login} : {my_pass}')
        service_page.authorize(my_login, my_pass, bad_login=True)
