from os import getcwd, startfile
import csv
from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QListWidget, QListWidgetItem, QFileDialog
from PyQt5.QtGui import QDoubleValidator, QMouseEvent
from PyQt5.QtCore import QLocale
from forms.main_form_ui import Ui_MainForm
from forms.settings_form_ui import Ui_SettingsForm
from forms.settings_form_form import SettingsFormIf
from scripts.variables import CONTROLS, LOCAL_VARS, CONFIG


class MainFormIf(QMainWindow, Ui_MainForm):
    """
    DESCR: Defines application main form behaviour
    REQUIRE: PyQt5
    """
    
    def __init__(self) -> None:
        super().__init__()
        super().setupUi(self,)
        super().retranslateUi(self,)
        self.init_ui()

        CONTROLS["env"].log.debug("Инициализация формы настроек.")
        self.settings = SettingsFormIf(self)
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
        instance = super().__new__(cls)
        instance.settings = None
        instance.table_state = None
        instance.selected_row_data = None
        instance.selected_row_updated_data = None
        CONTROLS["env"].log.debug(f"Создан экземпляр #{id(instance)}-{type(instance)}")
        
        return instance

    def add_new_rec(self) -> None:
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

    def call_edit_sups_form(self) -> None:
        self.supports.show()

        return None

    def call_info(self) -> None:
        startfile(f"{getcwd()}\\{LOCAL_VARS['help_path']}")
        
        return None

    def call_settings_form(self) -> None:
        self.settings.show()
        CONTROLS["env"].log.debug("Открыта форма настроек.")

        return None
    
    def closeEvent(self, event) -> None:
        """
        NOTE: PROCESS THIS!!!
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
        result = None
        if self.table_state == LOCAL_VARS["table_states"][1]:
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
            self.backlog_tableWidget.selectRow(None)
            self.selected_row_data = None
            self.selected_row_updated_data = None
            self.app_status_bar.clearMessage()
            self.app_status_bar.showMessage(f"Приложение готово. БД подключена.")
        return None

    def export_report_data(self, data: list) -> None:
        """
            DESC:
        """
        return None

    def form_report_all_time(self) -> None:
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
        return None

    def form_report_last_month(self) -> None:
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
        return None

    def form_report_last_week(self) -> None:
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
        return None
    
    def form_report_today(self) -> None:
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
        return None

    def init_ui(self) -> None:
        self.allow_float_on_amt_lineEd = QDoubleValidator(0.00,9999999999999.99,2)
        locale = QLocale(QLocale.English, QLocale.UnitedStates)
        self.allow_float_on_amt_lineEd.setNotation(QDoubleValidator.StandardNotation)
        self.allow_float_on_amt_lineEd.setLocale(locale)
        self.amount_lineEd.setValidator(self.allow_float_on_amt_lineEd)

        self.set_column_headers()

        self.backlog_tableWidget.cellClicked.connect(self.select_data_from_row)
        self.backlog_tableWidget.cellDoubleClicked.connect(self.set_record_edit_in_backlog)
        self.backlog_tableWidget.cellChanged.connect(self.complete_record_edit_in_backlog)
        self.menu_settings_btn.triggered.connect(self.call_settings_form)
        self.menu_call_info_btn.triggered.connect(self.call_info)
        self.menu_report_today_btn.triggered.connect(self.form_report_today)
        self.menu_report_last_week_btn.triggered.connect(self.form_report_last_week)
        self.menu_report_last_month_btn.triggered.connect(self.form_report_last_month)
        self.menu_report_all_time_btn.triggered.connect(self.form_report_all_time)
        self.menu_import_btn.triggered.connect(self.import_ext_data)
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
        self.defVal1_btn.setText(self.settings.defBtn1_lnEd.text())
        self.defVal2_btn.setText(self.settings.defBtn2_lnEd.text())
        self.defVal3_btn.setText(self.settings.defBtn3_lnEd.text())
        self.defVal4_btn.setText(self.settings.defBtn4_lnEd.text())
        self.defVal5_btn.setText(self.settings.defBtn5_lnEd.text())
        self.defVal6_btn.setText(self.settings.defBtn6_lnEd.text())
        
        return None    

    def import_ext_data(self) -> None:

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

        self.catSelection_list.clear()
        rows = CONTROLS["env"].call_select_cats_of_op(f"{getcwd()}\\sql\\get_cats_of_operation.sql", self.opSelection_cmbBox.currentText())
        for row in rows:
            self.catSelection_list.addItem(QListWidgetItem(row[0]))
        
        return None

    def load_operation_types(self) -> None:
        self.opSelection_cmbBox.clear()
        rows = CONTROLS["env"].call_sql_select_cmd(f"{getcwd()}\\sql\\get_all_operations.sql")
        for row in rows:
            self.opSelection_cmbBox.addItem(row[0])
        
    
    def load_last_X_actions(self) -> None:
        """
        DESCR: load last X actions from Action_log table into tabWidget
        REQUIRE: QTableWidgetItem, QTableWidget, os.getcwd
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
        CONTROLS["env"].log.debug(f"Левый одиночный клик мыши в таблице в ряд {row_index}")
        self.selected_row_data = [self.backlog_tableWidget.item(row_index, j).text()
                                  for j in range(self.backlog_tableWidget.columnCount())]
        CONTROLS["env"].log.debug(f"Выбран диапазон значений: {self.selected_row_data} из таблицы.")
        
        return None

    def set_column_headers(self) -> None:
        self.backlog_tableWidget.setHorizontalHeaderLabels(LOCAL_VARS["RU_db_tables"]["Actions_log"])
        self.backlog_tableWidget.setColumnWidth(0, 40)
        self.backlog_tableWidget.setColumnWidth(1, 120)
        self.backlog_tableWidget.setColumnWidth(2, 80)
        self.backlog_tableWidget.setColumnWidth(3, 100)
        self.backlog_tableWidget.setColumnWidth(4, 100)
        self.backlog_tableWidget.setColumnWidth(5, 200)

        return None

    def set_def_val_1_to_amount(self) -> None:
        self.amount_lineEd.setText("")
        self.amount_lineEd.setText(str(CONFIG["def_btn1"]))
        CONTROLS["env"].log.debug(f"Значение {CONFIG['def_btn1']} записано в поле ввода.")
        
        return None

    def set_def_val_2_to_amount(self) -> None:
        self.amount_lineEd.setText("")
        self.amount_lineEd.setText(str(CONFIG["def_btn2"]))
        CONTROLS["env"].log.debug(f"Значение {CONFIG['def_btn2']} записано в поле ввода.")
        
        return None

    def set_def_val_3_to_amount(self) -> None:
        self.amount_lineEd.setText("")
        self.amount_lineEd.setText(str(CONFIG["def_btn3"]))
        CONTROLS["env"].log.debug(f"Значение {CONFIG['def_btn3']} записано в поле ввода.")
        
        return None

    def set_def_val_4_to_amount(self) -> None:
        self.amount_lineEd.setText("")
        self.amount_lineEd.setText(str(CONFIG["def_btn4"]))
        CONTROLS["env"].log.debug(f"Значение {CONFIG['def_btn4']} записано в поле ввода.")
        
        return None

    def set_def_val_5_to_amount(self) -> None:
        self.amount_lineEd.setText("")
        self.amount_lineEd.setText(str(CONFIG["def_btn5"]))
        CONTROLS["env"].log.debug(f"Значение {CONFIG['def_btn5']} записано в поле ввода.")
        
        return None

    def set_def_val_6_to_amount(self) -> None:
        self.amount_lineEd.setText("")
        self.amount_lineEd.setText(str(CONFIG["def_btn6"]))
        CONTROLS["env"].log.debug(f"Значение {CONFIG['def_btn6']} записано в поле ввода.")
        
        return None

    def set_record_edit_in_backlog(self, row_index, column_index) -> None:
        CONTROLS["env"].log.debug(f"Левый двойной клик мыши в таблице в ряд {row_index}")
        if self.table_state == LOCAL_VARS["table_states"][0]:
            self.table_state = LOCAL_VARS["table_states"][1]
            self.app_status_bar.clearMessage()
            self.app_status_bar.showMessage(f"Состояние таблицы - {LOCAL_VARS['RU_table_states'][1]}")
            CONTROLS["env"].log.debug(f"Редактируется ячейка {row_index}:{column_index}.")
            CONTROLS["env"].log.debug(f"Исходные значения: {self.selected_row_data}.")

        return None

    

    #=====================================

    def call_export_form(self):
        self.reports.show()

    def add_new_rec_back(self):
        logging.debug('Попытка добавить новую запись...')
        cat_chosen = True if self.rec_cat_selector_cmb.currentIndex() != -1 else False
        op_chosen = True if self.rec_op_selector_cmb.currentIndex() != -1 else False
        payment_set = True if len(self.price_txt.text()) > 0 else False
        payment_set = True if all([True for sym in self.price_txt.text() if sym in '0123456789.']) is True else False
        if all((cat_chosen, op_chosen, payment_set,)) is True:
            op_chosen = self.OPERATION_IDs[self.rec_op_selector_cmb.currentIndex()]
            cat_chosen = self.CATEGORIES_IDs[self.rec_cat_selector_cmb.currentIndex()]
            payment_set = float(self.price_txt.text())
            try:
                supportive_vestments.sql_insert_new_action(db_cursor=local_vars.DB_CURSOR,
                                                           db_connector=local_vars.DB_CONNECTOR,
                                                           datetime_stamp=datetime.datetime.now().replace(microsecond=0), op=op_chosen,
                                                           cat=cat_chosen, paid=payment_set,
                                                           comment=self.rec_comment_txt.toPlainText())
                logging.debug('Запись успешно добавлена')
            except Exception as ex:
                logging.error(ex)
                return None
            self.cancel_rec()
            self.load_last_actions()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Не все поля заполнены корректно.")
            msg.setWindowTitle("Внимание!")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            retval = msg.exec()
        return None


    def cancel_rec(self):
        self.rec_cat_selector_cmb.setCurrentIndex(-1)
        self.rec_op_selector_cmb.setCurrentIndex(-1)
        self.price_txt.setText('')
        self.rec_comment_txt.setPlainText('')

    def select_cur_act_row(self, row_index):
        self.actions_table.selectRow(row_index)

    def del_cur_action(self, row_index):
        logging.debug('Попытка удалить запись...')
        self.actions_table.selectRow(row_index)
        act = self.actions_table.selectedItems()[0].data(0)
        op = self.OPERATION_IDs[self.rec_op_selector_cmb.findText(self.actions_table.selectedItems()[1].data(0))]
        cat = self.CATEGORIES_IDs[self.rec_cat_selector_cmb.findText(self.actions_table.selectedItems()[2].data(0))]
        paid = self.actions_table.selectedItems()[3].data(0)
        data = {
            'action_datetime': act,
            'optype_id': op,
            'cat_id': cat,
            'paid_value': paid,
            'comment': self.actions_table.selectedItems()[4].data(0)
        }
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Вы действительно хотите удалить эту запись?")
        msg.setWindowTitle("Подтверждение удаления.")
        msg.setStandardButtons(QMessageBox.StandardButton.No)
        msg.addButton(QMessageBox.StandardButton.Yes)
        retval = msg.exec()
        if retval == QMessageBox.StandardButton.Yes:
            supportive_vestments.sql_delete_action_data(local_vars.DB_CURSOR, local_vars.DB_CONNECTOR, data)
            self.load_last_actions()
            logging.debug('Запись успешно удалена.')
        else:
            logging.warning('В ходе удаления возникли ошибки.')

        return None
