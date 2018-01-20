#  -*- coding: utf-8 -*-

#  form implementation generated from reading ui file 'form.ui'
# 
#  Created by: PyQt5 UI code generator 5.9.1
# 
#  WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import os
import requests
import zipfile
from lxml import etree
import functools
# import queue
import execjs


"""问题：下载队列"""


class SearchThread(QtCore.QThread):
    def run(self):
        pass


class ComicThread(QtCore.QThread):
    def run(self):
        pass


class DownThread(QtCore.QThread):
    down_init = QtCore.pyqtSignal(list)
    down_progress = QtCore.pyqtSignal(list)

    def __init__(self, checked, link_volume, title_volume, parent=None):
        super(DownThread, self).__init__()
        self.checked = checked
        self.link_volume = link_volume
        self.title_volume = title_volume

    def run(self):
        """下载漫画"""

        for i_volume in range(0, len(self.checked)):
            self.down_init.emit([i_volume, '正在解析', 0])
            response_volume = requests.get('http://manhua.dmzj.com' + self.link_volume[self.checked[i_volume]])
            tree_volume = etree.HTML(response_volume.text)
            js_volume = tree_volume.xpath("//html/head/script[1]/text()")[0].strip().split('\n')[2].strip()[5:-1]
            url_image = execjs.eval(js_volume)[19:-4].split('","')
            for i_image in range(0, len(url_image)):
                url_image[i_image] = 'http://images.dmzj.com/' + url_image[i_image].replace('\\', '')
            self.down_init.emit([i_volume, '正在下载', len(url_image)])
            dir_volume = self.title_volume[self.checked[i_volume]].replace('/', ' ')
            if not os.path.exists(dir_volume):
                os.mkdir(dir_volume)
            else:
                self.down_init.emit([i_volume, '目录存在', 0])
                continue
            os.chdir(dir_volume)
            headers = {'Referer': 'http://manhua.dmzj.com' + self.link_volume[self.checked[i_volume]]}
            name_image = []
            for i_image in range(0, len(url_image)):
                name_image.append(str(i_image) + '.jpg')
                get_image = requests.get(url_image[i_image], headers=headers)
                with open(name_image[i_image], 'wb') as fd:
                    fd.write(get_image.content)
                self.down_progress.emit([i_volume, i_image, len(url_image)])

            os.chdir(os.path.dirname(os.path.abspath('.')))
            zip_volume = zipfile.ZipFile(dir_volume + '.zip', 'w')
            for i_image in range(0, len(url_image)):
                zip_volume.write('./' + dir_volume + '/' + name_image[i_image])
        os.chdir(os.path.dirname(os.path.abspath('.')))
        os.chdir(os.path.dirname(os.path.abspath('.')))
        print('end')


class UiForm(object):
    def setup_ui(self, form):
        """窗口初始状态"""

        form.setObjectName("form")
        form.isMaximized()
        form.setWindowTitle("动漫之家漫画下载 BY ssj")
        self.gridLayout_Form = QtWidgets.QGridLayout(form)
        self.gridLayout_Form.setObjectName("gridLayout_Form")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.search_edit = QtWidgets.QLineEdit(form)
        self.search_edit.setObjectName("search_edit")
        self.gridLayout.addWidget(self.search_edit, 0, 0, 1, 1)
        self.search_buttom = QtWidgets.QPushButton(form)
        self.search_buttom.setObjectName("search_buttom")
        self.search_buttom.setText("搜索")
        self.gridLayout.addWidget(self.search_buttom, 0, 1, 1, 1)
        self.gridLayout_Form.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.search_buttom.clicked.connect(self.search)
        self.tabWidget = QtWidgets.QTabWidget(form)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.tabCloseRequested.connect(self.tab_remove)
        self.num_tab = 0
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.search_tab), "搜索结果")
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.down_tab), "下载任务")
        self.gridLayout_Form.addWidget(self.tabWidget, 1, 0, 1, 1)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(form)

    def search(self):
        """搜索漫画"""

        # 清空搜索页面
        if('nofound_label' in dir(self)):
            if self.nofound_label != None:
                self.gridLayout_search.removeWidget(self.nofound_label)
                self.nofound_label.deleteLater()
                self.nofound_label = None
        if('title_search_label' in dir(self)):
            for i_t_label in self.search_scrollAreaWidgetContents.children():
                i_t_label.deleteLater()
                i_t_label = None

        url_search = 'https://www.dmzj.com/dynamic/o_search/index/' + '闪电侠'
        result_search = requests.get(url_search)
        # 没有搜索结果
        if '很遗憾，您搜索的内容暂时没有找到。' in result_search.text:
            self.nofound_label = QtWidgets.QLabel(self.search_scrollAreaWidgetContents)
            self.nofound_label.setGeometry(QtCore.QRect(50, 20, 500, 140))
            self.nofound_label.setTextFormat(QtCore.Qt.AutoText)
            self.nofound_label.setAlignment(QtCore.Qt.AlignCenter)
            self.nofound_label.setText("<html><head/><body><p><span style=\" font-size:24pt;\">很遗憾，您搜索的内容暂时没有找到。</span></p></body></html>")
            self.gridLayout_search.addWidget(self.nofound_label, 0, 0, 1, 1)
            self.nofound_label.show()
        # 显示搜索结果
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
            # 爬取搜索结果中每一页的漫画信息
            for i_page_search in range(0, len(page_search)):
                result_search = requests.get(url_search + '/' + page_search[i_page_search])
                tree_search = etree.HTML(result_search.text)
                page_search = tree_search.xpath(
                    '//div[@class="bottom_page page"]/a[text()!="上一页"][text()!="下一页"]/text()')
                self.title_search = tree_search.xpath('//ul[@class="update_con autoHeight"]/li/a/@title')
                self.latest_search = tree_search.xpath('//p[@class="newPage"]/text()')
                self.link_search = tree_search.xpath('//ul[@class="update_con autoHeight"]/li/a/@href')
                # 该页漫画信息
                for i_comic in range(0, len(self.title_search)):
                    self.title_search_sum.append(self.title_search[i_comic])
                    self.latest_search_sum.append(self.latest_search[i_comic])
                    self.link_search_sum.append('http:' + self.link_search[i_comic])
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
                    self.title_search_label[self.i_comic_sum].setText(text_search_label)
                    self.title_search_label[self.i_comic_sum].show()
                    self.title_search_label[self.i_comic_sum].mousePressEvent = functools.partial(self.comic, source_object = self.title_search_label[self.i_comic_sum])
                    if i_comic in range(3, len(self.title_search), 4):
                        y = y + 30
                    self.i_comic_sum = self.i_comic_sum + 1
                self.search_scrollAreaWidgetContents.setFixedHeight(y + 30)

    def comic(self, event, source_object=None):

        """漫画界面"""

        self.i_comic = int(source_object.text()[52:-25][0]) - 1
        self.comic_tab = QtWidgets.QWidget()
        self.gridLayout_comic = QtWidgets.QGridLayout(self.comic_tab)
        self.comic_frame = QtWidgets.QFrame()
        self.comic_frame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.comic_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.comic_frame.show()
        self.gridLayout_comic.addWidget(self.comic_frame, 0, 0, 1, 1)
        self.tabWidget.insertTab(1, self.comic_tab, "")
        self.num_tab += 1
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.comic_tab), self.title_search_sum[self.i_comic])
        self.tabWidget.setCurrentWidget(self.comic_tab)
        response_comic = requests.get(self.link_search_sum[self.i_comic])
        # 暂停提供
        if '4004.gif' in response_comic.text:
            self.noprovide_label = QtWidgets.QLabel(self.comic_frame)
            self.noprovide_label.setAlignment(QtCore.Qt.AlignCenter)
            self.noprovide_label.setText("<html><head/><body><p><span style=\" font-size:24pt;\">因版权等原因暂停提供</span></p></body></html>")
            self.noprovide_label.setGeometry(50, 20, 500, 140)
            self.gridLayout_comic.addWidget(self.noprovide_label, 0, 0, 1, 1)
            self.noprovide_label.show()
        # 显示章节列表
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
            self.title_label.setText('﻿<html><head/><body><p><span style=" font-size:14pt; font-weight:600; color:#0000ff;">' + self.title_search_sum[self.i_comic] + '</span></p></body></html>')
            self.intro_label = QtWidgets.QLabel(self.comic_frame)
            self.intro_label.setGeometry(250, 90, 351, 301)
            self.intro_label.setAlignment(QtCore.Qt.AlignBaseline)
            self.intro_label.setWordWrap(True)
            self.intro_label.setFrameShape(QtWidgets.QFrame.Box)
            self.intro_label.setFrameShadow(QtWidgets.QFrame.Plain)
            self.intro_label.setText(intro_comic[0].strip())
            self.allselect_button = QtWidgets.QPushButton(self.comic_frame)
            self.allselect_button.setGeometry(400, 40, 100, 40)
            self.allselect_button.setText("全选")
            self.download_button = QtWidgets.QPushButton(self.comic_frame)
            self.download_button.setGeometry(500, 40, 100, 40)
            self.download_button.setText("下载")
            self.volume_checkbox = []
            i_list = 0
            for i_volume in range(0, len(self.title_volume)):
                x = 10 + 180 * i_list
                y = 10 + 30 * (i_volume % 15) * (i_list + 1)
                self.volume_checkbox.append(QtWidgets.QCheckBox(self.volume_scrollAreaWidgetContents))
                self.volume_checkbox[i_volume].setGeometry(x, y, 170, 20)
                self.volume_checkbox[i_volume].setText(str(i_volume + 1) + ' ' + self.title_volume[i_volume])
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
        """关闭标签页"""

        if index != 0 and index != self.num_tab + 1:
            self.tabWidget.removeTab(index)
            self.num_tab -= 1

    def all_select(self):
        """点击全选按钮"""

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

    def download(self):
        """下载漫画"""

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
        # 下载任务列表
        for i_volume in range(0, len(checked)):
            self.downlist_frame.append(QtWidgets.QFrame(self.down_scrollAreaWidgetContents))
            self.downtitle_label.append(QtWidgets.QLabel(self.downlist_frame[i_volume]))
            self.downstatus_label.append(QtWidgets.QLabel(self.downlist_frame[i_volume]))
            self.down_progressBar.append(QtWidgets.QProgressBar(self.downlist_frame[i_volume]))
            self.downlist_frame[i_volume].setGeometry(0, y, 1301, 40)
            self.downlist_frame[i_volume].setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.downlist_frame[i_volume].setFrameShadow(QtWidgets.QFrame.Raised)
            self.downlist_frame[i_volume].show()
            self.downtitle_label[i_volume].setGeometry(19, 5, 581, 31)
            self.downtitle_label[i_volume].setText('<html><head/><body><p><span style=" font-size:18pt;">' + self.title_search_sum[self.i_comic] + ' ' + self.title_volume[checked[i_volume]] + '</span></p></body></html>')
            self.downtitle_label[i_volume].show()
            self.downstatus_label[i_volume].setGeometry(1160, 10, 131, 21)
            self.downstatus_label[i_volume].setText('等待下载')
            self.downstatus_label[i_volume].show()
            self.down_progressBar[i_volume].setGeometry(730, 10, 411, 21)
            self.down_progressBar[i_volume].hide()
            y += 40
        # 下载
        self.tabWidget.setCurrentWidget(self.down_tab)
        self.down_thread = DownThread(checked, self.link_volume, self.title_volume)
        self.down_thread.down_init.connect(self.down_init)
        self.down_thread.down_progress.connect(self.down_progress)
        self.down_thread.start()

    def down_init(self, down_info):
        """下载状态信息"""

        i_volume = down_info[0]
        status_text = down_info[1]
        progress_max = down_info[2]
        self.downstatus_label[i_volume].setText(status_text)
        if progress_max != 0:
            self.down_progressBar[i_volume].setMaximum(progress_max)
            self.down_progressBar[i_volume].setValue(0)
            self.down_progressBar[i_volume].show()

    def down_progress(self, down_info):
        """下载进度条"""

        i_volume = down_info[0]
        i_image = down_info[1] + 1
        progress_max = down_info[2]
        self.down_progressBar[i_volume].setValue(i_image)
        if i_image == progress_max:
            self.downstatus_label[i_volume].setText('下载完成')
            self.down_progressBar[i_volume].hide()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui = UiForm()
    ui.setup_ui(form)
    form.showMaximized()
    sys.exit(app.exec_())
