from base.base_class import Base
from utils.logger import Logger


class BasketPage(Base):
    """ класс для методов КОРЗИНЫ """

    url = 'https://knsrussia.kns.ru/basket.aspx'

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

# Locators

    basket_container_locator = '//div[@id="BasketFull"]'
    basket_container_title = 'Ваша корзина'
    basket_items_list_locator = '//div[contains(@class,"item") and string-length(@data-id) > 0]'
    basket_total_summ_locator = '//span[@id="BasketPos_TotalSumRUR"]'
    # в span поле data-basketpos_totalsumrur="NNNNN" <-сумма

# Getters

# Actions

    def assert_in_basket(self):
        self.get_current_url()
        basket_container_text = self.get_element(self.basket_container_locator).text
        assert basket_container_text.lower() == self.basket_container_title.lower(), f'Ошибка. Не найден ожидаемый ' \
                                                                                     f'заголовок корзины: \
                                                                                     "{self.basket_container_title}\".'
        return Logger.log_event('Мы на странице корзины')

    def get_basket_items_list(self):
        """ Получаем список товаров в корзине"""
        basket_list = self.get_elements(self.basket_items_list_locator)
        basket_goods_list = []
        for item in basket_list:
            name = item.get_attribute('data-name')
            price = item.get_attribute('data-price')
            sku = item.get_attribute('data-id')
            basket_goods_list.append({
                'name': name,
                'price': price,
                'sku': sku
            })
        return basket_goods_list

    def get_basket_total_summ(self) -> int:
        basket_total_summ = self.get_element(self.basket_total_summ_locator)
        total_summ = basket_total_summ.get_attribute('data-basketpos_inittotalsumrur')
        return int(total_summ)

# Methods

    def compare_order_with_basket(self, order_list):
        """ сравнение списка ранее заказанных товаров с корзиной
        формат order_list - list[objects]
        object = product_item = {
                'name': name,
                'url': url,
                'desc': desc,
                'price': price,
                'sku': sku,
                'add_to_basket_link': add_to_basket_link
                }
        """
        cleaned_order_list = []
        for order_item in order_list:
            """ формируем краткий список заказанного"""
            cleaned_order_list.append({
                'name': order_item['name'],
                'price': order_item['price'],
                'sku': order_item['sku']
            })
        basket_list = self.get_basket_items_list()

        # сортируем списки перед сравнением
        basket_list = sorted(basket_list, key=lambda x: x['sku'])
        cleaned_order_list = sorted(cleaned_order_list, key=lambda x: x['sku'])

        # проверка на длину списков
        assert len(basket_list) == len(cleaned_order_list), 'Количество товаров в заказе и в корзине отличаются друг ' \
                                                            'от друга!'

        # собираем несовпадения в товарах через функцию zip для кортежей
        mismatches = []
        for order_item, basket_item in zip(cleaned_order_list, basket_list):
            # важный момент, т.к. в магазине KNS к именам товаров в каталоге добавляется тип товара ("Монитор")
            # а названиях этих товаров в корзине этот тип уже отсутствует! ;-(
            if basket_item['name'] not in order_item['name']:
                mismatches.append((basket_item['name'], order_item['name']))

        # финальная проверка
        assert not mismatches, f'Несовпадения в списках заказа и товаров в корзине:\n{mismatches}'

        Logger.log_event('Список товаров в заказе совпал со списком в корзине!')


    def compare_order_summ_with_basket(self, order_list):
        """ сравнение суммы товаров в заказе с общей суммой из корзины """
        order_summ = sum(int(item['price']) for item in order_list)
        basket_summ = self.get_basket_total_summ()

        # вводим показатель погрешности округления сумм в 2 рубля
        # отладка тестирования показала, что значение в корзине округляется иногда с расхождением в 1 рубль
        tolerance = 2

        Logger.log_event(f'Стоимость заказанного товара ({order_summ}) совпадает с суммой в корзине ({basket_summ}).')
        assert abs(order_summ - basket_summ) <= tolerance, f'Ошибка. Стоимость заказанного товара ' \
                                                           f'({order_summ}) с учетом погрешности {tolerance} не ' \
                                                           f'совпадает с тем, что выводится в {basket_summ} корзине!'