import requests
from lxml import etree
from selenium import webdriver
import os
import zipfile

def search():
    print('搜索：')
    kw_search = input()
    url_search = 'https://www.dmzj.com/dynamic/o_search/index/' + kw_search
    result_search = requests.get(url_search)
    if '很遗憾，您搜索的内容暂时没有找到。' in result_search.text:
        print('很遗憾，您搜索的内容暂时没有找到。')
    else:
        tree_search = etree.HTML(result_search.text)
        page_search = tree_search.xpath\
            ('//div[@class="bottom_page page"]/a[text()!="上一页"][text()!="下一页"]/text()')
        print('共' + str(len(page_search)) + '页搜索结果')
        print('输入页数：')
        i_page_search = int(input()) - 1

        if i_page_search in range(0,len(page_search)):
            result_search = requests.get(url_search + '/' + page_search[i_page_search])
            print('第' + page_search[i_page_search] + '页')
            print()
            tree_search = etree.HTML(result_search.text)
            global title_search
            title_search = tree_search.xpath('//ul[@class="update_con autoHeight"]/li/a/@title')
            latest_search = tree_search.xpath('//p[@class="newPage"]/text()')
            global link_search
            link_search = tree_search.xpath('//ul[@class="update_con autoHeight"]/li/a/@href')
            for i_comic in range(0,len(title_search)):
                print(i_comic + 1)
                print(title_search[i_comic] + ' ' + latest_search[i_comic])
                print()
            global input_i_comic
            print('输入漫画序号：')
            input_i_comic = int(input()) - 1
        else:
            print('该页没有搜索结果')

def comic():
    print(title_search[input_i_comic])
    print()
    response_comic = requests.get(link_search[input_i_comic])
    if '4004.gif' in response_comic.text:
        print('因版权等原因暂停提供')
        input()
        exit()
    else:
        tree_comic = etree.HTML(response_comic.text)
        global title_volume
        global link_volume
        title_volume = tree_comic.xpath('//div[@class="cartoon_online_border"]/ul/li/a/text()')
        link_volume = tree_comic.xpath('//div[@class="cartoon_online_border"]/ul/li/a/@href')

        for i_volume in range(0,len(title_volume)):
            print(i_volume + 1)
            print(title_volume[i_volume])
            print()

        global input_i_volume
        print('输入卷数：')
        input_i_volume = int(input()) - 1

def images():
    dir_comic = title_search[input_i_comic].replace('/', ' ')
    if not os.path.exists(dir_comic):
        os.mkdir(dir_comic)
    os.chdir(dir_comic)

    print(title_volume[input_i_volume])
    print()
    print('正在下载...')
    browser = webdriver.PhantomJS()
    browser.get('http://manhua.dmzj.com' + link_volume[input_i_volume])
    tree_volume = etree.HTML(browser.page_source)
    url_image = tree_volume.xpath('//select[@id="page_select"]/option/@value')

    dir_volume = title_volume[input_i_volume].replace('/', ' ')
    if not os.path.exists(dir_volume):
        os.mkdir(dir_volume)
    else:
        exit()
    os.chdir(dir_volume)
    headers = {'Referer':'http://manhua.dmzj.com' + link_volume[input_i_volume]}

    name_image = []
    for i_image in range(0,len(url_image)):
        name_image.append(str(i_image) + '.jpg')
        get_image = requests.get(url_image[i_image], headers = headers)
        with open(name_image[i_image], 'wb') as fd:
            fd.write(get_image.content)

    os.chdir(os.path.dirname(os.path.abspath('.')))
    zip_volume = zipfile.ZipFile(dir_volume + '.zip', 'w')
    for i_image in range(0,len(url_image)):
            zip_volume.write('./' + dir_volume + '/' + name_image[i_image])

    print()
    print('下载完毕\n')


print('=' * 30)
print('动漫之家下载工具 Beta 1.0')
print('ssjgoku制作')
print('2017年11月4日')
print('输入"q"退出程序')
print('=' * 30)
print()
if input() == 'q':
    exit()
else:
    search()
    comic()
    if not os.path.exists('download'):
        os.mkdir('download')
    os.chdir('download')
    images()