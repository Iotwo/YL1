from forms.settings_form_ui import Ui_SettingsForm
from PyQt5.QtWidgets import QWidget, QFileDialog, QMessageBox
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QLocale
from os import getcwd
from scripts.variables import CONTROLS, LOCAL_VARS, CONFIG, ERRORS


class SettingsFormIf(QWidget, Ui_SettingsForm):
    def __init__(self, parent):
        super().__init__()
        super().setupUi(self,)
        super().retranslateUi(self,)
        self.parentForm = parent
        self.init_ui()
        self.load_cfg()

        CONTROLS["env"].log.debug("Форма настроек приложения инициализирована.")

        return None

    def __new__(cls, *args, **kwargs) -> object:
        instance = super().__new__(cls)
        CONTROLS["env"].log.debug(f"Создан экземпляр #{id(instance)}-{type(instance)}")
        
        return instance
    

    def init_ui(self) -> None:
        self.allow_int_on_defBtns_lineEd = QIntValidator(0, 30000)
        locale = QLocale(QLocale.English, QLocale.UnitedStates)
        self.allow_int_on_defBtns_lineEd.setLocale(locale)
        self.defBtn1_lnEd.setValidator(self.allow_int_on_defBtns_lineEd)
        self.defBtn2_lnEd.setValidator(self.allow_int_on_defBtns_lineEd)
        self.defBtn3_lnEd.setValidator(self.allow_int_on_defBtns_lineEd)
        self.defBtn4_lnEd.setValidator(self.allow_int_on_defBtns_lineEd)
        self.defBtn5_lnEd.setValidator(self.allow_int_on_defBtns_lineEd)
        self.defBtn6_lnEd.setValidator(self.allow_int_on_defBtns_lineEd)

        self.locateDB_btn.clicked.connect(self.choose_db_dialog)
        self.applyCfg_btn.clicked.connect(self.apply_new_settings_and_exit)
        self.denyAndExit_btn.clicked.connect(self.cancel_and_exit)
        
        return None

    def choose_db_dialog(self) -> None:

        ofd_invitation = "Выберите файл БД."
        ofd_start_location = getcwd()
        ofd_filter = "База данных (*.db);;База данных (*.sqlite);;Все файлы (*)"
        db_file = QFileDialog.getOpenFileName(self, ofd_invitation,
                                              ofd_start_location, ofd_filter)[0]
        self.dbPath_lineEd.setText(db_file)

        return None

    def apply_new_settings_and_exit(self) -> None:
        CONTROLS["env"].log.info("Запись конфигурации в буфер..")
        try:
            CONFIG["db_path"] = self.dbPath_lineEd.text()
            CONFIG["def_btn1"] = int(self.defBtn1_lnEd.text())
            CONFIG["def_btn2"] = int(self.defBtn2_lnEd.text())
            CONFIG["def_btn3"] = int(self.defBtn3_lnEd.text())
            CONFIG["def_btn4"] = int(self.defBtn4_lnEd.text())
            CONFIG["def_btn5"] = int(self.defBtn5_lnEd.text())
            CONFIG["def_btn6"] = int(self.defBtn6_lnEd.text())
            
        except Exception as ex:
            CONTROLS["env"].log.debug(f"Error code: 4 - {ERRORS[3]}")
            CONTROLS["env"].log.error("Ошибка обработки конфигурации.")
            CONTROLS["env"].log.debug(f"Raw exception data: {ex.__str__()}")
            return None

        CONTROLS["env"].log.info("Сохранение конфигурации в файл..")
        try:
            CONTROLS["env"].save_config_to_file()
            self.parentForm.import_configuration()
        except Exception as ex:
            CONTROLS["env"].log.debug(f"Error code: 4 - {ERRORS[3]}")
            CONTROLS["env"].log.error("Ошибка обработки конфигурации.")
            CONTROLS["env"].log.debug(f"Raw exception data: {ex.__str__()}")
            return None

        CONTROLS["env"].log.info("Сохранение новой конфигурации выполнено успешно.")
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Конфигурация обновлена.\nЕсли вы меняли путь к БД - перезагрузите программу.")
        msg.setWindowTitle("Изменение конфигурации.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()
        self.hide()
        return None
    

    def cancel_and_exit(self) -> None:
        self.dbPath_lineEd.setText(CONFIG["db_path"])
        self.defBtn1_lnEd.setText(str(CONFIG["def_btn1"]))
        self.defBtn2_lnEd.setText(str(CONFIG["def_btn2"]))
        self.defBtn3_lnEd.setText(str(CONFIG["def_btn3"]))
        self.defBtn4_lnEd.setText(str(CONFIG["def_btn4"]))
        self.defBtn5_lnEd.setText(str(CONFIG["def_btn5"]))
        self.defBtn6_lnEd.setText(str(CONFIG["def_btn6"]))
        CONTROLS["env"].log.info("Изменения конфигурарции отменены.")
        self.hide()

        return None

    def load_cfg(self) -> None:
        
        self.dbPath_lineEd.setText(CONFIG["db_path"])
        self.defBtn1_lnEd.setText(CONFIG["def_btn1"])
        self.defBtn2_lnEd.setText(CONFIG["def_btn2"])
        self.defBtn3_lnEd.setText(CONFIG["def_btn3"])
        self.defBtn4_lnEd.setText(CONFIG["def_btn4"])
        self.defBtn5_lnEd.setText(CONFIG["def_btn5"])
        self.defBtn6_lnEd.setText(CONFIG["def_btn6"])
        CONTROLS["env"].log.debug("Настройки программы загружены в форму конфигурации.")
        return None
