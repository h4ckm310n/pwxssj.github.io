from ui_main import UIForm
from PyQt5 import QtCore, QtWidgets
import requests
from lxml.html import etree


class SearchThread(QtCore.QThread):

    wait = QtCore.pyqtSignal()
    '''no_result = QtCore.pyqtSignal()
    result = QtCore.pyqtSignal(list)'''

    def __init__(self, url_search, parent=None):
        super(SearchThread, self).__init__()
        self.url_search = url_search

    def run(self):
        self.wait.emit()
        '''print("check")
        result_search = requests.get(self.url_search)
        if '很遗憾，您搜索的内容暂时没有找到。' in result_search.text:
            print("noresult")
            self.no_result.emit()
            print('noresultemit:' + str(self.no_result.emit()))
        else:
            print("result")
            self.run_search(result_search)'''

    def run_search(self, result_search):
        tree_search = etree.HTML(result_search.text)
        page_search = tree_search.xpath(
            '//div[@class="bottom_page page"]/a[text()!="上一页"][text()!="下一页"]/text()')

        i_comic_sum = 0
        title_search_sum = []
        latest_search_sum = []
        link_search_sum = []

        for i_page_search in range(0, len(page_search)):
            result_search = requests.get(self.url_search + '/' + page_search[i_page_search])
            tree_search = etree.HTML(result_search.text)
            page_search = tree_search.xpath(
                '//div[@class="bottom_page page"]/a[text()!="上一页"][text()!="下一页"]/text()')

            title_search = tree_search.xpath('//ul[@class="update_con autoHeight"]/li/a/@title')
            cover_search = tree_search.xpath('//ul[@class="update_con autoHeight"]/li/a/img/@src')
            auth_search = tree_search.xpath('//ul[@class="update_con autoHeight"]/li/p[class="auth"]/text()')
            latest_search = tree_search.xpath('//p[@class="newPage"]/text()')
            link_search = tree_search.xpath('//ul[@class="update_con autoHeight"]/li/a/@href')

            # 该页漫画信息
            for i_comic in range(0, len(title_search)):
                title_search_sum.append(title_search[i_comic])
                latest_search_sum.append(latest_search[i_comic])
                link_search_sum.append('http:' + link_search[i_comic])
                i_comic_sum = i_comic_sum + 1
        print('end crawl')
        self.result.emit([title_search_sum, latest_search_sum, link_search_sum, i_comic_sum])


class UISearch(UIForm):
    def __init__(self, url_search, search_thread):
        super(UISearch, self).__init__()
        self.url_search = url_search
        self.search_thread = search_thread

        self.noresult_label = None
        self.title_search_label = None
        self.wait_label = None

    def search(self):
        if self.noresult_label is not None:
            self.gridLayout_search.removeWidget(self.noresult_label)
            self.noresult_label.deleteLater()
            self.noresult_label = None
        if 'title_search_label' in dir(self):
            for i_t_label in self.search_scrollAreaWidgetContents.children():
                i_t_label.deleteLater()
                # i_t_label = None

        '''if self.search_edit.text() == '':
            ''''''
            print('请输入搜索内容')'''

    def waiting(self):
        self.wait_label = QtWidgets.QLabel(self.search_scrollAreaWidgetContents)
        self.wait_label.setGeometry(QtCore.QRect(50, 20, 300, 20))
        self.wait_label.setTextFormat(QtCore.Qt.AutoText)
        self.wait_label.setAlignment(QtCore.Qt.AlignCenter)
        self.wait_label.setText("正在搜索……")
        self.wait_label.show()

    def no_result(self):
        print("UInoresult")
        '''self.gridLayout_search.removeWidget(self.wait_label)
        self.wait_label.deleteLater()
        self.wait_label = None

        self.noresult_label = QtWidgets.QLabel(self.search_scrollAreaWidgetContents)
        self.noresult_label.setGeometry(QtCore.QRect(50, 20, 500, 140))
        self.noresult_label.setTextFormat(QtCore.Qt.AutoText)
        self.noresult_label.setAlignment(QtCore.Qt.AlignCenter)
        self.noresult_label.setText("<html><head/><body><p><span style=\" font-size:24pt;\">\
        很遗憾，您搜索的内容暂时没有找到。</span></p></body></html>")
        self.gridLayout_search.addWidget(self.noresult_label, 0, 0, 1, 1)
        self.noresult_label.show()'''

    def result(self, search_result):
        print("UIresult")
        search_titles = search_result[0]
        search_latests = search_result[1]
        search_links = search_result[2]
        i_comic_sum = search_result[3]

        self.search_scrollArea.setStyleSheet('.QWidget {background-color: rgb(255, 255, 255);}')
        y = 10
        self.title_search_label = []
        for i in range(0, i_comic_sum):
            print(search_titles[i])
