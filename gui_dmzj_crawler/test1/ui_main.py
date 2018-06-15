from PyQt5 import QtCore, QtWidgets


class UIForm(QtWidgets.QWidget):
    def __init__(self):
        super(UIForm, self).__init__()

        self.search_edit = QtWidgets.QLineEdit(self)
        self.search_button = QtWidgets.QPushButton(self)

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.num_tab = 0

        self.search_tab = QtWidgets.QWidget()
        self.search_scrollArea = QtWidgets.QScrollArea(self.search_tab)
        self.search_scrollAreaWidgetContents = QtWidgets.QWidget()

        self.dl_tab = QtWidgets.QWidget()
        self.dl_scrollArea = QtWidgets.QScrollArea(self.dl_tab)

        self.dl_scrollAreaWidgetContents = QtWidgets.QWidget()

        self.tabWidget.tabCloseRequested.connect(self.tab_remove)

        self.setup_ui()

    def setup_ui(self):
        form_width = 800
        form_height = 600
        self.setGeometry(300, 300, form_width, form_height)
        self.setFixedSize(form_width, form_height)
        self.setWindowTitle("动漫之家漫画下载 BY ssj")

        self.setObjectName("form")
        self.search_edit.setObjectName("search_edit")
        self.search_button.setObjectName("search_button")
        self.tabWidget.setObjectName("tabWidget")
        self.search_tab.setObjectName("search_tab")
        self.dl_tab.setObjectName("dl_tab")
        self.search_scrollArea.setObjectName("search_scrollArea")
        self.search_scrollAreaWidgetContents.setObjectName("search_scrollAreaWidgetContents")
        self.dl_scrollArea.setObjectName("dl_scrollArea")
        self.dl_scrollAreaWidgetContents.setObjectName("dl_scrollAreaWidgetContents")

        self.search_edit.setGeometry(13, 16, 710, 21)
        self.search_button.setGeometry(730, 12, 68, 32)
        self.tabWidget.setGeometry(12, 55, 780, 550)
        self.search_scrollArea.setGeometry(20, 12, 740, 494)
        self.dl_scrollArea.setGeometry(20, 12, 740, 494)
        self.search_scrollAreaWidgetContents.setGeometry(0, 0, 740, 494)
        self.dl_scrollAreaWidgetContents.setGeometry(0, 0, 740, 494)

        self.search_button.setText("搜索")

        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(False)

        self.search_scrollArea.setWidget(self.search_scrollAreaWidgetContents)
        self.search_scrollArea.setWidgetResizable(True)
        self.tabWidget.addTab(self.search_tab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.search_tab), "搜索结果")

        # self.dl_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 696, 316))
        self.dl_scrollArea.setWidget(self.dl_scrollAreaWidgetContents)
        self.tabWidget.addTab(self.dl_tab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.dl_tab), "下载任务")
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.show()

    def tab_remove(self, index):
        """关闭标签页"""

        if index != 0 and index != self.num_tab + 1:
            self.tabWidget.removeTab(index)
            self.num_tab -= 1


