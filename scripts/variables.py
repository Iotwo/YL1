#############################################
# File with constants and control parameters.
#############################################

LOCAL_VARS = {
    "conf_path": "./config.cfg",
    "help_path": "./help/help.html",
    "log_dir": "./logs/",
    "report_dir": "./reports/",
    "db_tables": {
        "Actions_log": ["id", "action_datetime", "optype", "category", "amount", "comment"],
        "Categories": ["cat_name", "optype"],
        "Operations": ["op_name"],
        },
    "RU_db_tables": {
        "Actions_log": ["№", "Когда", "Тип", "Категория", "Сумма", "Заметка",],
        "Categories": [],
        "Operations": [],
        },
    "table_states": ["view", "edit"],
    "RU_table_states": ["Просмотр", "Редактирование"],
    "last_err_code": 0,
}

CONFIG = {
    "db_path": "",
    "def_btn1": 0,
    "def_btn2": 0,
    "def_btn3": 0,
    "def_btn4": 0,
    "def_btn5": 0,
    "def_btn6": 0,
}

CONTROLS = {
    "env": None,
    "db_bus": None,
}

ERRORS = {
    0: "OK",
    1: "File not found.",
    2: "Not enough permissions in file system.",
    3: "Inconsistent configuration.",
    4: "Incorrect config value.",
    5: "Incorrect report file extenson",
    255: "General error."
}
