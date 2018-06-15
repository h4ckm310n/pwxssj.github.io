from PyQt5 import QtCore, QtWidgets
from ui_main import UIForm
from search import UISearch, SearchThread


class Main(UIForm):
    def __init__(self):
        super(Main, self).__init__()


        self.url_search = 'https://www.dmzj.com/dynamic/o_search/index/' + '超人'

        self.search_thread = None
        self.comic_thread = None
        self.dl_thread = None

        self.ui_search = None

        self.search_button.clicked.connect(self.start_search)

    def start_search(self):
        self.search_thread = SearchThread(self.url_search)

        self.ui_search = UISearch(self.url_search, self.search_thread)
        self.search_thread.wait.connect(self.ui_search.waiting)
        self.ui_search.search()
        self.search_thread.start()




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
