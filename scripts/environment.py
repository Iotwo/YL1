import os
import sys
import logging
import datetime
import csv
from sqlite3 import connect, Connection
from scripts.variables import *


class Environment(object):
    """
    DESCR: this class describes interaction between the main program and files in OS
    REQUIRE:
    RETURN: 
    """

    def __new__(cls, *args, **kwargs) -> object:
        instance = super().__new__(cls)
        instance.log = None
        
        return instance

    def __init__(self) -> None:

        return None


    def call_db_ddl(self, ddl_path: str) -> int:
        """
        DESCR:
        REQUIRE:
        RETURN: 
        """
        CONTROLS["env"].log.info("Поиск DDL-скрипта базы данных..")
        CONTROLS["env"].log.debug(f"path={ddl_path}")
        if os.path.isfile(ddl_path) is False:
            CONTROLS["env"].log.debug(f"Error code: 2 - {ERRORS[2]}")
            CONTROLS["env"].log.error("Не удалось открыть DDL-скрипт базы данных.")
        CONTROLS["env"].log.info("DDL-скрипт обнаружен.")
        CONTROLS["env"].log.info("Исполнение DDL-скрипта базы данных..")
        try:
            with open(file=ddl_path, mode='r', encoding='utf-8') as buffer:
                CONTROLS["db_bus"].execute_db_ddl(buffer.readlines())
        except Exception as ex:
            CONTROLS["env"].log.debug(f"Error code: 3 - {ERRORS[3]}")
            CONTROLS["env"].log.error("Неправильная стуктура DDL-скрипта.")
            CONTROLS["env"].log.debug(f"Raw exception data: {ex.__str__()}")

            return 3
        
        CONTROLS["env"].log.info("DLL-скрипт выполнен.")
        
        return 0

    def call_db_purge(self, sql_path: str) -> int:
        """
        DESCR:
        REQUIRE:
        RETURN: 
        """

        CONTROLS["env"].log.info("Поиск SQL-скрипта..")
        CONTROLS["env"].log.debug(f"path={sql_path}")
        if os.path.isfile(sql_path) is False:
            CONTROLS["env"].log.debug(f"Error code: 2 - {ERRORS[2]}")
            CONTROLS["env"].log.error("Не удалось открыть SQL-скрипт.")
            return 2
        CONTROLS["env"].log.info("SQL-скрипт обнаружен.")
        CONTROLS["env"].log.info("Исполнение SQL-скрипта базы данных..")
        try:
            with open(file=sql_path, mode='r', encoding='utf-8') as buffer:
                CONTROLS["db_bus"].purge_db(buffer.read())
        except Exception as ex:
            CONTROLS["env"].log.debug(f"Error code: 3 - {ERRORS[3]}")
            CONTROLS["env"].log.error("Неправильная стуктура SQL-скрипта.")
            CONTROLS["env"].log.debug(f"Raw exception data: {ex.__str__()}")

            return 3
        
        CONTROLS["env"].log.info("SQL-скрипт выполнен.")
        
        return 0

    def call_delete_rec_command(self, sql_path: str, table_name: str, del_marker: str, del_val: str) -> int:
        
        CONTROLS["env"].log.info("Поиск SQL-скрипта..")
        CONTROLS["env"].log.debug(f"path={sql_path}")
        if os.path.isfile(sql_path) is False:
            CONTROLS["env"].log.debug(f"Error code: 2 - {ERRORS[2]}")
            CONTROLS["env"].log.error("Не удалось открыть SQL-скрипт.")
            return 2
        CONTROLS["env"].log.info("SQL-скрипт обнаружен.")
        CONTROLS["env"].log.info("Исполнение SQL-скрипта базы данных..")
        try:
            with open(file=sql_path, mode='r', encoding='utf-8') as buffer:
                CONTROLS["db_bus"].delete_record_from_table(buffer.read(), table_name, del_marker, del_val)
        except Exception as ex:
            CONTROLS["env"].log.debug(f"Error code: 3 - {ERRORS[3]}")
            CONTROLS["env"].log.error("Неправильная стуктура SQL-скрипта.")
            CONTROLS["env"].log.debug(f"Raw exception data: {ex.__str__()}")

            return 3
        
        CONTROLS["env"].log.info("SQL-скрипт выполнен.")
        
        return 0
    
    def call_insert_new_rec(self, sql_path: str, table_name: str, values: list) -> int:
        
        CONTROLS["env"].log.info("Поиск SQL-скрипта..")
        CONTROLS["env"].log.debug(f"path={sql_path}")
        if os.path.isfile(sql_path) is False:
            CONTROLS["env"].log.debug(f"Error code: 2 - {ERRORS[2]}")
            CONTROLS["env"].log.error("Не удалось открыть SQL-скрипт.")
            return 2
        CONTROLS["env"].log.info("SQL-скрипт обнаружен.")
        CONTROLS["env"].log.info("Исполнение SQL-скрипта базы данных..")
        try:
            with open(file=sql_path, mode='r', encoding='utf-8') as buffer:
                CONTROLS["db_bus"].insert_data_to_table(buffer.read(), table_name, values)
        except Exception as ex:
            CONTROLS["env"].log.debug(f"Error code: 3 - {ERRORS[3]}")
            CONTROLS["env"].log.error("Неправильная стуктура SQL-скрипта.")
            CONTROLS["env"].log.debug(f"Raw exception data: {ex.__str__()}")

            return 3
        
        CONTROLS["env"].log.info("SQL-скрипт выполнен.")
        
        return 0

    def call_select_last_x_records(self, sql_path: str) -> object:
        """
        """
        result = None
        CONTROLS["env"].log.info("Поиск SQL-скрипта..")
        CONTROLS["env"].log.debug(f"path={sql_path}")
        if os.path.isfile(sql_path) is False:
            CONTROLS["env"].log.debug(f"Error code: 2 - {ERRORS[2]}")
            CONTROLS["env"].log.error("Не удалось открыть SQL-скрипт.")
            return None
        CONTROLS["env"].log.info("SQL-скрипт обнаружен.")
        CONTROLS["env"].log.info("Исполнение SQL-скрипта базы данных..")
        try:
            with open(file=sql_path, mode='r', encoding='utf-8') as buffer:
                result = CONTROLS["db_bus"].execute_custom_sql(buffer.read(), True)
        except Exception as ex:
            CONTROLS["env"].log.debug(f"Error code: 3 - {ERRORS[3]}")
            CONTROLS["env"].log.error("Неправильная стуктура SQL-скрипта.")
            CONTROLS["env"].log.debug(f"Raw exception data: {ex.__str__()}")

            return None
        
        CONTROLS["env"].log.info("SQL-скрипт выполнен.")
        
        return result

    def call_select_cats_of_op(self, sql_path:str, op_type: str) -> object:

        result = None
        CONTROLS["env"].log.info("Поиск SQL-скрипта..")
        CONTROLS["env"].log.debug(f"path={sql_path}")
        if os.path.isfile(sql_path) is False:
            CONTROLS["env"].log.debug(f"Error code: 2 - {ERRORS[2]}")
            CONTROLS["env"].log.error("Не удалось открыть SQL-скрипт.")
            return None
        CONTROLS["env"].log.info("SQL-скрипт обнаружен.")
        CONTROLS["env"].log.info("Исполнение SQL-скрипта базы данных..")
        try:
            with open(file=sql_path, mode='r', encoding='utf-8') as buffer:
                result = CONTROLS["db_bus"].select_all_from_categories(buffer.read(), op_type)
        except Exception as ex:
            CONTROLS["env"].log.debug(f"Error code: 3 - {ERRORS[3]}")
            CONTROLS["env"].log.error("Неправильная стуктура SQL-скрипта.")
            CONTROLS["env"].log.debug(f"Raw exception data: {ex.__str__()}")

            return None
        
        return result

    def call_sql_select_cmd(self, sql_path: str) -> object:
        """
        """
        result = None
        CONTROLS["env"].log.info("Поиск SQL-скрипта..")
        CONTROLS["env"].log.debug(f"path={sql_path}")
        if os.path.isfile(sql_path) is False:
            CONTROLS["env"].log.debug(f"Error code: 2 - {ERRORS[2]}")
            CONTROLS["env"].log.error("Не удалось открыть SQL-скрипт.")
            return None
        CONTROLS["env"].log.info("SQL-скрипт обнаружен.")
        CONTROLS["env"].log.info("Исполнение SQL-скрипта базы данных..")
        try:
            with open(file=sql_path, mode='r', encoding='utf-8') as buffer:
                result = CONTROLS["db_bus"].execute_custom_sql(buffer.read(), True)
        except Exception as ex:
            CONTROLS["env"].log.debug(f"Error code: 3 - {ERRORS[3]}")
            CONTROLS["env"].log.error("Неправильная стуктура SQL-скрипта.")
            CONTROLS["env"].log.debug(f"Raw exception data: {ex.__str__()}")

            return None
        
        CONTROLS["env"].log.info("SQL-скрипт выполнен.")
        
        return result

    def call_update_record_in_table(self, sql_path: str, table_name:str, upd_params: dict, key_name: str, key_val: str) -> int:
        """
        """
        
        result = None
        CONTROLS["env"].log.info("Поиск SQL-скрипта..")
        CONTROLS["env"].log.debug(f"path={sql_path}")
        if os.path.isfile(sql_path) is False:
            CONTROLS["env"].log.debug(f"Error code: 2 - {ERRORS[2]}")
            CONTROLS["env"].log.error("Не удалось открыть SQL-скрипт.")
            return 2
        CONTROLS["env"].log.info("SQL-скрипт обнаружен.")
        CONTROLS["env"].log.info("Исполнение SQL-скрипта базы данных..")
        try:
            with open(file=sql_path, mode='r', encoding='utf-8') as buffer:
                if table_name == "Actions_log":
                    result = CONTROLS["db_bus"].update_item_data_on_actionslog(buffer.read(), table_name, upd_params, key_name, key_val)
                elif table_name == "Categories":
                    result = CONTROLS["db_bus"].update_item_data_on_categories(buffer.read(), table_name, upd_params, key_name, key_val)
                elif table_name == "Operations":
                    result = CONTROLS["db_bus"].update_item_data_on_operations(buffer.read(), table_name, upd_params, key_name, key_val)
                    
        except Exception as ex:
            CONTROLS["env"].log.debug(f"Error code: 3 - {ERRORS[3]}")
            CONTROLS["env"].log.error("Неправильная стуктура SQL-скрипта.")
            CONTROLS["env"].log.debug(f"Raw exception data: {ex.__str__()}")

            return 3
        
        CONTROLS["env"].log.info("SQL-скрипт выполнен.")
        
        return result
    
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

    def create_report_file(self, r_type: str, r_data: list) -> None:
        """
        """
        result = None
        CONTROLS["env"].log.info("Формирование отчёта..")
        try:
            r_name = f"{LOCAL_VARS['report_dir']}Y1_{datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')}_report."
            if r_type == "csv":
                r_name += "csv"
                CONTROLS["env"].log.debug(f"Отчёт в формате CSV.")
                with open(file=r_name, mode='w', encoding="utf-8-sig", newline='') as repf:
                    csv_type= csv.writer(repf, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
                    for row in r_data:
                        csv_type.writerow(row)
                    repf.flush()
            elif r_type == "txt":
                r_name += "txt"
                with open(file=r_name, mode='w', encoding="utf-8-sig") as repf:
                    repf.write('=' * 70 + '\n')
                    repf.write("Расходы за сегодня:"+ '\n')
                    repf.write('=' * 70 + '\n')
                    repf.write("Категория".ljust(50) + "Значение".ljust(16) + '\n')
                    for row in r_data:
                        if "Расход" in row:
                            repf.write(f"{str(row[1]).ljust(50)}{str(row[2]).ljust(2)}" + '\n')
                    repf.write('\n')
                    repf.write('=' * 70 + '\n')
                    repf.write("Доходы за сегодня:" + '\n')
                    repf.write('=' * 70 + '\n')
                    repf.write("Категория".ljust(50) + "Значение".ljust(16) + '\n')
                    for row in r_data:
                        if "Доход" in row:
                            repf.write(f"{str(row[1]).ljust(50)}{str(row[2]).ljust(2)}" + '\n')
                    rep.flush()
                CONTROLS["env"].log.debug(f"Отчёт {r_name} сформирован.")
            else:
                CONTROLS["env"].log.debug(f"Error code: 5 - {ERRORS[5]}")
                CONTROLS["env"].log.error("Передано неверное расширение файла отчёта!")
                return 5 
        except Exception as ex:
            CONTROLS["env"].log.debug(f"Error code: 2 - {ERRORS[2]}")
            CONTROLS["env"].log.error("Не удалось создать файл отчёта.")
            CONTROLS["env"].log.debug(f"Raw exception data: {ex.__str__()}")
            return 2
        
        return 0
    
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
        with open(file=f"{LOCAL_VARS['log_dir']}Y1_{datetime.datetime.now().date()}_app.log", mode='a', encoding="utf-8") as f:
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
                CONTROLS["env"].log.debug(f"file={os.getcwd()}\\sql\\get_datatables_from_db.sql")
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
                CONTROLS["env"].log.debug(f"file={os.getcwd()}\\sql\\get_columns_from_table_template.sql")
                for table in LOCAL_VARS["db_tables"].keys():
                    query.seek(0)
                    CONTROLS["env"].log.debug("Запрос к базе...")
                    result = CONTROLS["db_bus"].execute_pragma_statement(query.read(), table,)
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
                        if line not in LOCAL_VARS["db_tables"][table]:
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
            CONTROLS["env"].log.debug(f"Error code: 255 - {ERRORS[255]}")
            CONTROLS["env"].log.error("Не удалось сохранить значения конфигурации в файл.")
            CONTROLS["env"].log.debug(f"Raw exception data: {ex.__str__()}")

            return 2

        CONTROLS["env"].log.info("Конфигурация успешно записана в файл.")
        return 0
