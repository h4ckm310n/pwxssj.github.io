from PyQt5.QtCore import *
import requests
import multiprocessing as mp
import json
import os
from comic_download.process import *
import time
from concurrent.futures import *


headers = {'Referer': 'http://imgsmall.dmzj.com/'}


class PutThread(QThread):
    new = pyqtSignal(dict)

    def __init__(self, tasks):
        super(PutThread, self).__init__()
        self.tasks = tasks
        self.tasks_checked = []

    def run(self):
        self.check_task()
        for task in self.tasks_checked:
            q1.put(task)

    def check_task(self):
        for task in self.tasks:
            if all_tasks != []:
                for task_exist in all_tasks:
                    if (task['comic'] == task_exist['comic']) and (task['chap'] == task_exist['chap']):
                        # 存在相同任务
                        break
                    else:
                        # 添加任务

                        task['index'] = len(all_tasks)
                        self.tasks_checked.append(task)
                        self.new.emit(task)
                        all_tasks.append(task)
                        break
            else:
                task['index'] = len(all_tasks)
                self.tasks_checked.append(task)
                self.new.emit(task)
                all_tasks.append(task)


class DLThread(QThread):
    def __init__(self):
        super(DLThread, self).__init__()
        self.dl_pool = mp.Pool()

    def run(self):
        while True:
            if q1.empty():
                time.sleep(5)
                continue
            else:
                # new_task = self.dl_pool.apply_async(chap_info, )
                chap_info()

                time.sleep(2)
        self.dl_pool.close()
        self.dl_pool.join()


class UPDThread(QThread):
    info = pyqtSignal(dict)
    def __init__(self):
        super(UPDThread, self).__init__()
        self.upd_pool = mp.Pool()

    def run(self):
        self.update()

    def update(self):
        while True:
            if q2.empty():
                time.sleep(2)
                continue
            else:
                upd = self.upd_pool.apply_async(task_upd, ).get()
                self.info.emit(upd)
                time.sleep(2)
        self.upd_pool.close()
        self.upd_pool.join()


class InitThread(QThread):
    init = pyqtSignal(list)
    def __init__(self):
        super(InitThread, self).__init__()

    def run(self):
        """读取文件并添加到下载列表"""

        tasks = []
        with open('comic.txt', 'r+') as sav:
            if sav.read() == '':
                self.init.emit([])
            else:
                for task in sav.readlines():
                    task = json.loads(task.replace('\n', ''))
                    comic = task['comic']
                    chap = task['chap']
                    url = task['url']
                    page_num = task['page_num']
                    state = task['state']
                    if state == 0:
                        q1.put(task)
                    tasks.append(task)
                self.init.emit(tasks)
        time.sleep(1)
