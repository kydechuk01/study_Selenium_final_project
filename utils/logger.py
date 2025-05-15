import datetime


class Logger:
    """ Класс для логирования результатов в файл: """

    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = f'./logs/log_{current_time}.log'

    @classmethod
    def log_write_to_file(cls, log_data: str):
        try:
            with open(cls.log_filename, 'a', encoding='utf-8') as log_file:
                log_file.write(log_data)
        except (OSError, PermissionError, ValueError) as err:
            print(f'Ошибка записи в лог {cls.log_filename}: {err}. Данные для записи: {log_data}')


    @classmethod
    def log_event(cls, message: str):
        log_data = f"{str(datetime.datetime.now())} {message}\n"
        cls.log_write_to_file(log_data)