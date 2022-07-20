import pandas as pd
import csv
import os

FILENAME_INPUT = 'AndroidPF_Audio混音策略.xlsx'
FILENAME_CSV = 'temp1.csv'
FILENAME_XML = 'contexts_to_duck_configuration.xml'
PATH_OUT = 'out'


def xlsx_to_csv_pd():
    data_xls = pd.read_excel(FILENAME_INPUT, index_col=0)
    data_xls.to_csv(FILENAME_CSV, encoding='utf_8_sig')


def output(f, s):
    f.write(s + '\n')


def make_xml_file(ls):
    if ls[1][1] != 'ID':
        return 'fail'
    c_value = 1
    c_type = 2
    c_comment = len(ls[1]) - 4
    names = ls[1][3:c_comment]
    print(names)
    num = len(names)
    keymap = {}
    for line in ls:
        if line[c_type] in names:
            keymap[line[c_type]] = line[c_value]

    with open(PATH_OUT + os.sep + FILENAME_XML, 'w') as f:
        output(f, '<?xml version="1.0" encoding="utf-8"?>')
        output(f, '<contextsToDuckConfiguration>')
        output(f, '\t<contexts totalNumber="' + str(num) + '">')

        for line in ls:
            if line[c_type] in names:

                duck_num = 0
                duck_list = []
                for i in range(0, num):
                    strategy = line[i + 3]
                    if 'N' in strategy:
                        duck_num += 1
                        duck_list.append('\t\t\t<duck name="' + names[i] + '" macro="' + keymap[names[i]] + '"/>')

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


if __name__ == '__main__':
    xlsx_to_csv_pd()
    ls = []

    if not os.path.exists(PATH_OUT):
        print(' make dir')
        os.system('mkdir ' + PATH_OUT)

    with open(FILENAME_CSV, encoding='utf-8') as file:
        fin = csv.reader(file)
        for row in fin:
            ls.append(row)
    file.close()

    make_xml_file(ls)
    print('--------done--------')
