import requests
import pymysql
from lxml.html import etree
import multiprocessing as mp
import time
from datetime import datetime
import os

base_url = 'https://intranet.must.edu.mo/student/'
news_url = base_url + 'jumpMoreXtgNews.jsp'
down_url = base_url + 'DownloadFile'
view_url = base_url + 'InfoServlet'
headers = {'Authorization': 'Basic MTcwOTg1M3hpMDExMDAxOjM2OTcyOTMy',  # base64(id:pwd)
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/70.0.3538.110 Safari/537.36'}
lower_date = '2018-11-30'
import re


class DB:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'Vmust'
        self.pwd = 'wolaojunyibuganle'
        self.db = 'Vmust_news'
        self.con = None
        self.cursor = None

    def connect(self, times):
        """connect database"""

        if too_many_errors(times):
            log('Error: connect database failed ' + str(times) + ' times, cancel')
            return False
        try:
            times += 1
            log('trying to connect database ' + str(times) + ' times...')
            self.con = pymysql.connect(self.host, self.user, self.pwd, self.db)
            self.cursor = self.con.cursor()
            log('Success: connect successfully')
            return True
        except Exception:
            log('Error: connect database failed')
            time.sleep(2)
            return self.connect(times)
        except KeyboardInterrupt:
            log('KeyboardInterrupt, exit')
            exit()

    def close(self):
        self.cursor.close()
        self.con.close()
        log('datebase closed')

    def news_exist(self, id, times):
        """check if current news exists in database"""

        if too_many_errors(times):
            log('Error: search id '+ id + ' failed ' + str(times) + ' times, cancel')
            return -1
        try:
            times += 1
            log('trying to search id ' + id + ' '+ str(times) + ' times...')
            self.connect(0)
            sql = 'SELECT * FROM news WHERE id = %s' % id
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            self.close()
            if result is None:
                # news not in database
                log('id ' + id + ' not exists, update')
                return 0
            else:
                log('id ' + id + ' exists, skip')
                return 1
        except Exception:
            log('Error: search in database failed')
            return self.news_exist(id, times)
        except KeyboardInterrupt:
            log('KeyboardInterrupt, exit')
            exit()

    def update(self, id, title, category, date, onclick, text, files, times):
        """update to database"""

        if too_many_errors(times):
            log('Error: update id ' + id + ' failed ' + str(times) + ' times, cancel')
            return -1
        try:
            times += 1
            log('trying to update news id ' + id + ' ' + str(times) + ' times...')
            self.connect(0)
            sql1 = "INSERT INTO news(id, title, category, date, onclick, text) VALUES " \
                  "('%s', '%s', '%s', '%s', '%s', '%s')" % (id, title, category, date, onclick, text)
            print(sql1)
            self.cursor.execute(sql1)
            self.con.commit()
            log('    Success: insert news id ' + id + ' successfully')
            if files != []:
                for file in files:
                    sql2 = "INSERT INTO files(id, file) VALUES ('%s', '%s')" % (id, file)
                    print(sql2)
                    self.connect(0)
                    self.cursor.execute(sql2)
                    self.con.commit()
                    log('    Success: insert file id ' + id + ' successfully')
            log('    Success: update id ' + id + 'successfully')
            self.close()
            return 1
        except KeyboardInterrupt:
            log('KeyboardInterrupt, exit')
            exit()
        except Exception:
            log('    Error: update id ' + id + ' failed')
            self.con.rollback()
            return self.update(id, title, category, date, onclick, text, files, times)


class Scrape:
    def __init__(self):
        self.session = requests.Session()
        self.session.trust_env = False
        self.db = DB()
        self.pool = mp.Pool(4)

    def down(self, title, category, date, id, mode, times):
        """downContent"""

        indent = ''
        if mode == 'view':
            indent = '    '
        if too_many_errors(times):
            log(indent + 'Error: download id ' + id + ' failed ' + str(times) + ' times, cancel')
            return -1
        data = {'dId': id}
        try:
            times += 1
            log(indent + 'trying to download id ' + id + ' ' + str(times) + ' times...')
            r = self.session.post(down_url, data=data, headers=headers)
            if r.status_code != 200:
                raise Exception

            extension = r.headers['Content-disposition'].lstrip('attachment;filename="download+files"')
            filename = id + extension
            with open('files/' + filename, 'wb') as f:
                f.write(r.content)
            log(indent + 'Success: download id: ' + id + ' successfully')
            if mode == 'view':
                return filename
            elif mode == 'down':
                if self.db.update(id, title, category, date, mode, '0', [filename], 0) == -1:
                    return -1
                return 1
        except KeyboardInterrupt:
            log('KeyboardInterrupt, exit')
            exit()
        except Exception:
            log(indent + 'Error: download id: ' + id + ' failed')
            return self.down(title, category, date, id, mode, times)

    def view(self, title, category, date, id, news, dept, lang, times):
        """viewContent"""

        if too_many_errors(times):
            log('Error: get content id ' + id + ' failed ' + str(times) + ' times, cancel')
            return -1
        data = {'id': id,
                'infoType': news,
                'deptType': dept,
                'langType': lang}
        try:
            times += 1
            log('trying to get content id ' + id + ' ' + str(times) + ' times...')
            r = self.session.post(view_url, data=data, headers=headers)
            if r.status_code != 200:
                raise Exception
            tree = etree.HTML(r.text)
            # text content
            content_texts = tree.xpath('//table[@id="Table_01"]/tr[4]/td/table/tr[2]/td/table/tr[2]/td//text()|'
                                       '//table[@id="Table_01"]/tr[4]/td/table/tr[2]//img/@src')
            temp = ''
            for t in content_texts:
                if '/studentGroup/upload' in t:
                    text = '(imgurl)' + base_url.replace('/student/', t) + '(/imgurl)'
                temp += t
            text = temp.strip()
            # download files
            file_down = tree.xpath('//table[@id="Table_01"]/tr[4]/td/table/tr[2]/td/table/tr/td/a/@onclick')
            files = []
            if file_down != []:
                for f in file_down:
                    if 'downContent' in f:
                        did = f.lstrip('downContent(\'').rstrip('\');')
                        down_result = self.down(title, category, date, did, 'view', 0)
                        if down_result == -1:
                            raise Exception
                        files.append(down_result)

            # update to database
            if self.db.update(id, title, category, date, 'view', text, files, 0) == -1:
                return -1
            log('Success: get content id ' + id + ' successfully')
            return 1
        except KeyboardInterrupt:
            log('KeyboardInterrupt, exit')
            exit()
        except Exception:
            log('Error: get content id ' + id + ' failed')
            return self.view(title, category, date, id, news, dept, lang, times)

    def news_list(self, content, times):
        """get the list of news"""

        if too_many_errors(times):
            log('Error: list news failed ' + str(times) + ' times, cancel')
            return -1
        try:
            times += 1
            list_status = 0
            log('trying to list news ' + str(times) + ' times...')
            t = etree.HTML(content)
            text = t.xpath('//a[@style="cursor:pointer"]/text()')
            onclick = t.xpath('//a[@style="cursor:pointer"]/@onclick')
            for i in range(len(text)):
                # reach the lower date
                if lower_date in text[i]:
                    break

                text[i] = text[i].strip()
                category = re.search('^\([^)]*\)', text[i]).group()
                date = re.search('[\d]{4}-[\d]{2}-[\d]{2}$', text[i]).group()
                title = text[i].lstrip(category).rstrip(date).strip()
                category = category.lstrip('(').rstrip(')')

                if 'viewContent' in onclick[i]:
                    onclick[i] = onclick[i].lstrip('viewContent(\'').rstrip('\');').split('\', \'')
                    id = onclick[i][0]
                    news = 'news'
                    dept = 'student'
                    lang = ''
                    exist = self.db.news_exist(id, 0)
                    if exist == 0:
                        if self.view(title, category, date, id, news, dept, lang, 0) == -1:
                            list_status = -1
                            continue
                    elif exist == -1:
                        list_status = -1
                        continue
                    else:
                        continue

                elif 'downContent' in onclick[i]:
                    onclick[i] = onclick[i].lstrip('downContent(\'').rstrip('\');')
                    id = onclick[i]
                    exist = self.db.news_exist(id, 0)
                    if exist == 0:
                        if self.down(title, category, date, id, 'down', 0) == -1:
                            list_status = -1
                            continue
                    elif exist == -1:
                        list_status = -1
                        continue
                    else:
                        continue
            if list_status == -1:
                log('Error: listing failed')
                return -1
            log('Success: listing successfully')
            return 1
        except KeyboardInterrupt:
            log('KeyboardInterrupt, exit')
            exit()
        except Exception:
            log('Error: listing failed')
            return self.news_list(content, times)

    def login(self, times):
        if too_many_errors(times):
            log('Error: login failed ' + str(times) + ' times, cancel')
            return -1
        if not self.db.connect(0):
            return -1
        self.db.close()
        try:
            times += 1
            log('trying to login ' + str(times) + ' times...')
            r = self.session.get(news_url, headers=headers)
            if r.status_code == 200:
                log('Success: login successfully')
                return r.text
            raise Exception
        except KeyboardInterrupt:
            log('KeyboardInterrupt, exit')
            exit()
        except Exception:
            log('Error: login failed')
            time.sleep(3)
            return self.login(times)


def log(text):
    try:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
        print(now + text)
        with open('news.log', 'a') as f:
            f.write(now + text + '\n')
    except Exception:
        log('Error: log failed')
        datetime.now()


def too_many_errors(times):
    """if a task failed 5 times, cancel it"""

    if times >= 5:
        return True
    return False


if __name__ == '__main__':
    scrape = Scrape()
    content = scrape.login(0)
    scrape.news_list(content, 0)

