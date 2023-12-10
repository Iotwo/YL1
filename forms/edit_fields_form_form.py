from os import getcwd
from forms.edit_fields_form_ui import Ui_EditFieldsForm
from PyQt5.QtWidgets import QWidget
from scripts.variables import CONTROLS, LOCAL_VARS, CONFIG, ERRORS


class EditFieldsFormIf(QWidget, Ui_EditFieldsForm):
    def __init__(self, parent):
        super().__init__()
        super().setupUi(self,)
        super().retranslateUi(self,)
        self.parentForm = parent
        self.init_ui()

        self.load_operation_types()
        CONTROLS["env"].log.debug("Форма редактирования служебных полей приложения инициализирована.")

        return None

    def __new__(cls, *args, **kwargs) -> object:
        instance = super().__new__(cls)
        instance.selected_op = None
        CONTROLS["env"].log.debug(f"Создан экземпляр #{id(instance)}-{type(instance)}")
        
        return instance
    

    def init_ui(self) -> None:
        self.operations_listWidget.itemClicked.connect(self.set_selected_operation)
        self.op_categories_listWidget.itemClicked.connect(self.load_categories_of_optype)
        #self.add_new_cat_btn.clicked.connect()
        #self.rm_selected_cat_btn.clicked.connect()
        #self.exit_btn.clicked.connect()
        return None

    def load_categories_of_optype(self, op_value) -> None:
        self.op_categories_listWidget.clear()
        rows = CONTROLS["env"].call_select_cats_of_op(f"{getcwd()}\\sql\\get_cats_of_operation.sql", self.selected_op)
        for row in rows:
            self.op_categories_listWidget.addItem(QListWidgetItem(row[0]))
        return None

    def load_operation_types(self) -> None:
        self.operations_listWidget.clear()
        rows = CONTROLS["env"].call_sql_select_cmd(f"{getcwd()}\\sql\\get_all_operations.sql")
        for row in rows:
            self.operations_listWidget.addItem(QListWidgetItem(row[0]))
        return None
    
    def set_selected_operation(self, selectedItem) -> None:
        self.selected_op = op_value.text()
        return None
