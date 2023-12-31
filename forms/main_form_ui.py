# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Project\YL1\design\MainForm_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.setWindowModality(QtCore.Qt.NonModal)
        MainForm.setEnabled(True)
        MainForm.resize(916, 582)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainForm.sizePolicy().hasHeightForWidth())
        MainForm.setSizePolicy(sizePolicy)
        MainForm.setMinimumSize(QtCore.QSize(910, 570))
        MainForm.setMaximumSize(QtCore.QSize(9999999, 9999999))
        MainForm.setFocusPolicy(QtCore.Qt.TabFocus)
        MainForm.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        MainForm.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainForm)
        self.centralwidget.setMinimumSize(QtCore.QSize(910, 530))
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 908, 510))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.main_hLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.main_hLayout.setContentsMargins(0, 0, 0, 0)
        self.main_hLayout.setSpacing(3)
        self.main_hLayout.setObjectName("main_hLayout")
        self.backlog_tableWidget = QtWidgets.QTableWidget(self.horizontalLayoutWidget)
        self.backlog_tableWidget.setMinimumSize(QtCore.QSize(640, 480))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.backlog_tableWidget.setFont(font)
        self.backlog_tableWidget.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.backlog_tableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.backlog_tableWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.backlog_tableWidget.setFrameShadow(QtWidgets.QFrame.Raised)
        self.backlog_tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.backlog_tableWidget.setProperty("showDropIndicator", False)
        self.backlog_tableWidget.setDragDropOverwriteMode(False)
        self.backlog_tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.backlog_tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.backlog_tableWidget.setTextElideMode(QtCore.Qt.ElideRight)
        self.backlog_tableWidget.setGridStyle(QtCore.Qt.DashLine)
        self.backlog_tableWidget.setColumnCount(6)
        self.backlog_tableWidget.setObjectName("backlog_tableWidget")
        self.backlog_tableWidget.setRowCount(0)
        self.main_hLayout.addWidget(self.backlog_tableWidget)
        self.interface_vLayout = QtWidgets.QVBoxLayout()
        self.interface_vLayout.setSpacing(3)
        self.interface_vLayout.setObjectName("interface_vLayout")
        self.categories_vLayout = QtWidgets.QVBoxLayout()
        self.categories_vLayout.setSpacing(3)
        self.categories_vLayout.setObjectName("categories_vLayout")
        self.optype_hint_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.optype_hint_label.setFont(font)
        self.optype_hint_label.setAlignment(QtCore.Qt.AlignCenter)
        self.optype_hint_label.setObjectName("optype_hint_label")
        self.categories_vLayout.addWidget(self.optype_hint_label)
        self.opSelection_cmbBox = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.opSelection_cmbBox.setMinimumSize(QtCore.QSize(180, 30))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        font.setBold(True)
        self.opSelection_cmbBox.setFont(font)
        self.opSelection_cmbBox.setObjectName("opSelection_cmbBox")
        self.categories_vLayout.addWidget(self.opSelection_cmbBox)
        self.cat_hint_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.cat_hint_label.setFont(font)
        self.cat_hint_label.setAlignment(QtCore.Qt.AlignCenter)
        self.cat_hint_label.setObjectName("cat_hint_label")
        self.categories_vLayout.addWidget(self.cat_hint_label)
        self.catSelection_list = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        self.catSelection_list.setMinimumSize(QtCore.QSize(180, 120))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        font.setBold(True)
        self.catSelection_list.setFont(font)
        self.catSelection_list.setObjectName("catSelection_list")
        self.categories_vLayout.addWidget(self.catSelection_list)
        self.interface_vLayout.addLayout(self.categories_vLayout)
        self.amount_vLayout = QtWidgets.QVBoxLayout()
        self.amount_vLayout.setSpacing(3)
        self.amount_vLayout.setObjectName("amount_vLayout")
        self.amount_lineEd = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.amount_lineEd.setMinimumSize(QtCore.QSize(180, 30))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        font.setBold(True)
        self.amount_lineEd.setFont(font)
        self.amount_lineEd.setInputMethodHints(QtCore.Qt.ImhDigitsOnly|QtCore.Qt.ImhPreferNumbers)
        self.amount_lineEd.setInputMask("")
        self.amount_lineEd.setMaxLength(16)
        self.amount_lineEd.setFrame(True)
        self.amount_lineEd.setClearButtonEnabled(False)
        self.amount_lineEd.setObjectName("amount_lineEd")
        self.amount_vLayout.addWidget(self.amount_lineEd)
        self.predefinedAmt_gLayout = QtWidgets.QGridLayout()
        self.predefinedAmt_gLayout.setSpacing(3)
        self.predefinedAmt_gLayout.setObjectName("predefinedAmt_gLayout")
        self.defVal1_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.defVal1_btn.setMinimumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        font.setBold(True)
        self.defVal1_btn.setFont(font)
        self.defVal1_btn.setObjectName("defVal1_btn")
        self.predefinedAmt_gLayout.addWidget(self.defVal1_btn, 0, 0, 1, 1)
        self.defVal2_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.defVal2_btn.setMinimumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        font.setBold(True)
        self.defVal2_btn.setFont(font)
        self.defVal2_btn.setObjectName("defVal2_btn")
        self.predefinedAmt_gLayout.addWidget(self.defVal2_btn, 0, 1, 1, 1)
        self.defVal6_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.defVal6_btn.setMinimumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        font.setBold(True)
        self.defVal6_btn.setFont(font)
        self.defVal6_btn.setObjectName("defVal6_btn")
        self.predefinedAmt_gLayout.addWidget(self.defVal6_btn, 4, 1, 1, 1)
        self.defVal3_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.defVal3_btn.setMinimumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        font.setBold(True)
        self.defVal3_btn.setFont(font)
        self.defVal3_btn.setObjectName("defVal3_btn")
        self.predefinedAmt_gLayout.addWidget(self.defVal3_btn, 2, 0, 1, 1)
        self.defVal4_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.defVal4_btn.setMinimumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        font.setBold(True)
        self.defVal4_btn.setFont(font)
        self.defVal4_btn.setObjectName("defVal4_btn")
        self.predefinedAmt_gLayout.addWidget(self.defVal4_btn, 2, 1, 1, 1)
        self.defVal5_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.defVal5_btn.setMinimumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Terminal")
        font.setPointSize(14)
        font.setBold(True)
        self.defVal5_btn.setFont(font)
        self.defVal5_btn.setObjectName("defVal5_btn")
        self.predefinedAmt_gLayout.addWidget(self.defVal5_btn, 4, 0, 1, 1)
        self.amount_vLayout.addLayout(self.predefinedAmt_gLayout)
        self.interface_vLayout.addLayout(self.amount_vLayout)
        self.action_hLayout = QtWidgets.QHBoxLayout()
        self.action_hLayout.setSpacing(3)
        self.action_hLayout.setObjectName("action_hLayout")
        self.clear_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.clear_btn.setMinimumSize(QtCore.QSize(60, 120))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        font.setBold(True)
        self.clear_btn.setFont(font)
        self.clear_btn.setObjectName("clear_btn")
        self.action_hLayout.addWidget(self.clear_btn)
        self.addRec_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.addRec_btn.setMinimumSize(QtCore.QSize(120, 120))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        font.setBold(True)
        self.addRec_btn.setFont(font)
        self.addRec_btn.setObjectName("addRec_btn")
        self.action_hLayout.addWidget(self.addRec_btn)
        self.interface_vLayout.addLayout(self.action_hLayout)
        self.main_hLayout.addLayout(self.interface_vLayout)
        MainForm.setCentralWidget(self.centralwidget)
        self.main_menu_bar = QtWidgets.QMenuBar(MainForm)
        self.main_menu_bar.setGeometry(QtCore.QRect(0, 0, 916, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_menu_bar.sizePolicy().hasHeightForWidth())
        self.main_menu_bar.setSizePolicy(sizePolicy)
        self.main_menu_bar.setMinimumSize(QtCore.QSize(600, 30))
        self.main_menu_bar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.main_menu_bar.setObjectName("main_menu_bar")
        self.main_menu_tables_btn = QtWidgets.QMenu(self.main_menu_bar)
        self.main_menu_tables_btn.setGeometry(QtCore.QRect(269, 127, 240, 94))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_menu_tables_btn.sizePolicy().hasHeightForWidth())
        self.main_menu_tables_btn.setSizePolicy(sizePolicy)
        self.main_menu_tables_btn.setMinimumSize(QtCore.QSize(240, 35))
        self.main_menu_tables_btn.setMaximumSize(QtCore.QSize(240, 100))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setKerning(False)
        self.main_menu_tables_btn.setFont(font)
        self.main_menu_tables_btn.setObjectName("main_menu_tables_btn")
        self.main_menu_reports_btn = QtWidgets.QMenu(self.main_menu_bar)
        self.main_menu_reports_btn.setMinimumSize(QtCore.QSize(0, 35))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.main_menu_reports_btn.setFont(font)
        self.main_menu_reports_btn.setObjectName("main_menu_reports_btn")
        self.menu_actions = QtWidgets.QMenu(self.main_menu_bar)
        self.menu_actions.setMinimumSize(QtCore.QSize(0, 35))
        self.menu_actions.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.menu_actions.setFont(font)
        self.menu_actions.setObjectName("menu_actions")
        MainForm.setMenuBar(self.main_menu_bar)
        self.app_status_bar = QtWidgets.QStatusBar(MainForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.app_status_bar.sizePolicy().hasHeightForWidth())
        self.app_status_bar.setSizePolicy(sizePolicy)
        self.app_status_bar.setMinimumSize(QtCore.QSize(600, 20))
        self.app_status_bar.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setKerning(False)
        self.app_status_bar.setFont(font)
        self.app_status_bar.setObjectName("app_status_bar")
        MainForm.setStatusBar(self.app_status_bar)
        self.menu_edit_fields_btn = QtWidgets.QAction(MainForm)
        self.menu_edit_fields_btn.setObjectName("menu_edit_fields_btn")
        self.menu_edit_ops_btn = QtWidgets.QAction(MainForm)
        self.menu_edit_ops_btn.setObjectName("menu_edit_ops_btn")
        self.menu_call_info_btn = QtWidgets.QAction(MainForm)
        self.menu_call_info_btn.setObjectName("menu_call_info_btn")
        self.menu_report_today_btn = QtWidgets.QAction(MainForm)
        self.menu_report_today_btn.setObjectName("menu_report_today_btn")
        self.menu_report_last_week_btn = QtWidgets.QAction(MainForm)
        self.menu_report_last_week_btn.setObjectName("menu_report_last_week_btn")
        self.menu_report_last_month_btn = QtWidgets.QAction(MainForm)
        self.menu_report_last_month_btn.setObjectName("menu_report_last_month_btn")
        self.menu_report_all_time_btn = QtWidgets.QAction(MainForm)
        self.menu_report_all_time_btn.setObjectName("menu_report_all_time_btn")
        self.menu_edit_rec_btn = QtWidgets.QAction(MainForm)
        self.menu_edit_rec_btn.setObjectName("menu_edit_rec_btn")
        self.menu_import_btn = QtWidgets.QAction(MainForm)
        self.menu_import_btn.setObjectName("menu_import_btn")
        self.menu_settings_btn = QtWidgets.QAction(MainForm)
        self.menu_settings_btn.setObjectName("menu_settings_btn")
        self.main_menu_tables_btn.addAction(self.menu_edit_fields_btn)
        self.main_menu_tables_btn.addAction(self.menu_call_info_btn)
        self.main_menu_reports_btn.addAction(self.menu_report_today_btn)
        self.main_menu_reports_btn.addAction(self.menu_report_last_week_btn)
        self.main_menu_reports_btn.addAction(self.menu_report_last_month_btn)
        self.main_menu_reports_btn.addAction(self.menu_report_all_time_btn)
        self.menu_actions.addAction(self.menu_import_btn)
        self.menu_actions.addAction(self.menu_settings_btn)
        self.main_menu_bar.addAction(self.main_menu_tables_btn.menuAction())
        self.main_menu_bar.addAction(self.main_menu_reports_btn.menuAction())
        self.main_menu_bar.addAction(self.menu_actions.menuAction())

        self.retranslateUi(MainForm)
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "Учёт расходов и доходов"))
        self.backlog_tableWidget.setSortingEnabled(True)
        self.optype_hint_label.setText(_translate("MainForm", "Тип операции"))
        self.opSelection_cmbBox.setToolTip(_translate("MainForm", "Выберите операцию"))
        self.cat_hint_label.setText(_translate("MainForm", "Категории"))
        self.catSelection_list.setToolTip(_translate("MainForm", "Выберите категории"))
        self.amount_lineEd.setToolTip(_translate("MainForm", "Введите сумму"))
        self.defVal1_btn.setToolTip(_translate("MainForm", "Преднастроенная сумма"))
        self.defVal1_btn.setText(_translate("MainForm", "150"))
        self.defVal2_btn.setToolTip(_translate("MainForm", "Преднастроенная сумма"))
        self.defVal2_btn.setText(_translate("MainForm", "300"))
        self.defVal6_btn.setToolTip(_translate("MainForm", "Преднастроенная сумма"))
        self.defVal6_btn.setText(_translate("MainForm", "5000"))
        self.defVal3_btn.setToolTip(_translate("MainForm", "Преднастроенная сумма"))
        self.defVal3_btn.setText(_translate("MainForm", "500"))
        self.defVal4_btn.setToolTip(_translate("MainForm", "Преднастроенная сумма"))
        self.defVal4_btn.setText(_translate("MainForm", "1000"))
        self.defVal5_btn.setToolTip(_translate("MainForm", "Преднастроенная сумма"))
        self.defVal5_btn.setText(_translate("MainForm", "1500"))
        self.clear_btn.setText(_translate("MainForm", "Отменить\n"
" --- \n"
"Удалить"))
        self.addRec_btn.setText(_translate("MainForm", "Добавить\n"
"---\n"
"Применить"))
        self.main_menu_tables_btn.setTitle(_translate("MainForm", "Меню"))
        self.main_menu_reports_btn.setTitle(_translate("MainForm", "Отчёты"))
        self.menu_actions.setTitle(_translate("MainForm", "Действия"))
        self.menu_edit_fields_btn.setText(_translate("MainForm", "Изменить служебные"))
        self.menu_edit_ops_btn.setText(_translate("MainForm", "Изменить операции"))
        self.menu_edit_ops_btn.setIconText(_translate("MainForm", "Отчёты..."))
        self.menu_edit_ops_btn.setToolTip(_translate("MainForm", "Отчёты..."))
        self.menu_call_info_btn.setText(_translate("MainForm", "Справка"))
        self.menu_report_today_btn.setText(_translate("MainForm", "За сегодня"))
        self.menu_report_last_week_btn.setText(_translate("MainForm", "За неделю"))
        self.menu_report_last_month_btn.setText(_translate("MainForm", "За месяц"))
        self.menu_report_all_time_btn.setText(_translate("MainForm", "За всё время"))
        self.menu_edit_rec_btn.setText(_translate("MainForm", "Редактор записей"))
        self.menu_import_btn.setText(_translate("MainForm", "Импорт данных"))
        self.menu_settings_btn.setText(_translate("MainForm", "Настройки"))
