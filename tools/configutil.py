import pandas as pd
import csv
import sys
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


def xlsx_to_csv_pd():
    data_xls = pd.read_excel(FILENAME_INPUT, index_col=0)
    data_xls.to_csv(FILENAME_CSV, encoding='utf_8_sig')


def output(f, s):
    f.write(s + '\n')


def filterStr(s):
    return s.lower().strip()


def wrapValue(type, val):
    if type == 'string':
        val = val.replace("\n","|")
        return "\"" + val + "\""
    else:
        return val


# main
#   generate json config
def makeJsonFile(ls):
    with open(PATH_OUT + os.sep + FILENAME_JSON, 'w') as f:
        output(f, '{')
        for line in ls:
            if filterStr(line[C_CATEGORY]) == 'json':
                str = "\t\"" + filterStr(line[C_KEY]) + "\":" + wrapValue(filterStr(line[C_TYPE]),
                                                                          line[C_VALUE]).strip() + ","
                output(f, str)
        output(f, '\t"" : ""')
        output(f, '}')


#   generate java  map config
def makeJavaMapFile(ls):
    with open(PATH_OUT + os.sep + FILENAME_MAP, 'w') as f:
        output(f, 'package com.neu.config.data;')
        output(f, 'import java.util.HashMap;')
        output(f, "")
        output(f, "public class ConfigMap {")
        output(f, "    public HashMap<String, Object> configMap = new HashMap<String, Object>(){{")
        for line in ls:
            if filterStr(line[C_CATEGORY]) == 'json':
                str = "\t\tput(\"" + filterStr(line[C_KEY]) + "\"," + wrapValue(filterStr(line[C_TYPE]),
                                                                                line[C_VALUE]).strip() + ");"
                output(f, str)
        output(f, '    }};')
        output(f, '}')
    pass


def makeRCFile(ls):
    with open(PATH_OUT + os.sep + FILENAME_RC, 'w') as f:
        output(f, 'on fs:')
        for line in ls:
            if filterStr(line[C_CATEGORY]) == 'property':
                str = "\tsetprop " + filterStr(line[C_KEY]) + " " + line[C_VALUE]
                output(f, str)
        output(f, '')
    pass


if __name__ == '__main__':
    # if len(sys.argv) > 1:
    #     fn = sys.argv[1]
    # else:
    #     return

    xlsx_to_csv_pd()
    ls = []

    if not os.path.exists(PATH_OUT):
        print(' make dir')
        os.system('mkdir ' + PATH_OUT)

    with open(FILENAME_CSV) as file:
        fin = csv.reader(file)
        for row in fin:
            ls.append(row)
    file.close()

    makeJsonFile(ls)
    makeJavaMapFile(ls)
    makeRCFile(ls)
