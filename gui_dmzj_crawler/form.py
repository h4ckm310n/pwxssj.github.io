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
import functools
from multiprocessing import Pool, Queue
import aiohttp, asyncio

'''问题：标签页关不掉，执行爬虫语句时窗口没有响应'''


class Ui_Form(object):
    def setupUi(self, Form):
        '''窗口初始状态'''

        Form.setObjectName("Form")
        Form.isMaximized()
        self.gridLayout_Form = QtWidgets.QGridLayout(Form)
        self.gridLayout_Form.setObjectName("gridLayout_Form")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.search_edit = QtWidgets.QLineEdit(Form)
        self.search_edit.setObjectName("search_edit")
        self.gridLayout.addWidget(self.search_edit, 0, 0, 1, 1)
        self.search_buttom = QtWidgets.QPushButton(Form)
        self.search_buttom.setObjectName("search_buttom")
        self.gridLayout.addWidget(self.search_buttom, 0, 1, 1, 1)
        self.gridLayout_Form.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.search_buttom.clicked.connect(self.search)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.tabCloseRequested.connect(self.tab_remove)

        self.search_tab = QtWidgets.QWidget()
        self.search_tab.setObjectName("search_tab")
        self.gridLayout_search = QtWidgets.QGridLayout(self.search_tab)
        self.gridLayout_search.setObjectName("gridLayout_search")
        self.search_scrollArea = QtWidgets.QScrollArea(self.search_tab)
        self.search_scrollArea.setObjectName("search_scrollArea")
        self.search_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.search_scrollAreaWidgetContents.setObjectName("search_scrollAreaWidgetContents")
        self.search_scrollArea.setWidget(self.search_scrollAreaWidgetContents)
        self.search_scrollArea.setWidgetResizable(True)
        self.gridLayout_search.addWidget(self.search_scrollArea, 0, 0, 1, 1)
        self.tabWidget.addTab(self.search_tab, "")
        self.down_tab = QtWidgets.QWidget()
        self.down_tab.setObjectName("down_tab")
        self.gridLayout_down = QtWidgets.QGridLayout(self.down_tab)
        self.gridLayout_down.setObjectName("gridLayout_down")
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

        self.gridLayout_down.addWidget(self.down_scrollArea, 0, 0, 1, 1)
        self.tabWidget.addTab(self.down_tab, "")
        self.gridLayout_Form.addWidget(self.tabWidget, 1, 0, 1, 1)
        
        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def search(self):
        '''搜索漫画'''

        if('nofound_label' in dir(self)):
            if self.nofound_label != None:
                self.gridLayout_search.removeWidget(self.nofound_label)
                self.nofound_label.deleteLater()
                self.nofound_label = None
        if('title_search_label' in dir(self)):
            for i_t_label in self.search_scrollAreaWidgetContents.children():
                i_t_label.deleteLater()
                i_t_label = None

        _translate = QtCore.QCoreApplication.translate
        url_search = 'https://www.dmzj.com/dynamic/o_search/index/' + '闪电侠'
        result_search = requests.get(url_search)
        if '很遗憾，您搜索的内容暂时没有找到。' in result_search.text:
            self.nofound_label = QtWidgets.QLabel(self.search_scrollAreaWidgetContents)
            self.nofound_label.setGeometry(QtCore.QRect(50, 20, 500, 140))
            self.nofound_label.setTextFormat(QtCore.Qt.AutoText)
            self.nofound_label.setAlignment(QtCore.Qt.AlignCenter)
            self.nofound_label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:24pt;\">很遗憾，您搜索的内容暂时没有找到。</span></p></body></html>"))
            self.gridLayout_search.addWidget(self.nofound_label, 0, 0, 1, 1)
            self.nofound_label.show()

        else:
            self.search_scrollArea.setStyleSheet('.QWidget {background-color: rgb(255, 255, 255);}')
            tree_search = etree.HTML(result_search.text)
            page_search = tree_search.xpath(
                '//div[@class="bottom_page page"]/a[text()!="上一页"][text()!="下一页"]/text()')
            y = 10
            self.i_comic_sum = 0
            self.title_search_label = []
            self.title_search_sum = []
            self.latest_search_sum = []
            self.link_search_sum = []


            for i_page_search in range(0, len(page_search)):
                result_search = requests.get(url_search + '/' + page_search[i_page_search])
                tree_search = etree.HTML(result_search.text)
                page_search = tree_search.xpath(
                    '//div[@class="bottom_page page"]/a[text()!="上一页"][text()!="下一页"]/text()')
                self.title_search = tree_search.xpath('//ul[@class="update_con autoHeight"]/li/a/@title')
                self.latest_search = tree_search.xpath('//p[@class="newPage"]/text()')
                self.link_search = tree_search.xpath('//ul[@class="update_con autoHeight"]/li/a/@href')


                for i_comic in range(0, len(self.title_search)):
                    self.title_search_sum.append(self.title_search[i_comic])
                    self.latest_search_sum.append(self.latest_search[i_comic])
                    self.link_search_sum.append(self.link_search[i_comic])

                    if i_comic in range(0, len(self.title_search), 4):
                        x = 10
                    elif i_comic in range(1, len(self.title_search), 4):
                        x = 290
                    elif i_comic in range(2, len(self.title_search), 4):
                        x = 570
                    elif i_comic in range(3, len(self.title_search), 4):
                        x = 850
                    self.title_search_label.append(QtWidgets.QLabel(self.search_scrollAreaWidgetContents))
                    self.title_search_label[self.i_comic_sum].setGeometry(QtCore.QRect(x, y, 270, 20))
                    self.title_search_label[self.i_comic_sum].setFrameShape(QtWidgets.QFrame.Box)
                    self.title_search_label[self.i_comic_sum].setFrameShadow(QtWidgets.QFrame.Raised)
                    text_search_label = '<html><head/><body><p><span style=" color:#0000ff;">' + str(self.i_comic_sum + 1) + '   ' + self.title_search_sum[self.i_comic_sum] + '</span></p></body></html>'
                    self.title_search_label[self.i_comic_sum].setText(_translate('Form', text_search_label))
                    self.title_search_label[self.i_comic_sum].show()
                    self.title_search_label[self.i_comic_sum].mousePressEvent = functools.partial(self.comic, source_object = self.title_search_label[self.i_comic_sum])
                    if i_comic in range(3, len(self.title_search), 4):
                        y = y + 30
                    self.i_comic_sum = self.i_comic_sum + 1
                self.search_scrollAreaWidgetContents.setFixedHeight(y + 30)


    def comic(self, event, source_object = None):

        '''漫画界面'''
        '''问题：'''

        _translate = QtCore.QCoreApplication.translate
        self.i_comic = int(source_object.text()[52:-25][0]) - 1

        self.comic_tab = QtWidgets.QWidget()
        self.gridLayout_comic = QtWidgets.QGridLayout(self.comic_tab)
        self.comic_frame = QtWidgets.QFrame()
        self.comic_frame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.comic_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.comic_frame.show()
        self.gridLayout_comic.addWidget(self.comic_frame, 0, 0, 1, 1)
        self.tabWidget.insertTab(1, self.comic_tab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.comic_tab), _translate("Form", self.title_search_sum[self.i_comic]))
        self.tabWidget.setCurrentWidget(self.comic_tab)
        response_comic = requests.get(self.link_search_sum[self.i_comic])
        if '4004.gif' in response_comic.text:
            self.noprovide_label = QtWidgets.QLabel(self.comic_frame)
            self.noprovide_label.setAlignment(QtCore.Qt.AlignCenter)
            self.noprovide_label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:24pt;\">因版权等原因暂停提供</span></p></body></html>"))
            self.noprovide_label.setGeometry(50, 20, 500, 140)
            self.gridLayout_comic.addWidget(self.noprovide_label, 0, 0, 1, 1)
            self.noprovide_label.show()
        else:
            self.volume_scrollArea = QtWidgets.QScrollArea(self.comic_frame)
            self.volume_scrollArea.setGeometry(620, 40, 621, 471)
            self.volume_scrollAreaWidgetContents = QtWidgets.QWidget()
            self.volume_scrollAreaWidgetContents.setFixedHeight(469)
            self.volume_scrollArea.setWidget(self.volume_scrollAreaWidgetContents)
            self.volume_scrollArea.setWidgetResizable(True)
            tree_comic = etree.HTML(response_comic.text)
            intro_comic = tree_comic.xpath('//div[@class="line_height_content"]/text()')
            cover_comic = tree_comic.xpath('//img[@id="cover_pic"]/@src')
            self.title_volume = tree_comic.xpath('//div[@class="cartoon_online_border"]/ul/li/a/text()')
            self.link_volume = tree_comic.xpath('//div[@class="cartoon_online_border"]/ul/li/a/@href')
            self.cover_label = QtWidgets.QLabel(self.comic_frame)
            self.cover_label.setGeometry(20, 90, 221, 301)
            self.cover_label.setAlignment(QtCore.Qt.AlignCenter)
            self.cover_label.setFrameShape(QtWidgets.QFrame.Box)
            self.cover_label.setFrameShadow(QtWidgets.QFrame.Plain)
            headers = {'Referer':self.link_search_sum[self.i_comic], 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
            get_cover = requests.get(cover_comic[0], headers = headers)
            cover_img = QtGui.QImage()
            cover_img.loadFromData(get_cover.content)
            self.cover_label.setPixmap(QtGui.QPixmap(cover_img).scaledToWidth(220))
            self.title_label = QtWidgets.QLabel(self.comic_frame)
            self.title_label.setGeometry(20, 40, 221, 41)
            self.title_label.setFrameShape(QtWidgets.QFrame.Box)
            self.title_label.setFrameShadow(QtWidgets.QFrame.Plain)
            self.title_label.setText(_translate("Form", '﻿<html><head/><body><p><span style=" font-size:14pt; font-weight:600; color:#0000ff;">' + self.title_search_sum[self.i_comic] + '</span></p></body></html>'))
            self.intro_label = QtWidgets.QLabel(self.comic_frame)
            self.intro_label.setGeometry(250, 90, 351, 301)
            self.intro_label.setAlignment(QtCore.Qt.AlignBaseline)
            self.intro_label.setWordWrap(True)
            self.intro_label.setFrameShape(QtWidgets.QFrame.Box)
            self.intro_label.setFrameShadow(QtWidgets.QFrame.Plain)
            self.intro_label.setText(_translate("Form", intro_comic[0].strip()))
            self.allselect_button = QtWidgets.QPushButton(self.comic_frame)
            self.allselect_button.setGeometry(400, 40, 100, 40)
            self.allselect_button.setText(_translate("Form", "全选"))
            self.download_button = QtWidgets.QPushButton(self.comic_frame)
            self.download_button.setGeometry(500, 40, 100, 40)
            self.download_button.setText(_translate("Form", "下载"))
            self.volume_checkbox = []
            i_list = 0
            for i_volume in range(0, len(self.title_volume)):
                x = 10 + 180 * i_list
                y = 10 + 30 * (i_volume % 15) * (i_list + 1)
                self.volume_checkbox.append(QtWidgets.QCheckBox(self.volume_scrollAreaWidgetContents))
                self.volume_checkbox[i_volume].setGeometry(x, y, 170, 20)
                self.volume_checkbox[i_volume].setText(_translate("Form", str(i_volume + 1) + ' ' + self.title_volume[i_volume]))
                self.volume_checkbox[i_volume].show()
                if i_volume != 0 and i_volume % 15 == 0:
                    i_list += 1
            self.num_check = 0
            self.allselect_button.clicked.connect(self.all_select)
            self.download_button.clicked.connect(self.download)
            self.cover_label.show()
            self.title_label.show()
            self.intro_label.show()
            self.allselect_button.show()
            self.download_button.show()
            self.volume_scrollArea.show()
            self.volume_scrollAreaWidgetContents.show()


    def tab_remove(self, index):
        tab = self.tabWidget.widget(index)
        #tab.deleteLater()
        self.tabWidget.removeTab(index)
        tab.close()
        tab.deleteLater()



    def all_select(self):
        '''点击全选按钮'''

        state_allcheck = 0
        for i_volume in range(0, len(self.title_volume)):
            if not self.volume_checkbox[i_volume].isChecked():
                state_allcheck = 0
                break
            if self.volume_checkbox[i_volume].isChecked():
                state_allcheck = 1
        if state_allcheck == 0:
            for i_volume in range(0, len(self.title_volume)):
                self.volume_checkbox[i_volume].setChecked(True)
        if state_allcheck != 0:
            for i_volume in range(0, len(self.title_volume)):
                self.volume_checkbox[i_volume].setChecked(False)


    async def image_download(self, headers, url_image, name_image, i_image):
        name_image.append(str(i_image) + '.jpg')
        async with aiohttp.ClientSession() as session:
            print(i_image)
            async with session.get(url_image[i_image], headers=headers) as get_image:
                image = await get_image.read()
                with open(name_image[i_image], 'wb') as fd:
                    fd.write(image)


    async def image_download_run(self, headers, url_image, name_image):
        for i_image in range(0, len(url_image)):
            await self.image_download(headers, url_image, name_image, i_image)


    def download(self):
        '''下载漫画'''
        '''问题：'''

        _translate = QtCore.QCoreApplication.translate

        checked = []
        for i_volume in range(0, len(self.title_volume)):
            if self.volume_checkbox[i_volume].isChecked():
                checked.append(i_volume)

        if not os.path.exists('download'):
            os.mkdir('download')
        os.chdir('download')

        dir_comic = self.title_search_sum[self.i_comic].replace('/', ' ')
        if not os.path.exists(dir_comic):
            os.mkdir(dir_comic)
        os.chdir(dir_comic)

        self.downlist_frame = []
        self.downtitle_label = []
        self.downstatus_label = []
        self.down_progressBar = []
        y = 0
        for i_volume in checked:
            y += 40
            self.downlist_frame.append(QtWidgets.QFrame(self.down_scrollAreaWidgetContents))
            self.downtitle_label.append(QtWidgets.QLabel(self.downlist_frame[i_volume]))
            self.downstatus_label.append(QtWidgets.QLabel(self.downlist_frame[i_volume]))
            self.down_progressBar.append(QtWidgets.QProgressBar(self.downlist_frame[i_volume]))

            self.downlist_frame[i_volume].setGeometry(0, y, 1301, 40)
            self.downlist_frame[i_volume].setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.downlist_frame[i_volume].setFrameShadow(QtWidgets.QFrame.Raised)
            self.downlist_frame[i_volume].show()
            self.downtitle_label[i_volume].setGeometry(19, 5, 581, 31)
            self.downtitle_label[i_volume].setText(_translate("Form", '<html><head/><body><p><span style=" font-size:18pt;">' + self.title_search_sum[self.i_comic] + ' ' + self.title_volume[i_volume] + '</span></p></body></html>'))
            self.downtitle_label[i_volume].show()
            self.downstatus_label[i_volume].setGeometry(1160, 10, 131, 21)
            self.downstatus_label[i_volume].setText(_translate("Form", '等待下载'))
            self.downstatus_label[i_volume].show()
            self.down_progressBar[i_volume].setGeometry(730, 10, 411, 21)
            self.down_progressBar[i_volume].hide()



        browser = webdriver.PhantomJS()

        for i_volume in checked:
            browser.get('http://manhua.dmzj.com' + self.link_volume[i_volume])
            tree_volume = etree.HTML(browser.page_source)
            url_image = tree_volume.xpath('//select[@id="page_select"]/option/@value')
            dir_volume = self.title_volume[i_volume].replace('/', ' ')
            if not os.path.exists(dir_volume):
                os.mkdir(dir_volume)
            else:
                continue
            os.chdir(dir_volume)
            headers = {'Referer':'http://manhua.dmzj.com' + self.link_volume[i_volume]}
            name_image = []

            image_loop = asyncio.get_event_loop()
            image_loop.run_until_complete(self.image_download_run(headers, url_image, name_image))

            os.chdir(os.path.dirname(os.path.abspath('.')))
            zip_volume = zipfile.ZipFile(dir_volume + '.zip', 'w')
            for i_image in range(0, len(url_image)):
                zip_volume.write('./' + dir_volume + '/' + name_image[i_image])
        os.chdir(os.path.dirname(os.path.abspath('.')))
        os.chdir(os.path.dirname(os.path.abspath('.')))


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "动漫之家漫画下载 BY ssj"))
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


