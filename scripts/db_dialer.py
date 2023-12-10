from datetime import datetime
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

    def delete_record_from_table(self, cmd: str, table: str, marker: str, mark_val: str) -> None:
        result = None
        self.sql_cmd = cmd.format(table_name=table, mark=marker, val=mark_val)
        CONTROLS["env"].log.debug("Готовится SQL-запрос...")
        CONTROLS["env"].log.debug(f"SQL:{self.sql_cmd}")
        result = self.data_cursor.execute(self.sql_cmd)
        CONTROLS["env"].log.debug(f"{result}")
        self.db_connector.commit()
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

    def execute_pragma_statement(self, sql_pragma: str, pragma_table: str) -> list:

        self.sql_cmd = sql_pragma.format(table=pragma_table)
        CONTROLS["env"].log.debug("Готовится SQL-запрос...")
        CONTROLS["env"].log.debug(f"SQL:{self.sql_cmd}")
        result = self.data_cursor.execute(self.sql_cmd).fetchall()
        result = [arg[1] for arg in result]
        CONTROLS["env"].log.debug(f"{self.data_cursor.description}")
        CONTROLS["env"].log.debug(f"Запрос вернул {len(result) if result is not None else result} кортежей.")
        
        return result
    
    def insert_multiple_data_to_actions_log(self, rows_coll: list, cmd: str) -> None:
        """
        DESCR: 
        REQ: sqlite3.Cursor, sqlite3.Connection
        ARGS:
            -: name of the table
        """
        result = None
        self.sql_cmd = cmd
        CONTROLS["env"].log.debug("Готовится SQL-запрос...")
        CONTROLS["env"].log.debug(f"SQL:{self.sql_cmd}")
        self.data_cursor.executemany(self.sql_cmd, rows_coll)
        self.db_connector.commit()
        CONTROLS["env"].log.debug(f"{self.data_cursor.description}")
        
        return None

    def insert_data_to_table(self, cmd: str, table: str, params: list) -> None:

        result = None

        self.sql_cmd = cmd
        CONTROLS["env"].log.debug("Готовится SQL-запрос...")
        CONTROLS["env"].log.debug(f"SQL:{self.sql_cmd}")
        self.data_cursor.execute(self.sql_cmd, params)
        self.db_connector.commit()
        CONTROLS["env"].log.debug(f"{self.data_cursor.description}")
        
        return result

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

    def select_all_from_categories(self, get_categories_for_op_script: str, operation: str) -> list:
        result = None
        self.sql_cmd = get_categories_for_op_script
        CONTROLS["env"].log.debug("Готовится SQL-запрос...")
        CONTROLS["env"].log.debug(f"SQL:{self.sql_cmd}")
        self.data_cursor.execute(self.sql_cmd, (operation,))
        result = self.data_cursor.fetchall()
        CONTROLS["env"].log.debug(f"{self.data_cursor.description}")
        CONTROLS["env"].log.debug(f"Запрос вернул {len(result) if result is not None else result} кортежей.")
        
        return result

    def select_all_from_optypes(self) -> list:
        result = None
        self.sql_cmd = ""
        CONTROLS["env"].log.debug("Готовится SQL-запрос...")
        CONTROLS["env"].log.debug(f"SQL:{self.sql_cmd}")
        self.data_cursor.execute(self.sql_cmd, columns)
        result = self.data_cursor.fetchall()
        CONTROLS["env"].log.debug(f"{self.data_cursor.description}")
        CONTROLS["env"].log.debug(f"Запрос вернул {len(result) if result is not None else result} кортежей.")
        
        return result

    def select_all_data_from_table(self, table: str, columns: list) -> list:
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

    def select_last_X_records_from_action(self) -> list:
        result = None
        self.sql_cmd = ""
        CONTROLS["env"].log.debug("Готовится SQL-запрос...")
        CONTROLS["env"].log.debug(f"SQL:{self.sql_cmd}")
        self.data_cursor.execute(self.sql_cmd, columns)
        result = self.data_cursor.fetchall()
        CONTROLS["env"].log.debug(f"{self.data_cursor.description}")
        CONTROLS["env"].log.debug(f"Запрос вернул {len(result) if result is not None else result} кортежей.")
        
        return result
    
    def update_item_data_on_actionslog(self, cmd: str, table: str, params: dict, marker_name: str, marker_val: str) -> None:
        """
        DESCR: execute sql-update command on given data-table
        REQ: sqlite3.Cursor, sqlite3.Connection
        ARGS:
            -cmd: command text template
            -table: name of the table
            -params: dict of pairs param-value
            -item_name: exact line marker for concrete update
            -item_marker:  exact line marker for concrete update
        """
        #params_vals=", ".join([table + '.?=?' for _ in params.keys()]),
        """
        self.sql_cmd = cmd.format(rid=params.get("id"),
                                  dt=datetime.strptime(params.get("action_datetime"), "%Y-%m-%d %H:%M:%S"),
                                  op=params.get("optype"),
                                  cat=params.get("category"),
                                  amt=params.get("amount"),
                                  cmt=params.get("comment"),
                                  mark_name=marker_name,
                                  mark_val=marker_val)
        """
        self.sql_cmd = cmd.format(mark_name=marker_name, mark_val=marker_val)
        CONTROLS["env"].log.debug("Готовится SQL-запрос...")
        CONTROLS["env"].log.debug(f"SQL:{self.sql_cmd}")
        #self.data_cursor.execute(self.sql_cmd, list(params.keys()) + list(params.values()))
        params = [params.get("id"), datetime.strptime(params.get("action_datetime"), "%Y-%m-%d %H:%M:%S"),
                  params.get("optype"), params.get("category"),
                  params.get("amount"), params.get("comment"),]
        self.data_cursor.execute(self.sql_cmd, params)
        self.db_connector.commit()
        CONTROLS["env"].log.debug(f"{self.data_cursor.description}")
        
        return None

    def update_item_data_on_categories(self, cmd: str, table: str, params: dict, marker_name: str, marker_val: str) -> None:
        """
        DESCR: execute sql-update command on given data-table
        REQ: sqlite3.Cursor, sqlite3.Connection
        ARGS:
            -cmd: command text template
            -table: name of the table
            -params: dict of pairs param-value
            -item_name: exact line marker for concrete update
            -item_marker:  exact line marker for concrete update
        """
        #params_vals=", ".join([table + '.?=?' for _ in params.keys()]),
        self.sql_cmd = cmd.format(table=table,
                                  params_vals=", ".join([table + '.' + key + '=' + val for (key,val) in params.items()]),
                                  mark_name=marker_name,
                                  mark_val=marker_val)
        CONTROLS["env"].log.debug("Готовится SQL-запрос...")
        CONTROLS["env"].log.debug(f"SQL:{self.sql_cmd}")
        #self.data_cursor.execute(self.sql_cmd, list(params.keys()) + list(params.values()))
        self.data_cursor.execute(self.sql_cmd)
        self.db_connector.commit()
        CONTROLS["env"].log.debug(f"{self.data_cursor.description}")
        
        return None

    def update_item_data_on_operations(self, cmd: str, table: str, params: dict, marker_name: str, marker_val: str) -> None:
        """
        DESCR: execute sql-update command on given data-table
        REQ: sqlite3.Cursor, sqlite3.Connection
        ARGS:
            -cmd: command text template
            -table: name of the table
            -params: dict of pairs param-value
            -item_name: exact line marker for concrete update
            -item_marker:  exact line marker for concrete update
        """
        #params_vals=", ".join([table + '.?=?' for _ in params.keys()]),
        self.sql_cmd = cmd.format(table=table,
                                  params_vals=", ".join([table + '.' + key + '=' + val for (key,val) in params.items()]),
                                  mark_name=marker_name,
                                  mark_val=marker_val)
        CONTROLS["env"].log.debug("Готовится SQL-запрос...")
        CONTROLS["env"].log.debug(f"SQL:{self.sql_cmd}")
        #self.data_cursor.execute(self.sql_cmd, list(params.keys()) + list(params.values()))
        self.data_cursor.execute(self.sql_cmd)
        self.db_connector.commit()
        CONTROLS["env"].log.debug(f"{self.data_cursor.description}")
        
        return None

     
