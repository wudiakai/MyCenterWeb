# encoding: utf-8

import sys
import tempfile
import time

import pandas as pd
import csv
import os

FILENAME_INPUT = 'AndroidPF_AudioFocus.xlsx'
FILENAME_CSV = 'temp.csv'
FILENAME_XML = 'interaction_matrix_configuration.xml'
g_out_path = ''


def xlsx_to_csv_pd(fileInput, outFolder):
    data_xls = pd.read_excel(fileInput, index_col=0)
    data_xls.to_csv(outFolder + os.sep + FILENAME_CSV, encoding='utf_8_sig')


def output(f, s):
    f.write(s + '\n')


# 策略转换
def change_action(strategy):
    if strategy == 'I':
        return 0, 'INTERACTION_REJECT'
    elif strategy == 'R' or strategy == 'N':
        return 1, 'INTERACTION_EXCLUSIVE'
    elif strategy == 'D':
        return 2, 'INTERACTION_CONCURRENT'
    else:
        return 0, 'INTERACTION_REJECT'


def make_xml_file(ls, outFolder):
    if ls[1][1] != 'Context':
        return 'fail'
    c_comment = len(ls[1]) - 1
    c_type = 1
    names = ls[1][2:c_comment]
    num = len(names)
    with open(outFolder + os.sep + FILENAME_XML, 'w') as f:
        output(f, '<?xml version="1.0" encoding="utf-8"?>')
        output(f, '<interactionMatrixConfiguration>')
        output(f, '\t<focusHolders totalNumber="' + str(num) + '">')

        for line in ls:
            if line[c_type] in names:
                output(f, '\t\t<focusHolder name="' + line[c_type] + '">')
                for i in range(0, num):
                    strategy = line[i + 2]
                    res, comment = change_action(strategy)
                    output(f, '\t\t\t<focusRequester name="' + names[
                        i] + '" interactionResult="' + str(res) + '"/>  <!--' + comment + '-->')
                output(f, '\t\t</focusHolder>')

        output(f, '\t</focusHolders>')
        output(f, '</interactionMatrixConfiguration>')
    pass


def makeFolder():
    global g_out_path
    folder = tempfile.gettempdir()
    g_out_path = os.path.join(folder, 'tmp_file', str(int(time.time()))) + os.sep
    if not os.path.exists(g_out_path):
        os.system('mkdir -p ' + g_out_path)


def main():
    global g_out_path
    if len(sys.argv) > 1:
        file = sys.argv[1]
        if len(sys.argv) > 2:
            g_out_path = sys.argv[2]
    else:
        print("请指定转换文件!")
        return

    if len(g_out_path) < 2:
        makeFolder()

    if not os.path.exists(g_out_path):
        print(' make dir')
        os.system('mkdir ' + g_out_path)

    xlsx_to_csv_pd(file, g_out_path)
    ls = []

    with open(g_out_path + os.sep + FILENAME_CSV) as file:
        fin = csv.reader(file)
        for row in fin:
            ls.append(row)
    file.close()

    make_xml_file(ls, g_out_path)
    os.remove(g_out_path + os.sep + FILENAME_CSV)
    print('--------done--------')


if __name__ == '__main__':
    main()
