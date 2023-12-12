from os import getcwd
from forms.edit_fields_form_ui import Ui_EditFieldsForm
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QMessageBox
from scripts.variables import CONTROLS, LOCAL_VARS, CONFIG, ERRORS


class EditFieldsFormIf(QWidget, Ui_EditFieldsForm):
    """
        
    """
    def __init__(self, parent):
        """
        DESCR: Initiate new object exemplar
        """
        super().__init__()
        super().setupUi(self,)
        super().retranslateUi(self,)
        self.parentForm = parent
        self.init_ui()

        self.load_operation_types()
        CONTROLS["env"].log.debug("Форма редактирования служебных полей приложения инициализирована.")

        return None

    def __new__(cls, *args, **kwargs) -> object:
        """
        DESCR: Create new object exemplar
        """
        instance = super().__new__(cls)
        instance.selected_op = None
        instance.selected_cat = None
        CONTROLS["env"].log.debug(f"Создан экземпляр #{id(instance)}-{type(instance)}")
        
        return instance

    def add_new_category_for_optype(self, operation: str) -> None:
        """
        DESCR: Insert new category of operations into DB
        """
        CONTROLS["env"].log.debug(f"Начат процесс добавления записи, проверка заполненности всех атрибутов...")
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText("Не хватает данных\n для вставки новой записи!")
        msg.setWindowTitle("Вставка записи.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        result = None

        if self.new_cat_txtEdit.text() == "":
            retval = msg.exec()
            CONTROLS["env"].log.debug("Вставка записи не произведена, не хватает данных.")
            return result
        if self.selected_op is None:
            retval = msg.exec()
            CONTROLS["env"].log.debug("Вставка записи не произведена, не хватает данных.")
            return result
        ins_data = [self.new_cat_txtEdit.text(), self.selected_op]
        CONTROLS["env"].log.info("Вставка новой записи...")
        CONTROLS["env"].log.debug(f"Данные для вставки: {ins_data}")
        LOCAL_VARS["last_err_code"] = CONTROLS["env"].call_insert_new_rec(f"{getcwd()}\\sql\\insert_value_into_categories.sql", "Categories", ins_data)
        if LOCAL_VARS["last_err_code"] == 0:
            CONTROLS["env"].log.info("Добавлена запись.")
        else:
            CONTROLS["env"].log.warn("Не удалось добавить запись.")

        self.load_categories_of_optype(self.selected_op)
        self.parentForm.load_categories_of_optype(self.selected_op)
        return None
    
    def exit_form_and_hide(self) -> None:
        """
        DESCR: Decline changes and leave form hidden.
        """
        self.new_cat_txtEdit.setText("")
        self.selected_op = None
        self.selected_cat = None
        self.op_categories_list.clear()
        self.operations_list.setCurrentRow(-1)
        CONTROLS["env"].log.debug(f"Выход из формы {self} и сокрытие формы.")
        self.hide()
        return None

    def init_ui(self) -> None:
        """
        DESCR: Initiate user interface.
        """
        self.operations_list.itemClicked.connect(self.load_categories_of_optype)
        self.op_categories_list.itemClicked.connect(self.set_selected_cat)
        self.add_new_cat_btn.clicked.connect(self.add_new_category_for_optype)
        self.rm_selected_cat_btn.clicked.connect(self.remove_selected_category)
        self.exit_btn.clicked.connect(self.exit_form_and_hide)
        return None
    
    def load_categories_of_optype(self, selectedItem) -> None:
        """
        DESCR: Load categories of exact operation from DB.
        """
        si = selectedItem
        si_t = "" if selectedItem is None or isinstance(selectedItem, str) is True else selectedItem.text()
        CONTROLS["env"].log.debug(f"Выбран элемент {si}, значение - {si_t}")
        self.selected_op = selectedItem if selectedItem is None or isinstance(selectedItem, str) is True else selectedItem.text()
        self.op_categories_list.clear()
        rows = CONTROLS["env"].call_select_cats_of_op(f"{getcwd()}\\sql\\get_cats_of_operation.sql", self.selected_op)
        for row in rows:
            self.op_categories_list.addItem(QListWidgetItem(row[0]))
        return None

    def load_operation_types(self) -> None:
        """
        DESCR: Load all operation types from DB.
        """
        self.operations_list.clear()
        rows = CONTROLS["env"].call_sql_select_cmd(f"{getcwd()}\\sql\\get_all_operations.sql")
        for row in rows:
            self.operations_list.addItem(QListWidgetItem(row[0]))
        return None

    def remove_selected_category(self, selectedCategory) -> None:
        """
        DESCR: Remove selected category from DB.
        """
        result = None
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText("Не выбрана запись для удаления!")
        msg.setWindowTitle("Удаление записи.")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        if self.op_categories_list.currentRow() <= 0:
            retval = msg.exec()
            CONTROLS["env"].log.debug("Удаление записи не произведено, запись не выбрана.")
            return result
        CONTROLS["env"].log.info("Попытка удалить запись...")
        CONTROLS["env"].log.debug(f"Удаляемая запись: {self.selected_cat}")
        LOCAL_VARS["last_err_code"] = CONTROLS["env"].call_delete_rec_command(f"{getcwd()}\\sql\\delete_record_from_table.sql",
                                                                              "Categories", "cat_name", '\'' + self.selected_cat + '\'')
        if LOCAL_VARS["last_err_code"] == 0:
            CONTROLS["env"].log.info("Запись удалена.")
            self.op_categories_list.setCurrentRow(-1)
        else:
            CONTROLS["env"].log.error("Во время удаления записи возникла ошибка.")
        self.load_categories_of_optype(self.selected_op)
        self.parentForm.load_categories_of_optype(self.selected_op)
        return None
    
    def set_selected_cat(self, selectedItem) -> None:
        """
        DESCR: On click collect all data from clicked ROW
        """
        si = selectedItem
        si_t = "" if selectedItem is None or isinstance(selectedItem, str) is True else selectedItem.text()
        CONTROLS["env"].log.debug(f"Выбран элемент {si}, значение - {si_t}")
        self.selected_cat = selectedItem if selectedItem is None or isinstance(selectedItem, str) is True else selectedItem.text()
        return None

    
