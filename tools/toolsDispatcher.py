import logging
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
            print(' config file type error!')
            logging.log(logging.ERROR, 'config file type error!')
            return 'file type error!'
    elif item == 'vhal':
        if file.content_type == 'application/vnd.ms-excel':
            try:
                path, file = await save_file(file, 'vhal_config.xls')
                input = os.path.join(path, file)
                PATH = './tools/shell/' + item
                out_path = path
                cmd = "python " + PATH + os.sep + "vhal_main.py " + input + " " + out_path
                os.system(cmd)
                os.remove(input)

                configutil.zip_files(out_path, 'vhal')
                configutil.out_files['vhal'] = os.path.join(out_path, 'vhal.zip')
                return 'OK'
            except Exception as e:
                print(' vhal  generate failed!' + str(e))
                logging.log(logging.ERROR, 'vhal  generate failed!' + str(e))
                return "NG"
        else:
            print(' vhal file type error!')
            logging.log(logging.ERROR, 'vhal file type error!')
            return 'file type error!'
    elif item == 'audiofocus':
        if file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            try:
                path, file = await save_file(file, 'AndroidPF_Audio焦点管理策略.xlsx')
                input = os.path.join(path, file)
                PATH = './tools/shell/audioConfig/'
                out_path = path
                cmd = "python " + PATH + os.sep + "audioFocus.py " + input + " " + out_path
                os.system(cmd)
                os.remove(input)

                configutil.zip_files(out_path, 'audiofocus')
                configutil.out_files['audiofocus'] = os.path.join(out_path, 'audiofocus.zip')
                return 'OK'
            except Exception as e:
                print(' audioFoucs  generate failed!' + str(e))
                logging.log(logging.ERROR, 'audioFoucs  generate failed!' + str(e))
                return "NG"
        else:
            print(' config file type error!')
            logging.log(logging.ERROR, 'config file type error!')
            return 'file type error!'
    elif item == 'audiomix':
        if file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            try:
                path, file = await save_file(file, 'AndroidPF_Audio焦点管理策略.xlsx')
                input = os.path.join(path, file)
                PATH = './tools/shell/audioConfig/'
                out_path = path
                cmd = "python " + PATH + os.sep + "audiomix_2.py " + input + " " + out_path
                os.system(cmd)
                os.remove(input)

                configutil.zip_files(out_path, 'audiomix')
                configutil.out_files['audiomix'] = os.path.join(out_path, 'audiomix.zip')
                return 'OK'
            except Exception as e:
                print(' audiomix  generate failed!' + str(e))
                logging.log(logging.ERROR, 'audiomix  generate failed!' + str(e))
                return "NG"
        else:
            print(' config file type error!')
            logging.log(logging.ERROR, 'config file type error!')
            return 'file type error!'


async def get_out_file(session: str):
    return configutil.get_out_file(session)


async def save_file(file: File, name: str):
    contents = await file.read()
    folder = tempfile.gettempdir()
    filepath = os.path.join(folder, 'tmp_file', str(int(time.time())))
    filename = os.path.join(filepath, name)
    if filepath != '' and not os.path.exists(filepath):
        os.system('mkdir -p ' + filepath)
    # os.mkdir(filepath)
    with open(filename, 'wb') as f:
        f.write(contents)

    return filepath, name
