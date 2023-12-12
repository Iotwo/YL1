from os import getcwd, startfile
import csv
from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QListWidget, QListWidgetItem, QFileDialog
from PyQt5.QtGui import QDoubleValidator, QMouseEvent
from PyQt5.QtCore import QLocale
from forms.main_form_ui import Ui_MainForm
from forms.settings_form_ui import Ui_SettingsForm
from forms.settings_form_form import SettingsFormIf
from forms.edit_fields_form_ui import Ui_EditFieldsForm
from forms.edit_fields_form_form import EditFieldsFormIf
from scripts.variables import CONTROLS, LOCAL_VARS, CONFIG


class MainFormIf(QMainWindow, Ui_MainForm):
    """
    DESCR: Defines application main form behaviour.
           Main form is needed for records processing
           and statistics collecting.
    """
    
    def __init__(self) -> None:
        """
        DESCR: Initiate newly created exemplar and configure it.
        """
        
        super().__init__()
        super().setupUi(self,)
        super().retranslateUi(self,)
        self.init_ui()

        CONTROLS["env"].log.debug("Инициализация формы настроек.")
        self.settings = SettingsFormIf(self)
        self.edit_fields = EditFieldsFormIf(self)
        self.import_configuration()
        
        CONTROLS["env"].log.debug("Загрузка последних записей.")
        self.load_operation_types()
        self.load_last_X_actions()
        self.table_state = LOCAL_VARS["table_states"][0]
        CONTROLS["env"].log.debug("Главная форма приложения инициализирована.")
        self.app_status_bar.clearMessage()
        self.app_status_bar.showMessage(f"Приложение готово. БД подключена.")
        
        return None

    def __new__(cls, *args, **kwargs) -> object:
        """
        DESCR: Create new exemplar of the class,
               add custom fields for child-forms and buffers
        """
        instance = super().__new__(cls)
        instance.settings = None
        instance.edit_fields = None
        instance.table_state = None
        instance.selected_row_data = None
        instance.selected_row_updated_data = None
        CONTROLS["env"].log.debug(f"Создан экземпляр #{id(instance)}-{type(instance)}")
        
        return instance

    def add_new_rec(self) -> None:
        """
        DESCR: Add new record about financial action to  DB
        """
        CONTROLS["env"].log.debug(f"Начат процесс добавления записи, проверка заполненности всех атрибутов...")
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText("Не хватает данных\n для вставки новой записи!")
        msg.setWindowTitle("Вставка записи.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        result = None
        
        if self.opSelection_cmbBox.currentIndex() == -1:
            retval = msg.exec()
            CONTROLS["env"].log.debug("Вставка записи не произведена, не хватает данных.")
            return result
        if self.catSelection_list.currentRow() == -1:
            retval = msg.exec()
            CONTROLS["env"].log.debug("Вставка записи не произведена, не хватает данных.")
            return result
        if self.amount_lineEd.text() == "":
            retval = msg.exec()
            CONTROLS["env"].log.debug("Вставка записи не произведена, не хватает данных.")
            return result
        
        ins_data = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.opSelection_cmbBox.currentText(),
                    self.catSelection_list.currentItem().text(), self.amount_lineEd.text()]
        CONTROLS["env"].log.info("Вставка новой записи...")
        CONTROLS["env"].log.debug(f"Данные для вставки: {ins_data}")
        LOCAL_VARS["last_err_code"] = CONTROLS["env"].call_insert_new_rec(f"{getcwd()}\\sql\\insert_value_into_actions.sql", "Actions_log", ins_data)
        if LOCAL_VARS["last_err_code"] == 0:
            CONTROLS["env"].log.info("Добавлена запись.")
        else:
            CONTROLS["env"].log.warn("Не удалось добавить запись.")

        self.load_last_X_actions()
        
        return result

    def call_info(self) -> None:
        """
        DESCR: Open help
        """
        startfile(f"{getcwd()}\\{LOCAL_VARS['help_path']}")
        
        return None

    def call_settings_form(self) -> None:
        """
        DESCR: Interact with Settings form
        """
        self.settings.show()
        CONTROLS["env"].log.debug("Открыта форма настроек.")

        return None

    def call_edit_fields_form(self) -> None:
        """
        DESCR: Interact with Edit form
        """
        self.edit_fields.show()
        CONTROLS["env"].log.debug("Открыта форма редактора полей.")

        return None
    
    def closeEvent(self, event) -> None:
        """
        DESCR: Process closing event on form. Ask for confirmation.
        """  
        CONTROLS["env"].log.debug("Закрытие главной формы приложения.")
        try:
            CONTROLS["env"].log.debug("Освобождение ресурсов формы...")
            retval = QMessageBox.question(self, "Выход", "Закрыть приложение?",
                                          QMessageBox.Close | QMessageBox.Cancel, QMessageBox.Cancel)
            event.ignore()
            if retval == QMessageBox.Close:
                event.accept()
            else:
                event.ingore()
                
        except Exception as ex:
            pass

        return None

    def complete_record_edit_in_backlog(self, row_index, col_index) -> None:
        """
        DESCR: Edit-part-2. Set new values for edited record and complete edition.
        """
        if self.table_state == LOCAL_VARS["table_states"][1]:
            self.selected_row_updated_data = [self.backlog_tableWidget.item(row_index, j).text()
                                              for j in range(self.backlog_tableWidget.columnCount())]
            CONTROLS["env"].log.debug(f"Изменённые значения: {self.selected_row_updated_data}.")
            upd_p = {LOCAL_VARS["db_tables"]["Actions_log"][i]: self.selected_row_updated_data[i]
                     for i in range(len(LOCAL_VARS["db_tables"]["Actions_log"]))}
            CONTROLS["env"].log.debug(f"Кортеж изменений: {upd_p}")
            
            LOCAL_VARS["last_err_code"] = CONTROLS["env"].call_update_record_in_table(f"{getcwd()}\\sql\\update_record_in_table_actionslog.sql",
                                                                                      "Actions_log", upd_p, "id", str(self.selected_row_updated_data[0]))
            self.table_state = LOCAL_VARS["table_states"][0]
            CONTROLS["env"].log.debug(f"Таблица в состоянии {LOCAL_VARS['RU_table_states'][0]}")
            self.app_status_bar.clearMessage()
            self.app_status_bar.showMessage(f"Состояние таблицы - {LOCAL_VARS['RU_table_states'][0]}")
            self.backlog_tableWidget.selectRow(None)
            self.selected_row_data = None 
            self.selected_row_updated_data = None
            self.app_status_bar.clearMessage()
            self.app_status_bar.showMessage(f"Приложение готово. БД подключена.")

        return None

    def decline_changes_and_clear(self) -> None:
        """
        DESCR: Method declines made unsaved changes or removes selected record.
        """
        result = None
        if self.table_state == LOCAL_VARS["table_states"][1]:
            CONTROLS["env"].log.info("Отмена изменений, внесённых в поля.")
            self.opSelection_cmbBox.selectIndex(-1)
            self.catSelection_list.selectRow(-1)
            self.amount_lineEd.setText("")
        elif self.table_state == LOCAL_VARS["table_states"][0]:
            CONTROLS["env"].log.info("Попытка удалить запись...")
            CONTROLS["env"].log.debug(f"Удаляемая запись: {self.selected_row_data}")
            LOCAL_VARS["last_err_code"] = CONTROLS["env"].call_delete_rec_command(f"{getcwd()}\\sql\\delete_record_from_table.sql", "Actions_log", "id", str(self.selected_row_data[0]))
            if LOCAL_VARS["last_err_code"] == 0:
                CONTROLS["env"].log.info("Запись удалена.")
            else:
                CONTROLS["env"].log.error("Во время удаления записи возникла ошибка.")
            self.load_last_X_actions()
            self.backlog_tableWidget.selectRow(-1)
            self.selected_row_data = None
            self.selected_row_updated_data = None
            self.app_status_bar.clearMessage()
            self.app_status_bar.showMessage(f"Приложение готово. БД подключена.")
        return None

    def form_report_all_time(self) -> None:
        """
        DESCR: Form report category-by-category for all timespan.
        """
        CONTROLS["env"].log.info("Построение отчёта за всё время в формате csv...")
        result = CONTROLS["env"].call_sql_select_cmd(f"{getcwd()}\\sql\\form_report_all_time.sql")
        if result is None:
            CONTROLS["env"].log.warn("Во время построения отчёта произошла ошибка.")
            return None
        LOCAL_VARS["last_err_code"] = CONTROLS["env"].create_report_file("csv", result)
        if LOCAL_VARS["last_err_code"] != 0:
            CONTROLS["env"].log.warn("Во время сохранения отчёта произошла ошибка.")
            return None
        CONTROLS["env"].log.info("Отчёт сформирован и выгружен.")

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Отчёт сформирован!")
        msg.setWindowTitle("Отчёт за период.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()
        return None

    def form_report_last_month(self) -> None:
        """
        DESCR: Form report category-by-category for last month.
        """
        CONTROLS["env"].log.info("Построение отчёта за последний месяц в формате csv...")
        result = CONTROLS["env"].call_sql_select_cmd(f"{getcwd()}\\sql\\form_report_last_month.sql")
        if result is None:
            CONTROLS["env"].log.warn("Во время построения отчёта произошла ошибка.")
            return None
        LOCAL_VARS["last_err_code"] = CONTROLS["env"].create_report_file("csv", result)
        if LOCAL_VARS["last_err_code"] != 0:
            CONTROLS["env"].log.warn("Во время сохранения отчёта произошла ошибка.")
            return None
        CONTROLS["env"].log.info("Отчёт сформирован и выгружен.")

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Отчёт сформирован!")
        msg.setWindowTitle("Отчёт за период.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()
        return None

    def form_report_last_week(self) -> None:
        """
        DESCR: Form report category-by-category for last week.
        """
        CONTROLS["env"].log.info("Построение отчёта за последние 7 дней в формате csv...")
        result = CONTROLS["env"].call_sql_select_cmd(f"{getcwd()}\\sql\\form_report_last_week.sql")
        if result is None:
            CONTROLS["env"].log.warn("Во время построения отчёта произошла ошибка.")
            return None
        LOCAL_VARS["last_err_code"] = CONTROLS["env"].create_report_file("csv", result)
        if LOCAL_VARS["last_err_code"] != 0:
            CONTROLS["env"].log.warn("Во время сохранения отчёта произошла ошибка.")
            return None
        CONTROLS["env"].log.info("Отчёт сформирован и выгружен.")

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Отчёт сформирован!")
        msg.setWindowTitle("Отчёт за период.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()
        return None
    
    def form_report_today(self) -> None:
        """
        DESCR: Form report category-by-category for this day.
        """
        CONTROLS["env"].log.info("Построение отчёта за день в формате csv...")
        result = CONTROLS["env"].call_sql_select_cmd(f"{getcwd()}\\sql\\form_report_today.sql")
        if result is None:
            CONTROLS["env"].log.warn("Во время построения отчёта произошла ошибка.")
            return None
        LOCAL_VARS["last_err_code"] = CONTROLS["env"].create_report_file("csv", result)
        if LOCAL_VARS["last_err_code"] != 0:
            CONTROLS["env"].log.warn("Во время сохранения отчёта произошла ошибка.")
            return None
        CONTROLS["env"].log.info("Отчёт сформирован и выгружен.")

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Отчёт сформирован!")
        msg.setWindowTitle("Отчёт за период.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()
        return None

    def init_ui(self) -> None:
        """
        DESCR: Initiate interface components.
        """
        self.allow_float_on_amt_lineEd = QDoubleValidator(0.00,9999999999999.99,2)
        locale = QLocale(QLocale.English, QLocale.UnitedStates)
        self.allow_float_on_amt_lineEd.setNotation(QDoubleValidator.StandardNotation)
        self.allow_float_on_amt_lineEd.setLocale(locale)
        self.amount_lineEd.setValidator(self.allow_float_on_amt_lineEd)

        self.set_column_headers()

        self.backlog_tableWidget.cellClicked.connect(self.select_data_from_row)
        self.backlog_tableWidget.cellDoubleClicked.connect(self.set_record_edit_in_backlog)
        self.backlog_tableWidget.cellChanged.connect(self.complete_record_edit_in_backlog)
        self.menu_call_info_btn.triggered.connect(self.call_info)
        self.menu_edit_fields_btn.triggered.connect(self.call_edit_fields_form)
        self.menu_import_btn.triggered.connect(self.import_ext_data)
        self.menu_report_today_btn.triggered.connect(self.form_report_today)
        self.menu_report_last_week_btn.triggered.connect(self.form_report_last_week)
        self.menu_report_last_month_btn.triggered.connect(self.form_report_last_month)
        self.menu_report_all_time_btn.triggered.connect(self.form_report_all_time)
        self.menu_settings_btn.triggered.connect(self.call_settings_form)
        self.opSelection_cmbBox.currentIndexChanged.connect(self.load_categories_of_optype)
        self.defVal1_btn.clicked.connect(self.set_def_val_1_to_amount)
        self.defVal2_btn.clicked.connect(self.set_def_val_2_to_amount)
        self.defVal3_btn.clicked.connect(self.set_def_val_3_to_amount)
        self.defVal4_btn.clicked.connect(self.set_def_val_4_to_amount)
        self.defVal5_btn.clicked.connect(self.set_def_val_5_to_amount)
        self.defVal6_btn.clicked.connect(self.set_def_val_6_to_amount)
        self.clear_btn.clicked.connect(self.decline_changes_and_clear)
        self.addRec_btn.clicked.connect(self.add_new_rec)
        
        return None

    def import_configuration(self) -> None:
        """
        DESCR: Import configured values from Settings.
        """
        self.defVal1_btn.setText(self.settings.defBtn1_lnEd.text())
        self.defVal2_btn.setText(self.settings.defBtn2_lnEd.text())
        self.defVal3_btn.setText(self.settings.defBtn3_lnEd.text())
        self.defVal4_btn.setText(self.settings.defBtn4_lnEd.text())
        self.defVal5_btn.setText(self.settings.defBtn5_lnEd.text())
        self.defVal6_btn.setText(self.settings.defBtn6_lnEd.text())
        
        return None    

    def import_ext_data(self) -> None:
        """
        DESCR: Load operational data from external source.
        """
        retval = QMessageBox.warning(self, "Импорт",
                                     "Внимание!\nДля корректного импорта файл должен\nотвечать следующим требованиям:\n" +\
                                     "\" - символ цитирования, ; - разделитель.",
                                     QMessageBox.Ok, QMessageBox.Ok)
        CONTROLS["env"].log.info("Импорт записей в файл...")
        imp_invitation = "Выберите файл для импорта записей."
        imp_start_location = getcwd()
        imp_filter = "Файл CSV (*.csv);;Все файлы (*)"
        imp_file = QFileDialog.getOpenFileName(self, imp_invitation,
                                               imp_start_location, imp_filter)[0]
        if len(imp_file) > 0:
            CONTROLS["env"].log.info("Выбран файл для импорта.")
            CONTROLS["env"].log.debug(f"{imp_file}")
            LOCAL_VARS["last_err_code"] = CONTROLS["env"].import_records_from_file(imp_file,
                                                                                   f"{getcwd()}\\sql\\insert_value_into_actions.sql",
                                                                                   "Actions_log")
            if LOCAL_VARS["last_err_code"] == 0:
                CONTROLS["env"].log.info("Импорт успешно выполнен. Записи БД будут перезагружены.")
                self.load_last_X_actions()
            else:
                CONTROLS["env"].log.warning("Во время импорта данных произошла ошибка!")
        else:
            CONTROLS["env"].log.info("Импорт отменён пользователем.")
                
        return None

    def load_categories_of_optype(self, cmb_index) -> None:
        """
        DESCR: Load categories of exact operation from DB.
        """
        self.catSelection_list.clear()
        rows = CONTROLS["env"].call_select_cats_of_op(f"{getcwd()}\\sql\\get_cats_of_operation.sql", self.opSelection_cmbBox.currentText())
        for row in rows:
            self.catSelection_list.addItem(QListWidgetItem(row[0]))
        
        return None

    def load_operation_types(self) -> None:
        """
        DESCR: Load all operation types from DB.
        """
        self.opSelection_cmbBox.clear()
        rows = CONTROLS["env"].call_sql_select_cmd(f"{getcwd()}\\sql\\get_all_operations.sql")
        for row in rows:
            self.opSelection_cmbBox.addItem(row[0])
        
    
    def load_last_X_actions(self) -> None:
        """
        DESCR: load last X actions from Action_log table into tabWidget
        """

        rows = CONTROLS["env"].call_select_last_x_records(f"{getcwd()}\\sql\\get_first_x_actions.sql")
        # next we must place row data into table
        self.backlog_tableWidget.clearContents()
        self.backlog_tableWidget.setRowCount(len(rows))
        rows = [tuple(map(str, [elem for elem in row])) for row in rows]
        # As soon as tableWidget can be populated only cell-by-cell...
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                self.backlog_tableWidget.setItem(i, j, QTableWidgetItem(rows[i][j]))
                
        return None

    def select_data_from_row(self, row_index) -> None:
        """
        DESCR: On click collect all data from clicked ROW
        """
        CONTROLS["env"].log.debug(f"Левый одиночный клик мыши в таблице в ряд {row_index}")
        self.selected_row_data = [self.backlog_tableWidget.item(row_index, j).text()
                                  for j in range(self.backlog_tableWidget.columnCount())]
        CONTROLS["env"].log.debug(f"Выбран диапазон значений: {self.selected_row_data} из таблицы.")
        
        return None

    def set_column_headers(self) -> None:
        """
        DESCR: Prettify column headers.
        """
        self.backlog_tableWidget.setHorizontalHeaderLabels(LOCAL_VARS["RU_db_tables"]["Actions_log"])
        self.backlog_tableWidget.setColumnWidth(0, 40)
        self.backlog_tableWidget.setColumnWidth(1, 120)
        self.backlog_tableWidget.setColumnWidth(2, 80)
        self.backlog_tableWidget.setColumnWidth(3, 100)
        self.backlog_tableWidget.setColumnWidth(4, 100)
        self.backlog_tableWidget.setColumnWidth(5, 200)

        return None

    def set_def_val_1_to_amount(self) -> None:
        """
        DESCR: Apply pre-defined value to button_1
        """
        self.amount_lineEd.setText("")
        self.amount_lineEd.setText(str(CONFIG["def_btn1"]))
        CONTROLS["env"].log.debug(f"Значение {CONFIG['def_btn1']} записано в поле ввода.")
        
        return None

    def set_def_val_2_to_amount(self) -> None:
        """
        DESCR: Apply pre-defined value to button_2
        """
        self.amount_lineEd.setText("")
        self.amount_lineEd.setText(str(CONFIG["def_btn2"]))
        CONTROLS["env"].log.debug(f"Значение {CONFIG['def_btn2']} записано в поле ввода.")
        
        return None

    def set_def_val_3_to_amount(self) -> None:
        """
        DESCR: Apply pre-defined value to button_3
        """
        self.amount_lineEd.setText("")
        self.amount_lineEd.setText(str(CONFIG["def_btn3"]))
        CONTROLS["env"].log.debug(f"Значение {CONFIG['def_btn3']} записано в поле ввода.")
        
        return None

    def set_def_val_4_to_amount(self) -> None:
        """
        DESCR: Apply pre-defined value to button_4
        """
        self.amount_lineEd.setText("")
        self.amount_lineEd.setText(str(CONFIG["def_btn4"]))
        CONTROLS["env"].log.debug(f"Значение {CONFIG['def_btn4']} записано в поле ввода.")
        
        return None

    def set_def_val_5_to_amount(self) -> None:
        """
        DESCR: Apply pre-defined value to button_5
        """
        self.amount_lineEd.setText("")
        self.amount_lineEd.setText(str(CONFIG["def_btn5"]))
        CONTROLS["env"].log.debug(f"Значение {CONFIG['def_btn5']} записано в поле ввода.")
        
        return None

    def set_def_val_6_to_amount(self) -> None:
        """
        DESCR: Apply pre-defined value to button_6
        """
        self.amount_lineEd.setText("")
        self.amount_lineEd.setText(str(CONFIG["def_btn6"]))
        CONTROLS["env"].log.debug(f"Значение {CONFIG['def_btn6']} записано в поле ввода.")
        
        return None

    def set_record_edit_in_backlog(self, row_index, column_index) -> None:
        """
        DESCR: Edit-part-1, select record for edition, collect pre-edited data...
        """
        CONTROLS["env"].log.debug(f"Левый двойной клик мыши в таблице в ряд {row_index}")
        if self.table_state == LOCAL_VARS["table_states"][0]:
            self.table_state = LOCAL_VARS["table_states"][1]
            self.app_status_bar.clearMessage()
            self.app_status_bar.showMessage(f"Состояние таблицы - {LOCAL_VARS['RU_table_states'][1]}")
            CONTROLS["env"].log.debug(f"Редактируется ячейка {row_index}:{column_index}.")
            CONTROLS["env"].log.debug(f"Исходные значения: {self.selected_row_data}.")

        return None
