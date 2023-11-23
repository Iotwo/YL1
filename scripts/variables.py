LOCAL_VARS = {
    "conf_path": "./config.cfg",
    "db_tables": {
        "Actions_log": ["id", "action_datetime", "optype", "category", "amount", "comment"],
        "Categories": ["cat_name"],
        "Operations": ["op_name"],
        },
    "RU_db_tables": {
        "Actions_log": ["№", "Когда", "Тип", "Категория", "Сумма", "Заметка",],
        "Categories": [],
        "Operations": [],
        },
    "last_err_code": 0,
}

CONFIG = {
    "db_path": "",
    "def_btn1": 0,
    "def_btn2": 0,
    "def_btn3": 0,
    "def_btn4": 0,
    "def_btn5": 0,
    "def_btn6": 0,}

CONTROLS = {
    "env": None,
    "db_bus": None,
}

ERRORS = {
    0: "OK",
    1: "File not found.",
    2: "Not enough permissions in file system.",
    3: "Inconsistent configuration.",
}
