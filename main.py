import sys
import os
import logging
import datetime
from PyQt5 import QtCore, QtWidgets 
from forms.main_form_ui import Ui_MainForm
from forms.main_form_form import MainFormIf
from forms.settings_form_ui import Ui_SettingsForm
from forms.settings_form_form import SettingsFormIf
from scripts.environment import Environment
from scripts.db_dialer import DBDialer
from scripts.variables import CONTROLS, LOCAL_VARS, CONFIG, ERRORS


if __name__ == "__main__":
    CONTROLS["env"] = Environment()
    CONTROLS["env"].create_base_dirs()
    CONTROLS["env"].initiate_log_file()
    CONTROLS["env"].log.info("===========================================")
    CONTROLS["env"].log.info("Запись начата.")
    CONTROLS["env"].log.info("===========================================")
    CONTROLS["env"].log.debug(f"Перечисление кодов ошибок:")
    CONTROLS["env"].log.debug(f"{';'.join(['='.join((str(key), str(val),)) for key, val in ERRORS.items()])}")
    
    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
        CONTROLS["env"].log.debug("Включено масштабирование высокого разрешения.")

    if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
        CONTROLS["env"].log.debug("Используются пиксельные карты высокого разрешения.")

    CONTROLS["db_bus"] = DBDialer()
    app = QtWidgets.QApplication(sys.argv)
    CONTROLS["env"].log.info("Инициализирован экзеспляр приложения.")

    sys.excepthook = CONTROLS["env"].redirect_except_hook
    CONTROLS["env"].log.debug("Настроен перехват внутренних событий PyQt.")
    
    CONTROLS["env"].log.debug("Поиск файла конфигурации...")
    if CONTROLS["env"].check_config_file_exists() != 0:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setText("Файл конфигурации не обнаружен!\nБудут использованы значения по умолчанию.")
        msg.setWindowTitle("Информация о запуске.")
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        retval = msg.exec()
        CONTROLS["env"].initiate_default_config()
        CONTROLS["env"].save_config_to_file()
    else:
        CONTROLS["env"].load_config_from_file()

    CONTROLS["env"].log.debug("Поиск файла базы данных...")
    if CONTROLS["env"].check_db_file_exists() != 0:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setText("Файл базы данных не обнаружен!\nБаза данных будет сконструирована.")
        msg.setWindowTitle("Информация о запуске.")
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        retval = msg.exec()
        CONTROLS["env"].create_db_file()
        CONTROLS["db_bus"].execute_db_ddl(open(file=f"{os.getcwd()}\\sql\\ddl.sql", mode='r', encoding="utf-8").readlines())
    else:
        LOCAL_VARS["last_err_code"] = CONTROLS["env"].open_db_file()
        if LOCAL_VARS["last_err_code"] != 0:
            CONTROLS["db_bus"].purge_db(open(file=f"{os.getcwd()}\\sql\\get_datatables_from_db.sql", mode='r', encoding="utf-8").read())
            CONTROLS["db_bus"].execute_db_ddl(open(file=f"{os.getcwd()}\\sql\\ddl.sql", mode='r', encoding="utf-8").readlines())
    
    CONTROLS["env"].log.debug("Инициализация главной формы приложения...")
    m_form = MainFormIf()
    m_form.show()
    CONTROLS["env"].log.info("Приложение готово к работе.")
    LOCAL_VARS["last_err_code"] = app.exec()
    CONTROLS["env"].log.debug("Значения внутренних переменных по итогу программы:")
    CONTROLS["env"].log.debug(f"LOCAL_VARS")
    CONTROLS["env"].log.debug(f"{';'.join(['='.join((str(key), str(val),)) for key, val in LOCAL_VARS.items()])}")
    CONTROLS["env"].log.debug(f"CONFIG")
    CONTROLS["env"].log.debug(f"{';'.join(['='.join((str(key), str(val),)) for key, val in CONFIG.items()])}")
    CONTROLS["env"].log.debug(f"CONTROLS")
    CONTROLS["env"].log.debug(f"{';'.join(['='.join((str(key), str(val),)) for key, val in CONTROLS.items()])}")
    CONTROLS["env"].log.info(f"Код выхода: {LOCAL_VARS['last_err_code']}")

    del(CONTROLS["db_bus"])
    logging.shutdown()
    sys.exit(LOCAL_VARS['last_err_code'])
