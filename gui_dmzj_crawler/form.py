# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets, uic
import os, requests, zipfile
from selenium import webdriver
from lxml import etree

'''主要问题出现在search函数上'''

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        #Form.setFixedSize(QtWidgets.QDesktopWidget.)
        self.gridLayout_4 = QtWidgets.QGridLayout(Form)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.search_edit = QtWidgets.QLineEdit(Form)
        self.search_edit.setObjectName("search_edit")
        self.gridLayout.addWidget(self.search_edit, 0, 0, 1, 1)

        self.search_buttom = QtWidgets.QPushButton(Form)
        self.search_buttom.setObjectName("search_buttom")
        self.gridLayout.addWidget(self.search_buttom, 0, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.search_buttom.clicked.connect(self.search)

        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.search_tab = QtWidgets.QWidget()
        self.search_tab.setObjectName("search_tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.search_tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.search_scrollArea = QtWidgets.QScrollArea(self.search_tab)
        self.search_scrollArea.setObjectName("search_scrollArea")
        self.search_scrollAreaWidgetContents = QtWidgets.QWidget()
        #self.search_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 2000, 2000))
        self.search_scrollAreaWidgetContents.setObjectName("search_scrollAreaWidgetContents")
        self.search_scrollArea.setWidget(self.search_scrollAreaWidgetContents)
        self.search_scrollArea.setWidgetResizable(True)
        self.gridLayout_2.addWidget(self.search_scrollArea, 0, 0, 1, 1)
        self.tabWidget.addTab(self.search_tab, "")

        self.down_tab = QtWidgets.QWidget()
        self.down_tab.setObjectName("down_tab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.down_tab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.down_scrollArea = QtWidgets.QScrollArea(self.down_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.down_scrollArea.sizePolicy().hasHeightForWidth())
        self.down_scrollArea.setSizePolicy(sizePolicy)
        self.down_scrollArea.setWidgetResizable(True)
        self.down_scrollArea.setObjectName("down_scrollArea")
        self.down_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.down_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 696, 316))
        self.down_scrollAreaWidgetContents.setObjectName("down_scrollAreaWidgetContents")
        self.down_scrollArea.setWidget(self.down_scrollAreaWidgetContents)

        self.gridLayout_3.addWidget(self.down_scrollArea, 0, 0, 1, 1)
        self.tabWidget.addTab(self.down_tab, "")
        self.gridLayout_4.addWidget(self.tabWidget, 1, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def search(self):
        '''目前发现的问题：进行新的一次搜索后，之前的搜索结果还在，新的搜索结果覆盖在上面'''

        _translate = QtCore.QCoreApplication.translate
        url_search = 'https://www.dmzj.com/dynamic/o_search/index/' + self.search_edit.text()
        result_search = requests.get(url_search)
        if '很遗憾，您搜索的内容暂时没有找到。' in result_search.text:
            self.nosearch_label = QtWidgets.QLabel(self.search_scrollAreaWidgetContents)
            self.nosearch_label.setGeometry(QtCore.QRect(50, 20, 500, 140))
            self.nosearch_label.setTextFormat(QtCore.Qt.AutoText)
            self.nosearch_label.setAlignment(QtCore.Qt.AlignCenter)
            self.nosearch_label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:24pt;\">很遗憾，您搜索的内容暂时没有找到。</span></p></body></html>"))
            self.gridLayout_2.addWidget(self.nosearch_label, 0, 0, 1, 1)
            self.nosearch_label.show()

        else:
            tree_search = etree.HTML(result_search.text)
            page_search = tree_search.xpath(
                '//div[@class="bottom_page page"]/a[text()!="上一页"][text()!="下一页"]/text()')
            y = 10
            i_comic_p = 0
            for self.i_page_search in range(0, len(page_search)):
                result_search = requests.get(url_search + '/' + page_search[self.i_page_search])
                tree_search = etree.HTML(result_search.text)
                page_search = tree_search.xpath(
                    '//div[@class="bottom_page page"]/a[text()!="上一页"][text()!="下一页"]/text()')
                self.title_search = tree_search.xpath('//ul[@class="update_con autoHeight"]/li/a/@title')
                self.latest_search = tree_search.xpath('//p[@class="newPage"]/text()')
                self.link_search = tree_search.xpath('//ul[@class="update_con autoHeight"]/li/a/@href')
                self.title_search_label = []

                for self.i_comic in range(0, len(self.title_search)):
                    if self.i_comic in range(0, len(self.title_search), 4):
                        x = 10
                    elif self.i_comic in range(1, len(self.title_search), 4):
                        x = 290
                    elif self.i_comic in range(2, len(self.title_search), 4):
                        x = 570
                    elif self.i_comic in range(3, len(self.title_search), 4):
                        x = 850
                    self.title_search_label.append(QtWidgets.QLabel(self.search_scrollAreaWidgetContents))
                    self.title_search_label[self.i_comic].setGeometry(QtCore.QRect(x, y, 270, 20))
                    self.title_search_label[self.i_comic].setFrameShape(QtWidgets.QFrame.Box)
                    self.title_search_label[self.i_comic].setFrameShadow(QtWidgets.QFrame.Raised)
                    text_search_label = '<html><head/><body><p><span style=" color:#0000ff;">' + str(i_comic_p + (self.i_comic + 1)) + '   ' + self.title_search[self.i_comic] + '</span></p></body></html>'
                    self.title_search_label[self.i_comic].setText(_translate('Form', text_search_label))
                    self.title_search_label[self.i_comic].show()
                    self.title_search_label[self.i_comic].mousePressEvent = self.comic()
                    if self.i_comic in range(3, len(self.title_search), 4):
                        y = y + 30
                i_comic_p = i_comic_p + self.i_comic
                self.search_scrollAreaWidgetContents.setFixedHeight(y + 30)

    def comic(self):
        '''目前发现的问题：无法检测点击哪个标签，也就无法获取相应的漫画信息'''

        pass



    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "动漫之家漫画下载工具"))
        self.search_buttom.setText(_translate("Form", "搜索"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.search_tab), _translate("Form", "搜索结果"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.down_tab), _translate("Form", "下载页面"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.showMaximized()
    sys.exit(app.exec_())

