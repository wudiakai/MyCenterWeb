import os.path
import threading
import asyncio

from dao.models import MyMarkdown

TIME_INTERVAL = 30 * 60  # 30 minutes


async def update_database(root: str, file: str):
    # print('------------------updateDatabase----------root:--', root, '  file:', file)
    filepath = os.path.join(root, file)
    mtime = get_file_m_time(filepath)
    filename = get_file_name(file)
    res = await MyMarkdown.filter(name=filename)
    need: bool = False  # 是否插入/更新数据库
    if len(res) == 0:  # 不存在则插入
        need = True
        print('create', filename, 'data')
    else:
        # print("time:", mtime, " last:", res[0].last_modify)
        if res[0].last_modify != mtime:
            need = True
            print(filename, 'The update has been written to the database.')
        else:
            print(filename, 'is already up to date.')
            pass

    if need:
        str = read_markdown_file(filepath)
        # print('content', str)
        await MyMarkdown(name=get_file_name(file),
                         last_modify=mtime,
                         content=str).save()


async def sync_svn():
    print('------------sync svn------------------')
    # os.system("sh ./markdown/sync.sh")
    tasks = []
    for root, dirs, files in os.walk("./markdown/md/"):
        for file in files:
            if '.md' in file:
                await update_database(root, file)
                # task = updateDatabase(root, file)
                # tasks.append(task)

    # global loop
    # if len(tasks) > 0:
    # loop.run_until_complete(asyncio.wait(tasks))
    # for t in tasks:
    #     task = loop.create_task(t)
    #     loop.run_until_complete(task)
    # loop.close()


def get_file_m_time(file: str):
    return os.stat(file).st_mtime


def get_file_name(name: str):
    return os.path.splitext(name)[0]


# def runSyncScheduled():
#     # run_task(syncSvn)
#     syncSvn()
#     threading.Timer(TIME_INTERVAL, runSyncScheduled).start()


# def run_task(task):
#     asyncio.run(task())
# loop = asyncio.new_event_loop()
# # loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
# loop.run_until_complete(task)
# loop.close()


async def refresh():
    await sync_svn()


async def get_data_by_name(name: str):
    res = await MyMarkdown().filter(name=name).first()
    # print(res)
    return res


# def init(lo):
#     print('mdmanager init')
#     global loop
#     loop = lo
#     asyncio.set_event_loop(loop)
#     threading.Timer(30, runSyncScheduled).start()


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
    }

    file = files[item]
    return read_markdown_list_file(file)


def read_markdown_list_file(file: str):
    if os.path.exists(file):
        lst = []
        index = 0

        sublst = []
        for line in open(file, encoding='utf-8'):
            # line = f.readline()
            line = line.replace('\n', '')
            if (line.startswith('--')):
                sublst.append(line.replace('-', ''))
            else:
                if len(sublst) > 0:
                    index = len(lst) - 1
                    lst[index]['sublist'] = sublst
                    lst[index]['submenu'] = True
                    sublst = []
                map = {}
                map['submenu'] = False
                map['title'] = line
                lst.append(map)

        if len(sublst) > 0:
            index = len(lst) - 1
            lst[index]['sublist'] = sublst
            lst[index]['submenu'] = True
            sublst = []

        print(lst)
        return lst

    else:
        return ""


async def search(text):
    res = await MyMarkdown().filter(name__icontains=text)
    print(res)
    for a in res:
        print(a.name)
    return res