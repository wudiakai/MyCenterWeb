import logging

import pandas as pd
import csv
import zipfile
import os

# constant var ##############
# column define
C_CATEGORY = 3
C_COMMENT = 4
C_TYPE = 5
C_KEY = 6
C_VALUE = 11

#
FILENAME_INPUT = 'AndroidPF_Config.xlsx'
FILENAME_CSV = 'temp.csv'
FILENAME_JSON = 'neu_config.json'
FILENAME_RC = 'init.neu.prop.rc'
FILENAME_MAP = 'ConfigMap.java'
PATH_OUT = 'out'

# global var
status = None
out_files = {}


def xlsx_to_csv_pd(path, file):
    data_xls = pd.read_excel(os.path.join(path, file), index_col=0)
    data_xls.to_csv(os.path.join(path, FILENAME_CSV), encoding='utf_8_sig')


def output(f, s):
    f.write(s + '\n')


def filter_str(s):
    return s.lower().strip()


def wrap_value(type, val):
    if type == 'string':
        val = val.replace("\n", "|")
        return "\"" + val + "\""
    else:
        return val


# main
# generate json config
def make_json_file(ls, out_path):
    with open(out_path + os.sep + FILENAME_JSON, 'w') as f:
        output(f, '{')
        for line in ls:
            if filter_str(line[C_CATEGORY]) == 'json':
                str = "\t\"" + filter_str(line[C_KEY]) + "\":" + wrap_value(filter_str(line[C_TYPE]),
                                                                            line[C_VALUE]).strip() + ","
                output(f, str)
        output(f, '\t"" : ""')
        output(f, '}')


#   generate java  map config
def make_java_mapFile(ls, out_path):
    with open(out_path + os.sep + FILENAME_MAP, 'w') as f:
        output(f, 'package com.neu.config.data;')
        output(f, 'import java.util.HashMap;')
        output(f, "")
        output(f, "public class ConfigMap {")
        output(f, "    public HashMap<String, Object> configMap = new HashMap<String, Object>(){{")
        for line in ls:
            if filter_str(line[C_CATEGORY]) == 'json':
                str = "\t\tput(\"" + filter_str(line[C_KEY]) + "\"," + wrap_value(filter_str(line[C_TYPE]),
                                                                                  line[C_VALUE]).strip() + ");"
                output(f, str)
        output(f, '    }};')
        output(f, '}')
    pass


def make_rc_file(ls, out_path):
    with open(out_path + os.sep + FILENAME_RC, 'w') as f:
        output(f, 'on fs:')
        for line in ls:
            if filter_str(line[C_CATEGORY]) == 'property':
                str = "\tsetprop " + filter_str(line[C_KEY]) + " " + line[C_VALUE]
                output(f, str)
        output(f, '')
    pass


def zip_files(path: str, name):
    zip_file = zipfile.ZipFile(os.path.join(path, name + '.zip'), 'w')
    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.endswith('zip'):
                zip_file.write(os.path.join(root, file), file)
    zip_file.close()


def get_out_file(session: str):
    logging.log(logging.INFO, 'session :' + session)
    print(session)
    global out_files
    return out_files[session]


def make_config(path: str, file: str):
    xlsx_to_csv_pd(path, file)
    ls = []

    out_path = os.path.join(path, PATH_OUT)
    print('------------------------' + out_path)
    if out_path != '' and not os.path.exists(out_path):
        os.system('mkdir -p ' + out_path)

    temp_file = os.path.join(path, FILENAME_CSV)
    is_config_file = False
    with open(temp_file, encoding='utf_8_sig') as file:
        fin = csv.reader(file)
        for row in fin:
            ls.append(row)
    file.close()

    if ls[2][C_CATEGORY] != '配置类型':
        return 'incorrect file!'

    make_json_file(ls, out_path)
    make_java_mapFile(ls, out_path)
    make_rc_file(ls, out_path)

    zip_files(out_path, 'config')
    global out_files
    out_files['config'] = os.path.join(out_path, 'config.zip')

    return 'OK'


if __name__ == '__main__':
    # if len(sys.argv) > 1:
    #     fn = sys.argv[1]
    # else:
    #     return

    make_config('./', FILENAME_INPUT)
