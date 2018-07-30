from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import multiprocessing as mp
from ui_main import UIForm
from comic_search.ui import *
from comic_search.thread import SearchThread
from comic_info.ui import *
from comic_info.thread import InfoThread
from comic_download.ui import *
from comic_download.thread import *
from comic_download.process import *


class Main(UIForm):
    def __init__(self):
        super(Main, self).__init__()
        self.init_dialog = InitDialog(self)
        self.dl_list = DLList(self.dl_tab)
        self.init_thread = InitThread()
        self.init_thread.init.connect(self.dl_init)
        self.init_thread.start()
        self.init_dialog.exec_()
        self.dl_thread = DLThread()
        self.upd_thread = UPDThread()
        self.upd_thread.info.connect(self.dl_update)
        self.dl_thread.start()
        self.upd_thread.start()

        self.search_thread = None
        self.info_thread = None

        self.search_dialog = None

        self.info_tab = None
        self.info_dialog = None

        self.dl_frames = []
        self.i_frame = 0

        self.put_pool = mp.Pool()
        self.dl_pool = mp.Pool()
        self.upd_pool = mp.Pool()

        self.setup_ui()

        self.search_button.clicked.connect(self.start_search)

    def dl_init(self, tasks):
        if tasks != []:
            for i in range(len(tasks)):
                tasks[i]['index'] = i
                self.add_task(tasks[i])
        self.dl_list.show()
        self.init_dialog.close()

    def start_search(self):

        text = '闪电侠'
        if text != '':
            self.search_dialog = SearchDialog(self)

            self.search_thread = SearchThread(text)

            self.search_thread.state.connect(self.search_state)
            self.search_thread.result.connect(self.search_list)

            self.search_thread.start()

    def search_state(self, state):
        search_state(self.search_dialog, state)

    def search_list(self, results):
        result_list = ResultList(self.search_tab)

        for result in results:
            title = result['title']
            auth = result['auth']
            latest = result['latest']
            status = result['status']
            id = result['id']

            result_list.add_to_list(title, auth, latest, status, id)

        result_list.show()

    def comic_clicked(self, title, auth, latest, status, id):
        self.info_dialog = InfoDialog(self)
        self.info_thread = InfoThread(title, auth, latest, status, id)
        self.info_thread.info_state.connect(self.info_state)
        self.info_thread.info.connect(self.comic_info)
        self.info_thread.start()

    def info_state(self, state):
        info_state(self.info_dialog, state)

    def comic_info(self, info):
        title = info['title']
        cover = info['cover']
        auth = info['auth']
        latest = info['latest']
        status = info['status']
        intro = info['intro']
        chaps = info['chaps']
        id = info['id']

        self.info_tab = QWidget()
        self.tabWidget.insertTab(1, self.info_tab, '')
        self.tabWidget.setTabText(1, title)
        self.tabWidget.setCurrentIndex(1)
        self.info_frame = InfoFrame(title, cover, auth, latest, status, intro, chaps, id, self.info_tab)
        self.info_frame.show()

    def download_clicked(self, comic, checkboxes):
        tasks = []
        for checked in checkboxes:
            chap = checked.chap
            url = checked.url
            tasks.append\
                ({"comic": comic, "index": 0, "chap": chap, "url": url, "progress": 0, "page_num": 1, "state": -1})
            # self.i_frame += 1
        self.put_thread = PutThread(tasks)
        self.put_thread.new.connect(self.add_task)
        self.put_thread.start()
        self.tabWidget.setCurrentWidget(self.dl_tab)

    def add_task(self, task):
        title = task['comic']
        chap = task['chap']
        page_num = task['page_num']
        state = task['state']
        frame = ItemFrame(title, chap, page_num, state, self.dl_list)
        self.dl_list.add_to_list(frame)
        self.dl_frames.append(frame)

    def dl_update(self, task):
        i = task['index']
        progress = task['progress']
        page_num = task['page_num']
        state = task['state']

        frame = self.dl_frames[i]
        if frame.state != state:
            frame.state_change(state)
        frame.progress_update(page_num, progress)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
