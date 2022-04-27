import os
import time
import tempfile

from fastapi import File

from tools import configutil
from tools.configutil import make_config


async def dispatcher(item: str, file: File):
    if item == 'config':
        if file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            path, file = await save_file(file, 'AndroidPF_Config.xlsx')
            return make_config(path, file)
        else:
            return 'file type error!'


async def get_out_file(session: str):
    return configutil.get_out_file(session)


async def save_file(file: File, name: str):
    contents = await file.read()
    folder = tempfile.gettempdir()
    filepath = os.path.join(folder, 'tmp_file', str(int(time.time())))
    print(filepath)
    filename = os.path.join(filepath, name)
    os.system('mkdir ' + filepath)
    # os.mkdir(filepath)
    with open(filename, 'wb') as f:
        f.write(contents)

    return filepath, name
