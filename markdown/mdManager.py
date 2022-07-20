import logging
import os.path
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import re

from constant import BASE_URL
from dao.models import MyMarkdown

TIME_INTERVAL = 30 * 60  # 30 minutes
loop = None
scheduler = None


async def update_database(root: str, file: str):
    # print('------------------updateDatabase----------root:--', root, '  file:', file)
    filepath = os.path.join(root, file)
    mtime = get_file_m_time(filepath)
    filename = get_file_name(file)
    res = await MyMarkdown.filter(name=filename)
    need = ''  # 是否插入/更新数据库
    if len(res) == 0:  # 不存在则插入
        need = 'create'

    else:
        if res[0].last_modify != mtime:
            need = 'update'
        else:
            print('[', filename, '] is already up to date.')
            logging.log(logging.INFO, '[' + filename + '] is already up to date.')
            pass

    if need == 'create':
        s = read_markdown_file(filepath)
        print('create [', filename, '] data.  length=' + str(len(s)))
        logging.log(logging.INFO, 'create [' + filename + '] data.  length=' + str(len(s)))
        try:
            await MyMarkdown(name=get_file_name(file),
                             last_modify=mtime,
                             content=s).save()
        except Exception as e:
            print('【Error】 ' + filename + ' create db failed!   length = ' + str(len(s)))
            logging.log(logging.ERROR, filename + ' create db failed!   length = ' + str(len(s)))
    elif need == 'update':
        s = read_markdown_file(filepath)
        data = {
            "id": res[0].id,
            'name': get_file_name(file),
            'content': s,
            'last_modify': mtime

        }
        logging.log(logging.INFO, '[' + filename + '] has been updated.')
        print('[', filename, '] has been updated.')

        await MyMarkdown(**data).save(force_update=True)


async def sync_svn():
    print('------------sync svn------------------')
    logging.log(logging.INFO, '------------sync svn------------------')
    os.system("sh ./markdown/sync.sh")
    tasks = []
    for root, dirs, files in os.walk("./markdown/md/"):
        for file in files:
            if '.md' in file:
                await update_database(root, file)


def get_file_m_time(file: str):
    return os.stat(file).st_mtime


def get_file_name(name: str):
    return os.path.splitext(name)[0]


def run_sync_scheduled():
    global loop
    asyncio.run_coroutine_threadsafe(sync_svn(), loop)


def start_timer():
    global scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_sync_scheduled, 'interval', seconds=TIME_INTERVAL)
    scheduler.start()


async def refresh():
    await sync_svn()


async def get_data_by_name(name: str):
    res = await MyMarkdown().filter(name=name).first()
    res.content = filter_img(res.content)
    res.content = filter_img2(res.content)
    res.content = filter_video(res.content)
    return res


def filter_img(data: str):
    src = re.compile(r"\(.*(?:image/|image\\)")

    return src.sub("(" + BASE_URL + "/img/", data)


def filter_img2(data: str):
    src = re.compile(r"\".*(?:image/|image\\)")

    return src.sub("\"" + BASE_URL + "/img/", data)


# def filter_img(data: str):
#     src = re.compile("\(.*/image")
#
#     return src.sub("(" + BASE_URL + "/img", data)


def filter_video(data: str):
    src = re.compile("<video")
    return src.sub("<video width=\"100%\"", data)


def read_markdown_file(name: str):
    file = name
    if os.path.exists(file):
        f = open(file, encoding='utf-8')
        return f.read()
    else:
        return ""


def read_markdown_list(item: str):
    files = {
        'module': './markdown/md/_modulelist.txt',
        'feature': './markdown/md/_featureList.txt',
    }

    file = files[item]
    return read_markdown_list_file(file)


def read_markdown_list_file(file: str):
    if os.path.exists(file):
        lst = []

        sublst = []
        for line in open(file, encoding='utf-8'):
            line = line.replace('\n', '')
            if line.startswith('--'):
                sublst.append(line.replace('-', ''))
            else:
                if len(sublst) > 0:
                    index = len(lst) - 1
                    lst[index]['sublist'] = sublst
                    lst[index]['submenu'] = True
                    sublst = []
                map1 = {'submenu': False, 'title': line}
                lst.append(map1)

        if len(sublst) > 0:
            index = len(lst) - 1
            lst[index]['sublist'] = sublst
            lst[index]['submenu'] = True
            sublst = []

        print('list :' + str(lst))
        logging.log(logging.INFO, 'list :' + str(lst))
        return lst

    else:
        return ""


async def search(text):
    res = await MyMarkdown().filter(name__icontains=text)
    print(res)
    for a in res:
        print(a.name)
    return res


def init():
    global loop
    loop = asyncio.get_event_loop()
    start_timer()
