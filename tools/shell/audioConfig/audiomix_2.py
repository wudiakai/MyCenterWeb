# encoding: utf-8
import sys
import tempfile
import time

import pandas as pd
import csv
import os

FILENAME_INPUT = 'AndroidPF_Audio混音策略.xlsx'
FILENAME_CSV = 'temp.csv'
FILENAME_XML = 'contexts_to_duck_configuration.xml'
g_out_path = ''


def xlsx_to_csv_pd(fileInput, outFolder):
    data_xls = pd.read_excel(fileInput, index_col=0)
    data_xls.to_csv(outFolder + os.sep + FILENAME_CSV, encoding='utf_8_sig')


def output(f, s):
    f.write(s + '\n')


def make_xml_file(ls, outFolder):
    if ls[1][1] != 'ID':
        return 'fail'
    c_value = 1
    c_type = 2
    c_comment = len(ls[1]) - 4
    c_volumeType = len(ls[1]) - 2
    names = ls[1][3:c_comment]
    print(names)
    num = len(names)
    volumeType = ls[2][c_volumeType]
    print(volumeType)
    keymap = {}
    for line in ls:
        if line[c_type] in names:
            keymap[line[c_type]] = line[c_value]

    with open(outFolder + os.sep + FILENAME_XML, 'w') as f:
        output(f, '<?xml version="1.0" encoding="utf-8"?>')
        output(f, '<contextsToDuckConfiguration>')
        output(f, '\t<contexts totalNumber="' + str(num) + '" volumetype="' + volumeType + '">')

        for line in ls:
            if line[c_type] in names:

                duck_num = 0
                duck_list = []
                for i in range(0, num):
                    strategy = line[i + 3]
                    if 'N' in strategy:
                        duck_num += 1
                        volume = strategy.replace('N', '').strip()
                        duck_list.append('\t\t\t<duck name="' + names[i] + '" macro="' + keymap[
                            names[i]] + '" volume="' + volume + '"/>')

                output(f, '\t\t<context name="' + line[c_type] + '" macro="' + line[
                    c_value] + '" numberOfCanDuck="' + str(duck_num) + '">')
                for s in duck_list:
                    output(f, s)
                if duck_num == 0:
                    output(f, '\t\t\t<!--' + line[c_type] + ' ducks nothing-->')
                output(f, '\t\t</context>')

        output(f, '\t</contexts>')
        output(f, '</contextsToDuckConfiguration>')
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
