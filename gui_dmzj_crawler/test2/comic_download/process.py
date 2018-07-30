import requests
import json
import multiprocessing as mp
import os
import concurrent.futures
import asyncio
import aiohttp


headers = {'Referer': 'http://imgsmall.dmzj.com/'}
global all_tasks
all_tasks = []
global num_tasks
global q1
global q2
q1 = mp.Queue()
q2 = mp.Queue()


def chap_info():
    """下载队列"""

    task = q1.get(True)
    task['state'] = 0
    q2.put(task)
    path_init = os.path.abspath('.')
    os.chdir('./download')

    comic = task['comic'].replace('/', ' ')
    chap = task['chap'].replace('/', ' ')
    if not os.path.exists('./' + comic):
        os.mkdir(comic)
    os.chdir(comic)
    if not os.path.exists('./' + chap):
        os.mkdir(chap)
    os.chdir(chap)

    url = task['url']
    r = requests.get(url)
    # print(r.status_code)
    r_json = r.json()
    page_num = r_json['picnum']
    task['page_num'] = page_num
    page_urls = r_json['page_url']
    progress = 0
    task['state'] = 1
    q2.put(task)

    image_tasks = [image_dl(page_url, task) for page_url in page_urls]
    image_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(image_loop)
    image_loop.run_until_complete(asyncio.wait(image_tasks))

    if progress == page_num:
        task['state'] = 2
        q2.put(task)

    os.chdir(path_init)


async def image_dl(url, task):
    """下载每页图片"""

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as get_image:
            filename = os.path.basename(url)
            image = await get_image.read()
            with open(filename, 'wb') as f:
                f.write(image)
            task['progress'] += 1
            if task['progress'] == task['page_num']:
                task['state'] = 2
            q2.put(task)


def task_upd():
    task = q2.get()
    return task
