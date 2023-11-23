from forms.settings_form_ui import Ui_SettingsForm
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QLocale
from os import getcwd


class SettingsFormIf(QWidget, Ui_SettingsForm):
    def __init__(self):
        super().__init__()
        super().setupUi(self,)
        super().retranslateUi(self,)
        self.init_ui()


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
        #self.applyCfg_btn.clicked.connect()
        #self.denyAndExit_btn.clicked.connect()
        
        return None

    def choose_db_dialog(self) -> None:

        ofd_invitation = "Выберите файл БД."
        ofd_start_location = getcwd()
        ofd_filter = "База данных (*.db);;База данных (*.sqlite);;Все файлы (*)"
        db_file = QFileDialog.getOpenFileName(self, ofd_invitation,
                                              ofd_start_location, ofd_filter)[0]
        self.dbPath_lineEd.setText(db_file)

        return None

    
