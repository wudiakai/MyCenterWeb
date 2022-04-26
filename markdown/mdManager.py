import os.path
import threading
import asyncio

from dao.models import MyMarkdown

TIME_INTERVAL = 30 * 60  # 30 minutes
global loop


async def getList():
    return await MyMarkdown().all()


async def updateDatabase(root: str, file: str):
    # print('------------------updateDatabase----------root:--', root, '  file:', file)
    filepath = os.path.join(root, file)
    mtime = getFileMtime(filepath)
    filename = getFileName(file)
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
        str = read_markdown(filepath)
        # print('content', str)
        await MyMarkdown(name=getFileName(file),
                         last_modify=mtime,
                         content=str).save()


async def syncSvn():
    print('------------sync svn------------------')
    # os.system("sh ./markdown/sync.sh")
    tasks = []
    for root, dirs, files in os.walk("./markdown/md/"):
        for file in files:
            if '.md' in file:
                await updateDatabase(root, file)
                # task = updateDatabase(root, file)
                # tasks.append(task)

    # global loop
    # if len(tasks) > 0:
    # loop.run_until_complete(asyncio.wait(tasks))
    # for t in tasks:
    #     task = loop.create_task(t)
    #     loop.run_until_complete(task)
    # loop.close()


def getFileMtime(file: str):
    return os.stat(file).st_mtime


def getFileName(name: str):
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
    await syncSvn()


# def init(lo):
#     print('mdmanager init')
#     global loop
#     loop = lo
#     asyncio.set_event_loop(loop)
#     threading.Timer(30, runSyncScheduled).start()


def read_markdown(name: str):
    file = name
    if os.path.exists(file):
        f = open(file, encoding='utf-8')
        return f.read()
    else:
        return ""


async def getDataByName(name: str):
    res = await MyMarkdown().filter(name=name).first()
    # print(res)
    return res
