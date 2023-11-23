from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import QLocale
from forms.main_form_ui import Ui_MainForm
from forms.settings_form_ui import Ui_SettingsForm
from forms.settings_form_form import SettingsFormIf
from scripts.variables import CONTROLS, LOCAL_VARS


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
        
        self.settings = SettingsFormIf()
        
        CONTROLS["env"].log.debug("Главная форма приложения загружена.")
        
        return None

    def call_edit_sups_form(self):
        self.supports.show()

    def call_settings_form(self):
        self.settings.show()

    def closeEvent(self, event):
        if self.close:
            CONTROLS["env"].log.debug("Закрытие главной формы приложения.")
            try:
                CONTROLS["env"].log.debug("Освобождение ресурсов формы...")
                #local_vars.DB_CONNECTOR.close()
                #CONTROLS["env"].log.debug('Подключение к базе данных закрыто.')
            except Exception as ex:
                CONTROLS["env"].log.error('Ошибка при завершении работы с базой данных.')
            CONTROLS["env"].log.debug("Главная форма закрыта. Попытка выхода из приложения...")
        else:
            event.ignore()

    def init_ui(self) -> None:
        self.allow_float_on_amt_lineEd = QDoubleValidator(0.00,9999999999999.99,2)
        locale = QLocale(QLocale.English, QLocale.UnitedStates)
        self.allow_float_on_amt_lineEd.setNotation(QDoubleValidator.StandardNotation)
        self.allow_float_on_amt_lineEd.setLocale(locale)
        self.amount_lineEd.setValidator(self.allow_float_on_amt_lineEd)

        self.set_column_headers()

        self.menu_settings_btn.triggered.connect(self.call_settings_form)
        
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








    def load_operations(self):
        self.rec_op_selector_cmb.clear()
        try:
            query_result = supportive_vestments.sql_select_all_operations(local_vars.DB_CURSOR)
            lines_cnt = len(query_result)
            if lines_cnt > 0:
                for i in range(lines_cnt):
                    self.rec_op_selector_cmb.addItem(query_result[i][1])
                    self.OPERATION_IDs.append(int(query_result[i][0]))
        except Exception as ex:
            print(ex)
            return -2

    def load_categories(self):
        self.rec_cat_selector_cmb.clear()
        try:
            query_result = supportive_vestments.sql_select_all_categories(local_vars.DB_CURSOR)
            lines_cnt = len(query_result)
            if lines_cnt > 0:
                for i in range(lines_cnt):
                    if query_result[i][1] == 'Пополнения':
                        self.DEPOSIT_ID = int(query_result[i][0])
                    self.rec_cat_selector_cmb.addItem(query_result[i][1])
                    self.CATEGORIES_IDs.append(int(query_result[i][0]))
        except Exception as ex:
            print(ex)
            return -2

    def load_last_actions(self):
        lines_cnt = 0
        try:
            for _ in range(self.actions_table.rowCount()):
                self.actions_table.removeRow(self.actions_table.rowCount() - 1)
            query_result = supportive_vestments.sql_select_all_actions(local_vars.DB_CURSOR)
            lines_cnt = len(query_result)
            if lines_cnt > 0:
                self.actions_table.setRowCount(lines_cnt)
                for i in range(lines_cnt):
                    for j in range(len(self.COLUMN_NAMES)):
                        self.actions_table.setItem(i, j, QTableWidgetItem(str(query_result[i][j + 1])))
        except Exception as ex:
            print(ex)
            return -1

    def set_cat_for_deposit(self):
        if self.rec_op_selector_cmb.currentText() == 'Поступления':
            self.rec_cat_selector_cmb.setCurrentIndex(self.CATEGORIES_IDs.index(self.DEPOSIT_ID))


    


    


    def form_report_today(self):
        logging.debug('Формируется отчёт за день...')
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        pros_list = supportive_vestments.sql_get_deposits_today(local_vars.DB_CURSOR)
        cons_list = supportive_vestments.sql_get_losses_today(local_vars.DB_CURSOR)
        with open(file=f'.\\reports\\report_at_{datetime.datetime.now().date()}.txt', mode='w', encoding='utf-8-sig') as rep:
            rep.write('=' * 70 + '\n')
            rep.write('Расходы за сегодня:'+ '\n')
            rep.write('=' * 70 + '\n')
            rep.write('Категория'.ljust(50) + 'Цена'.ljust(16) + '\n')
            for attr in cons_list:
                rep.write(f'{str(attr[0]).ljust(50)}{str(attr[1]).ljust(2)}' + '\n')
            rep.write('\n')
            rep.write('=' * 70 + '\n')
            rep.write('Доходы за сегодня:' + '\n')
            rep.write('=' * 70 + '\n')
            rep.write('Категория'.ljust(50) + 'Цена'.ljust(16) + '\n')
            for attr in pros_list:
                rep.write(f'{str(attr[0]).ljust(50)}{str(attr[1]).ljust(2)}' + '\n')
            rep.flush()
        pros = sum([float(attr[1]) for attr in pros_list])
        cons = sum([float(attr[1]) for attr in cons_list])
        msg.setText(f'Траты за сегодня: {cons} \nПополнения за сегодня: {pros}.\nОтчёт сохранён в директории программы.')
        msg.setWindowTitle("Отчёт готов.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()

        return None

    def form_report_week(self):
        logging.debug('Формируется отчёт за неделю...')
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        pros_list = supportive_vestments.sql_get_deposits_last_week(local_vars.DB_CURSOR)
        cons_list = supportive_vestments.sql_get_losses_last_week(local_vars.DB_CURSOR)
        with open(file=f'.\\reports\\report_at_{datetime.datetime.now().date()}.txt', mode='w',
                  encoding='utf-8-sig') as rep:
            rep.write('=' * 70 + '\n')
            rep.write('Расходы за последние 7 дней:' + '\n')
            rep.write('=' * 70 + '\n')
            rep.write('Категория'.ljust(50) + 'Цена'.ljust(16) + '\n')
            for attr in cons_list:
                rep.write(f'{str(attr[0]).ljust(50)}{str(attr[1]).ljust(2)}' + '\n')
            rep.write('\n')
            rep.write('=' * 70 + '\n')
            rep.write('Доходы за последние 7 дней:' + '\n')
            rep.write('=' * 70 + '\n')
            rep.write('Категория'.ljust(50) + 'Цена'.ljust(16) + '\n')
            for attr in pros_list:
                rep.write(f'{str(attr[0]).ljust(50)}{str(attr[1]).ljust(2)}' + '\n')
            rep.flush()
        pros = sum([float(attr[1]) for attr in pros_list])
        cons = sum([float(attr[1]) for attr in cons_list])
        msg.setText(
            f'Траты за последние 7 дней: {cons} \nПополнения за последние 7 дней: {pros}.\nОтчёт сохранён в директории программы.')
        msg.setWindowTitle("Отчёт готов.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()

        return None

    def form_report_month(self):
        logging.debug('Формируется отчёт за месяц...')
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        pros_list = supportive_vestments.sql_get_deposits_last_month(local_vars.DB_CURSOR)
        cons_list = supportive_vestments.sql_get_losses_last_month(local_vars.DB_CURSOR)
        with open(file=f'.\\reports\\report_at_{datetime.datetime.now().date()}.txt', mode='w',
                  encoding='utf-8-sig') as rep:
            rep.write('=' * 70 + '\n')
            rep.write('Расходы за последние 30 дней:' + '\n')
            rep.write('=' * 70 + '\n')
            rep.write('Категория'.ljust(50) + 'Цена'.ljust(16) + '\n')
            for attr in cons_list:
                rep.write(f'{str(attr[0]).ljust(50)}{str(attr[1]).ljust(2)}' + '\n')
            rep.write('\n')
            rep.write('=' * 70 + '\n')
            rep.write('Доходы за последние 30 дней:' + '\n')
            rep.write('=' * 70 + '\n')
            rep.write('Категория'.ljust(50) + 'Цена'.ljust(16) + '\n')
            for attr in pros_list:
                rep.write(f'{str(attr[0]).ljust(50)}{str(attr[1]).ljust(2)}' + '\n')
            rep.flush()
        pros = sum([float(attr[1]) for attr in pros_list])
        cons = sum([float(attr[1]) for attr in cons_list])
        msg.setText(
            f'Траты за последние 30 дней: {cons} \nПополнения за последние 30 дней: {pros}.\nОтчёт сохранён в директории программы.')
        msg.setWindowTitle("Отчёт готов.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()

        return None

    def form_report_all(self):
        logging.debug('Формируется отчёт за весь период работы программы.')
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        pros_list = supportive_vestments.sql_get_deposits_all_time(local_vars.DB_CURSOR)
        cons_list = supportive_vestments.sql_get_losses_all_time(local_vars.DB_CURSOR)
        with open(file=f'.\\reports\\report_at_{datetime.datetime.now().date()}.txt', mode='w',
                  encoding='utf-8-sig') as rep:
            rep.write('=' * 70 + '\n')
            rep.write('Расходы за всё время:' + '\n')
            rep.write('=' * 70 + '\n')
            rep.write('Категория'.ljust(50) + 'Цена'.ljust(16) + '\n')
            for attr in cons_list:
                rep.write(f'{str(attr[0]).ljust(50)}{str(attr[1]).ljust(2)}' + '\n')
            rep.write('\n')
            rep.write('=' * 70 + '\n')
            rep.write('Доходы за всё время:' + '\n')
            rep.write('=' * 70 + '\n')
            rep.write('Категория'.ljust(50) + 'Цена'.ljust(16) + '\n')
            for attr in pros_list:
                rep.write(f'{str(attr[0]).ljust(50)}{str(attr[1]).ljust(2)}' + '\n')
            rep.flush()
        pros = sum([float(attr[1]) for attr in pros_list])
        cons = sum([float(attr[1]) for attr in cons_list])
        msg.setText(
            f'Траты за всё время: {cons} \nПополнения за всё время: {pros}.\nОтчёт сохранён в директории программы.')
        msg.setWindowTitle("Отчёт готов.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()

        return None

    def call_info(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("Спасибо за пользование программой!\nИнструкция в руководстве.")
        msg.setWindowTitle("Справка.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()
        return None

    def call_export_form(self):
        self.reports.show()

    def add_new_rec(self):
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

