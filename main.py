##################################################
# This program is project for LMS
# Yandex Lyceum to demonstrate interaction
# between Python and SQLite DB via PyQt interface
##################################################

import sys  # cannot be imported any other way due to deep problem of exception hooks
from os import getcwd
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox
from forms.main_form_ui import Ui_MainForm
from forms.main_form_form import MainFormIf
from scripts.environment import Environment
from scripts.db_dialer import DBDialer
from scripts.variables import CONTROLS, LOCAL_VARS, CONFIG, ERRORS


if __name__ == "__main__":
    # Declare and configure inner logger.
    CONTROLS["env"] = Environment()
    CONTROLS["env"].create_base_dirs()
    CONTROLS["env"].initiate_log_file()
    CONTROLS["env"].log.info("===========================================")
    CONTROLS["env"].log.info("Запись начата.")
    CONTROLS["env"].log.info("===========================================")
    CONTROLS["env"].log.debug(f"Перечисление кодов ошибок:")
    CONTROLS["env"].log.debug(f"{';'.join(['='.join((str(key), str(val),)) for key, val in ERRORS.items()])}")

    # Adapt for HD-screens.
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        CONTROLS["env"].log.debug("Включено масштабирование высокого разрешения.")
    if hasattr(Qt, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        CONTROLS["env"].log.debug("Используются пиксельные карты высокого разрешения.")

    # Initiate DB adapter
    CONTROLS["db_bus"] = DBDialer()
    app = QApplication(sys.argv)
    CONTROLS["env"].log.info("Инициализирован экзеспляр приложения.")

    # Override inner exceptions to pass them outside.
    sys.excepthook = CONTROLS["env"].redirect_except_hook
    CONTROLS["env"].log.debug("Настроен перехват внутренних событий PyQt.")

    # Searching config-file
    CONTROLS["env"].log.info("Поиск файла конфигурации...")
    if CONTROLS["env"].check_config_file_exists() != 0:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Файл конфигурации не обнаружен!\nБудут использованы значения по умолчанию.")
        msg.setWindowTitle("Информация о запуске.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()
        CONTROLS["env"].initiate_default_config()
        CONTROLS["env"].save_config_to_file()
    else:
        CONTROLS["env"].load_config_from_file()

    # Search for Database file
    CONTROLS["env"].log.info("Поиск файла базы данных...")
    if CONTROLS["env"].check_db_file_exists() != 0:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Файл базы данных не обнаружен!\nБаза данных будет сконструирована.")
        msg.setWindowTitle("Информация о запуске.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()
        CONTROLS["env"].create_db_file()
        CONTROLS["env"].call_db_ddl(f"{getcwd()}\\sql\\ddl.sql")
    else:
        LOCAL_VARS["last_err_code"] = CONTROLS["env"].open_db_file()
        if LOCAL_VARS["last_err_code"] != 0:
            CONTROLS["env"].call_db_purge(f"{getcwd()}\\sql\\get_datatables_from_db.sql")
            CONTROLS["env"].call_db_ddl(f"{getcwd()}\\sql\\ddl.sql")

    # Start the application
    CONTROLS["env"].log.info("Инициализация главной формы приложения...")
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
    if LOCAL_VARS["last_err_code"] == 0:
        CONTROLS["env"].log.info(f"Код выхода: {LOCAL_VARS['last_err_code']}")
    else:
        CONTROLS["env"].log.error(f"Код выхода: {LOCAL_VARS['last_err_code']}")

    del(CONTROLS["db_bus"])
    logging.shutdown()
    sys.exit(LOCAL_VARS['last_err_code'])
