import os
import sys
import logging
import datetime
from sqlite3 import connect, Connection
from scripts.variables import *


class Environment(object):
    """
    DESCR:
    REQUIRE:
    RETURN: 
    """

    def __new__(cls, *args, **kwargs) -> object:
        instance = super().__new__(cls)
        instance.log = None
        
        return instance

    def __init__(self) -> None:

        return None


    def check_config_file_exists(self) -> int:
        """
        DESCR:
        REQUIRE:
        RETURN: 
        """
        if os.path.isfile(os.getcwd() + "\\config.cfg") is False:
            CONTROLS["env"].log.debug(f"Error code: 1 - {ERRORS[1]}")
            CONTROLS["env"].log.warn("Файл конфигурации не обнаружен.")
            return 1
        else:
            CONTROLS["env"].log.info("Файл конфигурации обнаружен.")

        return 0

    def check_db_file_exists(self) -> int:
        """
        DESCR:
        REQUIRE:
        RETURN: 
        """
        if os.path.isfile(CONFIG["db_path"]) is False:
            CONTROLS["env"].log.debug(f"Error code: 1 - {ERRORS[1]}")
            CONTROLS["env"].log.warn("Файл базы данных не обнаружен.")
            return 1
        else:
            CONTROLS["env"].log.info("Файл базы данных обнаружен.")
        
        return 0


    def create_db_file(self) -> int:
        """
        DESCR:
        REQUIRE:
        RETURN: 
        """
        CONTROLS["env"].log.debug("Создание файла базы...")
        try:
            CONTROLS["db_bus"].create_database()
        except Exception as ex:
            CONTROLS["env"].log.debug(f"Error code: 2 - {ERRORS[2]}")
            CONTROLS["env"].log.error("Не удалось создать файл базы данных.")
            CONTROLS["env"].log.debug(f"Raw exception data: {ex.__str__()}")
            return 2
        CONTROLS["env"].log.info("Файл базы данных успешно создан.")
        
        return 0
    
    def create_base_dirs(self,) -> None:
        """
        DESCR:
        REQUIRE:
        RETURN: 
        """
        if os.path.exists(os.getcwd() + "\\logs") is False:
            os.mkdir(os.getcwd() + "\\logs")
        if os.path.exists(os.getcwd() + "\\reports") is False:
            os.mkdir(os.getcwd() + "\\reports")

        return None

    def initiate_default_config(self) -> None:
        """
        DESCR:
        REQUIRE:
        RETURN: 
        """
        CONTROLS["env"].log.debug("Инициализация значений по умолчанию для конфигурации.")
        CONFIG["db_path"] = f"{os.getcwd()}\\opdb.db"
        CONFIG["def_btn1"] = 100
        CONFIG["def_btn2"] = 150
        CONFIG["def_btn3"] = 300
        CONFIG["def_btn4"] = 500
        CONFIG["def_btn5"] = 1000
        CONFIG["def_btn6"] = 1500
        
        return None
    
    def initiate_log_file(self) -> None:
        """
        DESCR:
        REQUIRE:
        RETURN: 
        """
        with open(file=f".\\logs\\Y1_{datetime.datetime.now().date()}_app.log", mode='a', encoding="utf-8") as f:
            f.write("")
        
        logging.basicConfig(filename=f".\\logs\\Y1_{datetime.datetime.now().date()}_app.log",
                            filemode='a', level=logging.DEBUG,datefmt="%H:%M:%S", 
                            format="%(asctime)s.%(msecs)d %(name)s %(levelname)s %(message)s",)
        self.log = logging.getLogger("general_logger")

        return None

    def load_config_from_file(self) -> int:
        """
        DESCR:
        REQUIRE:
        RETURN: 
        """
        CONTROLS["env"].log.debug("Загрузка конфигурации...")
        try:
            buffer = open(file=LOCAL_VARS["conf_path"], mode='r', encoding="utf-8").readlines()
        except Exception as ex:
            CONTROLS["env"].log.debug(f"Error code: 2 - {ERRORS[2]}")
            CONTROLS["env"].log.error("Не удалось загрузить файл конфигурации.")
            CONTROLS["env"].log.debug(f"Raw exception data: {ex.__str__()}")
            
            return 2
        CONTROLS["env"].log.debug("Файл конфигурации загружен.")
        CONTROLS["env"].log.debug("Чтение конфигурации...")
        try:
            for line in buffer:
                conf_line = line.split('=')
                if conf_line[0] in CONFIG.keys():
                    CONFIG[conf_line[0]] = conf_line[1][:-1]
                else:
                    CONTROLS["env"].log.debug(f"Error code: 3 - {ERRORS[3]}")
                    CONTROLS["env"].log.error("Файл конфигурации имеет неверный формат.")
                    return 3
        except Exception as ex:
            CONTROLS["env"].log.debug(f"Error code: 3 - {ERRORS[3]}")
            CONTROLS["env"].log.error("Файл конфигурации имеет неверный формат.")
            CONTROLS["env"].log.debug(f"Raw exception data: {ex.__str__()}")
            return 3
        
        CONTROLS["env"].log.info("Конфигурация загружена.")
        return 0

    def open_db_file(self) -> int:
        """
        DESCR:
        REQUIRE:
        RETURN: 
        """
        result = None
        
        CONTROLS["env"].log.debug("Открытие файла базы...")
        try:
            CONTROLS["db_bus"].open_db_file()
        except Exception as ex:
            CONTROLS["env"].log.debug(f"Error code: 2 - {ERRORS[2]}")
            CONTROLS["env"].log.error("Не удалось открыть базу данных.")
            CONTROLS["env"].log.debug(f"Raw exception data: {ex.__str__()}")

            return 2
            
        CONTROLS["env"].log.debug("Чтение базы данных...")
        try:
            with open(file=f"{os.getcwd()}\\sql\\get_datatables_from_db.sql", mode='r', encoding="utf-8") as query:
                query.seek(0)
                CONTROLS["env"].log.debug("Запрос к базе...")
                result = CONTROLS["db_bus"].execute_custom_sql(cmd=query.read(), is_select=True)
                CONTROLS["env"].log.debug("Запрос выполнен.")
                CONTROLS["env"].log.debug("Анализ структуры базы...")
                if result is None:
                    CONTROLS["env"].log.debug(f"Error code: 3 - {ERRORS[3]}")
                    CONTROLS["env"].log.error("Неправильная стуктура базы данных - запрос пуст.")
                    return 3
                if isinstance(result, list) is False:
                    CONTROLS["env"].log.debug(f"Error code: 3 - {ERRORS[3]}")
                    CONTROLS["env"].log.error("Неправильная стуктура базы данных - запрос пуст.")
                    return 3
                if len(result) == 0:
                    CONTROLS["env"].log.debug(f"Error code: 3 - {ERRORS[3]}")
                    CONTROLS["env"].log.error("Неправильная стуктура базы данных - неверное количество таблиц.")
                    return 3
                for line in result:
                    if line[0] not in LOCAL_VARS["db_tables"].keys():
                        CONTROLS["env"].log.debug(f"Error code: 3 - {ERRORS[3]}")
                        CONTROLS["env"].log.error(f"Неправильная стуктура базы данных - таблица {line[0]} отсутствует в схеме.")
                        return 3
                CONTROLS["env"].log.debug("Таблицы базы соответствуют схеме.")
            
            with open(file=f"{os.getcwd()}\\sql\\get_columns_from_table_template.sql", mode='r', encoding="utf-8") as query:
                for table in LOCAL_VARS["db_tables"].keys():
                    query.seek(0)
                    CONTROLS["env"].log.debug("Запрос к базе...")
                    result = CONTROLS["db_bus"].execute_custom_sql(cmd=query_read, is_select=False, args=[table])
                    CONTROLS["env"].log.debug("Запрос выполнен.")
                    CONTROLS["env"].log.debug(f"Анализ структуры таблицы {table}...")
                    if result is None:
                        CONTROLS["env"].log.debug(f"Error code: 3 - {ERRORS[3]}")
                        CONTROLS["env"].log.error("Неправильная стуктура базы данных - запрос пуст.")
                        return 3
                    if isinstance(result, list) is False:
                        CONTROLS["env"].log.debug(f"Error code: 3 - {ERRORS[3]}")
                        CONTROLS["env"].log.error("Неправильная стуктура базы данных - запрос пуст.")
                        return 3
                    if len(result) == 0:
                        CONTROLS["env"].log.debug(f"Error code: 3 - {ERRORS[3]}")
                        CONTROLS["env"].log.error("Неправильная стуктура базы данных - неверное количество атрибутов.")
                        return 3
                    for line in result:
                        if line[1] not in LOCAL_VARS["db_tables"][table]:
                            CONTROLS["env"].log.debug(f"Error code: 3 - {ERRORS[3]}")
                            CONTROLS["env"].log.error("Неправильная стуктура базы данных - атрибуты не совпадают со схемой.")
                            return 3
                    CONTROLS["env"].log.debug(f"Таблица {table} структурирована верно.")
            CONTROLS["env"].log.debug(f"Все таблицы структурированы верно.")
                        
        except Exception as ex:
            CONTROLS["env"].log.debug(f"Error code: 3 - {ERRORS[3]}")
            CONTROLS["env"].log.error("Неправильная стуктура базы данных.")
            CONTROLS["env"].log.debug(f"Raw exception data: {ex.__str__()}")

            return 3
        CONTROLS["env"].log.info("База данных загружена.")
        
        return 0
        

    def redirect_except_hook(self, cls, exception, traceback) -> None:
        """
        DESCR:
        REQUIRE:
        RETURN: 
        """
        sys.__excepthook__(cls, exception, traceback)

        return None

    def save_config_to_file(self) -> int:
        """
        DESCR:
        REQUIRE:
        RETURN: 
        """
        CONTROLS["env"].log.debug("Сохранение значений конфигурации в файл...")
        try:
            with open(file=LOCAL_VARS["conf_path"], mode='w', encoding='utf-8') as dst:
                for key, value in CONFIG.items():
                    dst.write(f"{key}={value}\n")
                dst.flush()  
        except Exception as ex:
            CONTROLS["env"].log.debug(f"Error code: 2 - {ERRORS[2]}")
            CONTROLS["env"].log.error("Не удалось сохранить значения конфигурации в файл.")
            CONTROLS["env"].log.debug(f"Raw exception data: {ex.__str__()}")

            return 2

        CONTROLS["env"].log.info("Конфигурация успешно записана в файл.")
        return 0
