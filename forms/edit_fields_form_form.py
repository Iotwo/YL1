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

        CONTROLS["env"].log.debug("Форма редактирования служебных полей приложения инициализирована.")

        return None

    def __new__(cls, *args, **kwargs) -> object:
        instance = super().__new__(cls)
        CONTROLS["env"].log.debug(f"Создан экземпляр #{id(instance)}-{type(instance)}")
        
        return instance
    

    def init_ui(self) -> None:

        return None

    def load_categories_of_optype(self, cmb_index) -> None:
        rows = CONTROLS["env"].call_select_cats_of_op(f"{getcwd()}\\sql\\get_cats_of_operation.sql", self.opSelection_cmbBox.currentText())
        self.cats_table.clearContents()
        self.cats_table.setRowCount(len(rows))
        rows = [tuple(map(str, [elem for elem in row])) for row in rows]
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                self.cats_table.setItem(i, j, QTableWidgetItem(rows[i][j]))
        return None

    def load_operation_types(self) -> None:
        rows = CONTROLS["env"].call_sql_select_cmd(f"{getcwd()}\\sql\\get_all_operations.sql")
        self.ops_table.clearContents()
        self.ops_table.setRowCount(len(rows))
        rows = [tuple(map(str, [elem for elem in row])) for row in rows]
        for i in range(len(rows)):
            for j in range(len(rows[i])):
                self.ops_table.setItem(i, j, QTableWidgetItem(rows[i][j]))
                
        return None
