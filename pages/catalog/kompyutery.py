import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from base.base_class import Base


class KompyuteryPage(Base):
    """ класс для методов авторизации """

    url = 'https://knsrussia.kns.ru/catalog/kompyutery/'

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

# Locators

    processor_series_filter_locator = '//li[@data-name="Серия процессора"]'  # раскрыть
    processor_series_expandall_locator = '//li[@data-name="Серия процессора"]//span[text()="Показать все"]'
    processor_series_corei9_locator = '//div[@class="fv-container"]//a[text()="Intel Core i9"]/..'
    processor_series_corei7_locator = '//div[@class="fv-container"]//a[text()="Intel Core i7"]/..'

    videocard_series_filter_locator = '//li[@data-name="Видеокарта"]'  # раскрыть
    videocard_series_expandall_locator = '//li[@data-name="Видеокарта"]//span[text()="Показать все"]'
    videocard_series_model_all_shown = '//li[@data-name="Видеокарта"]//li[not(contains(@class, "dn"))]'
    videocard_series_4070_locators = '//div[@class="fv-container"]' \
                                     '//a[contains(text(),"RTX 4070") or contains(text(),"RTX 4080")]'

    ram_size_filter_locator = '//li[@data-name="Объём памяти"]'  # раскрыть
    ram_size_expandall_locator = '//li[@data-name="Объём памяти"]//span[text()="Показать все"]'
    ram_sizes_32_64_locators = '//div[@class="fv-container"]' \
                               '//a[contains(text(),"32Gb") or contains(text(),"64Gb")]'

# Getters

# Actions

    def filter_i9_i7_processors(self):
        processor_series_filter = self.get_element(self.processor_series_filter_locator)
        self.scroll_to_element(processor_series_filter)
        print("Нажимается кнопка 'Серия процессора'")
        processor_series_filter.click()
        time.sleep(1)

        processor_series_expandall = self.get_element(self.processor_series_expandall_locator)
        self.scroll_to_element(processor_series_expandall)
        print("Нажимается кнопка 'Показать все'")
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(processor_series_expandall))
        processor_series_expandall.click()
        time.sleep(1)

        processor_corei7 = self.get_element(self.processor_series_corei7_locator)
        self.scroll_to_element(processor_corei7)
        print(f"Нажимается фильтр {processor_corei7.text}")
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(processor_corei7))
        processor_corei7.click()
        time.sleep(1)

        processor_corei9 = self.get_element(self.processor_series_corei9_locator)
        self.scroll_to_element(processor_corei9)
        print(f"Нажимается фильтр {processor_corei9.text}")
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(processor_corei9))
        processor_corei9.click()
        time.sleep(1)

        self.click_finish_choice()


    def filter_4070_videocards(self):
        """ обрабатываем комплексный фильтр из нескольких элементов"""

        # [!]без дополнительных принудительных задержек тест валится, т.к. клики на фильтры рандомно сбиваются
        # само-пропадающим попапом "показать" после клика на каждом фильтре

        videocard_series_filter = self.get_element(self.videocard_series_filter_locator)
        self.scroll_to_element(videocard_series_filter)
        print("Нажимается кнопка 'Видеокарта'")
        videocard_series_filter.click()
        time.sleep(1)

        videocard_expandall = self.get_element(self.videocard_series_expandall_locator)
        self.scroll_to_element(videocard_expandall)
        print("Нажимается кнопка 'Показать все'")
        videocard_expandall.click()
        time.sleep(1)

        # Надо ожидать пока элементы списка не станут все видимыми (класс "dn" удален из <li>)
        WebDriverWait(self.driver, 3).until(
            lambda driver: len(driver.find_elements(By.XPATH, self.videocard_series_model_all_shown)) > 0
        )

        videocard_series_4070_filter_list = self.get_elements(self.videocard_series_4070_locators)
        for video_link in videocard_series_4070_filter_list:
            time.sleep(1)
            self.scroll_to_element(video_link)
            # иногда попап с предложением "показать" возникает поверх списка фильтров, и клик попадает не в фильтр,
            # а в постороннее окно, выбрасывая исключение
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(video_link))
            print(f"Нажимается фильтр {video_link.text}")
            video_link.click()

        time.sleep(1)
        self.click_finish_choice()



    def filter_32_64_ram(self):
        """ обрабатываем комплексный фильтр из нескольких элементов"""
        ram_size_filter = self.get_element(self.ram_size_filter_locator)
        self.scroll_to_element(ram_size_filter)
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(ram_size_filter))
        print(f"Нажимается кнопка '{ram_size_filter.text}'")
        ram_size_filter.click()

        ram_size_expandall = self.get_element(self.ram_size_expandall_locator)
        WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(ram_size_expandall))
        ram_size_expandall.click()

        ram_size_filter_list = self.get_elements(self.ram_sizes_32_64_locators)
        for ram_filter in ram_size_filter_list:
            self.scroll_to_element(ram_filter)
            WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(ram_filter))
            ram_filter.click()
            print(f"Нажимается фильтр {ram_filter.text}")

        time.sleep(1)
        self.click_finish_choice()

# Methods