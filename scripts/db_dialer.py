import sqlite3
from sqlite3 import connect, Connection
from scripts.variables import *


class DBDialer(object):
    """
    DESCR: Class for local database manipulation
    REQ: sqlite3
    """

    def __del__(self) -> None:
        self.data_cursor.close()
        self.db_connector.close()

        return None
    
    def __init__(self,) -> None:
        """
        DESCR: initialize new instance
        REQ: sqlite3.Connection, sqlite3.Cursor
        """
        
        return None

    def __new__(cls, *args, **kwargs) -> object:
        """
        DESCR: create new instance of the class, initialize vals with defaults
        RETURN: new instance of DBDialer
        """
        instance = super().__new__(cls)
        instance.db_connector = None
        instance.data_cursor = None
        instance.sql_cmd = ""
        instance.db_responce = []
        
        return instance

    def create_database(self) -> None:
        self.db_connector = connect(database=CONFIG["db_path"], uri=False)
        self.data_cursor = self.db_connector.cursor()
        return None

    
    def execute_custom_sql(self, cmd: str, is_select: bool=False, *args) -> object:
        """
        DESCR: execute custom sql-command string
        """
        result = None
        self.sql_cmd = cmd
        CONTROLS["env"].log.debug("Готовится SQL-запрос...")
        CONTROLS["env"].log.debug(f"SQL:{self.sql_cmd}")
        if is_select is False:
            self.data_cursor.execute(self.sql_cmd, args)
            self.db_connector.commit()
        else:
            result = self.data_cursor.execute(self.sql_cmd).fetchall()
        CONTROLS["env"].log.debug(f"{self.data_cursor.description}")
        CONTROLS["env"].log.debug(f"Запрос вернул {len(result) if result is not None else result} кортежей.")
        return result

    def execute_db_ddl(self, ddl_script: str) -> None:
        """
        DESCR:
        """
        for line in ddl_script:
            self.sql_cmd = line
            CONTROLS["env"].log.debug("Готовится SQL-запрос...")
            CONTROLS["env"].log.debug(f"SQL:{self.sql_cmd}")
            self.data_cursor.execute(self.sql_cmd)
            self.db_connector.commit()
            CONTROLS["env"].log.debug(f"{self.data_cursor.description}")

        return None

    def insert_data_to_table(self, table: str, params: dict) -> None:
        """
        DESCR: execute sql-insert command on given data-table
        REQ: sqlite3.Cursor, sqlite3.Connection
        ARGS:
            -table: name of the table
            -params: dict of pairs param-value
        """
        result = None
        self.sql_cmd = f"INSERT INTO {table} ({', '.join(['?' for key in params.keys()])}) " +\
                       f"VALUES ({', '.join(['?' for value in params.values()])});"
        CONTROLS["env"].log.debug("Готовится SQL-запрос...")
        CONTROLS["env"].log.debug(f"SQL:{self.sql_cmd}")
        self.data_cursor.execute(self.sql_cmd, list(params.keys()) + list(params.values()))
        self.db_connector.commit()
        CONTROLS["env"].log.debug(f"{self.data_cursor.description}")
        return None

    def open_db_file(self) -> None:
        self.db_connector = connect(database="file:" + CONFIG["db_path"] + "?mode=rw", uri=True)
        self.data_cursor = self.db_connector.cursor()

        return None

    def purge_db(self, get_all_tables_script: str) -> None:
        """
        """
        self.sql_cmd = get_all_tables_script
        CONTROLS["env"].log.debug("Готовится SQL-запрос...")
        CONTROLS["env"].log.debug(f"SQL:{self.sql_cmd}")
        result = self.data_cursor.execute(self.sql_cmd).fetchall()
        CONTROLS["env"].log.debug(f"{self.data_cursor.description}")
        CONTROLS["env"].log.debug(f"Запрос вернул {len(result) if result is not None else result} кортежей.")
        for table in result:
            self.sql_cmd = f"DROP TABLE {table[0]};"
            CONTROLS["env"].log.debug("Готовится SQL-запрос...")
            CONTROLS["env"].log.debug(f"SQL:{self.sql_cmd}")
            self.data_cursor.execute(self.sql_cmd)
            self.db_connector.commit()
            CONTROLS["env"].log.debug(f"{self.data_cursor.description}")
        return None

    def select_data_from_table(self, table: str, columns: list) -> list:
        """
        DESCR: execute sql-select command on given data-table
        REQ: sqlite3.Cursor
        ARGS:
            -table: name of the table
            -columns: list of attributes
        RETURN: list of tuples from queried table
        """
        result = None
        self.sql_cmd = "SELECT " + f"{' '.join([table + '.?' for val in columns])} FROM {table};"
        CONTROLS["env"].log.debug("Готовится SQL-запрос...")
        CONTROLS["env"].log.debug(f"SQL:{self.sql_cmd}")
        self.data_cursor.execute(self.sql_cmd, columns)
        result = self.data_cursor.fetchall()
        CONTROLS["env"].log.debug(f"{self.data_cursor.description}")
        CONTROLS["env"].log.debug(f"Запрос вернул {len(result) if result is not None else result} кортежей.")
        
        return result

    def update_item_data_on_table(self, table: str, params: dict, item_name: str, item_marker: str) -> None:
        """
        DESCR: execute sql-update command on given data-table
        REQ: sqlite3.Cursor, sqlite3.Connection
        ARGS:
            -table: name of the table
            -params: dict of pairs param-value
            -item_name: exact line marker for concrete update
            -item_marker:  exact line marker for concrete update
        """
        self.sql_cmd = f"UPDATE {table} SET {[table + '.?=?' for _ in params.keys()]}" +\
                       " WHERE {item_name}={item_marker} ;"
        CONTROLS["env"].log.debug("Готовится SQL-запрос...")
        CONTROLS["env"].log.debug(f"SQL:{self.sql_cmd}")
        self.data_cursor.execute(sql=self.sql_cmd, parameters=list(params.keys()) + list(params.values()))
        self.db_connector.commit()
        CONTROLS["env"].log.debug(f"{self.data_cursor.description}")
        
        return None

     
