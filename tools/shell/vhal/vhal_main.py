# encoding: utf-8

import sys, os

sys.path.append('/')

import xls2cpp
import xlsparser
import util
import generalCode
import time
import tempfile

from string import Template

g_out_path = ''


def generateCppFileEn(xlsPath, outPath, dataSheetName, templateNameSheet):
    xlsParser = xlsparser.XlsParser(xlsPath)
    enumDatas = xlsParser.parseEnumData(dataSheetName)
    util.dumpAll(enumDatas)
    tmplates = xlsParser.parseTemplateData(templateNameSheet)
    tmpl = Template(tmplates.getTemplate("enum_hal"))
    print('--------------------------------------------')
    generator = xls2cpp.CppHeaderGenerator(outPath, None)
    generator.generateEnums(enumDatas, tmpl)
    generator.end()


def generateCppFileSt(xlsPath, outPath, dataSheetName, templateNameSheet):
    xlsParser = xlsparser.XlsParser(xlsPath)
    structDatas = xlsParser.parseStructData(dataSheetName)
    for i in range(0, len(structDatas)):
        structDatas[i].dump()
    tmplates = xlsParser.parseTemplateData(templateNameSheet)
    tmpl = Template(tmplates.getTemplate("struct"))
    print('--------------------------------------------')
    generator = xls2cpp.CppHeaderGenerator(outPath, None)
    generator.generateStructs(structDatas, tmpl)
    generator.end()


def generateDefaultConfigs(xlsPath, outPath, dataSheetName, templateNameSheet):
    xlsParser = xlsparser.XlsParser(xlsPath)
    dcDatas = xlsParser.parseDefaultConfigData(dataSheetName)
    util.dumpAll(dcDatas)
    tmplates = xlsParser.parseTemplateData(templateNameSheet)
    tmpl = Template(tmplates.getTemplate("default_config"))
    print('--------------------------------------------')
    generator = xls2cpp.CppHeaderGenerator(outPath, None)
    generator.generateDefaultConfigs(dcDatas, tmpl)
    generator.end()


def generateModuleConfigs(xlsPath, outPath, dataSheetName, templateNameSheet):
    xlsParser = xlsparser.XlsParser(xlsPath)
    dcDatas = xlsParser.parseDefaultConfigData(dataSheetName)
    util.dumpAll(dcDatas)
    tmplates = xlsParser.parseTemplateData(templateNameSheet)
    tmpl = Template(tmplates.getTemplate("module_config"))
    print('--------------------------------------------')
    generator = xls2cpp.CppHeaderGenerator(outPath, None)
    generator.generateDefaultConfigs(dcDatas, tmpl)
    generator.end()


def makeFolder():
    global g_out_path
    folder = tempfile.gettempdir()
    g_out_path = os.path.join(folder, 'tmp_file', str(int(time.time())))



def outFolder():
    global g_out_path
    return g_out_path


def generateTypesHal(xls):
    i = xls
    o = outFolder() + r'test.hal'
    dataSheet = 'types.hal'
    tmepSheet = 'templates'
    generateCppFileEn(i, o, dataSheet, tmepSheet)


def generateSt(xls):
    i = xls
    o = outFolder() + r'testSt.h'
    dataSheet = 'struct'
    tmepSheet = 'templates'
    generateCppFileSt(i, o, dataSheet, tmepSheet)


def generateDefaultConfig(xls):
    i = xls
    o = outFolder() + r'DefaultConfig.h'
    dataSheet = 'DefaultConfig.h'
    tmepSheet = 'templates'
    generateDefaultConfigs(i, o, dataSheet, tmepSheet)


def generateModuleConfig(xls):
    i = xls
    o = outFolder() + r'ModuleConfig.h'
    dataSheet = 'DefaultConfig.h'
    tmepSheet = 'templates'
    generateModuleConfigs(i, o, dataSheet, tmepSheet)


def generateModule(csv):
    i = csv

    generalCode.generateDefaultModules(i)


def gene_xls(xls):
    os.system("del /F /Q " + outFolder() + "output" + os.sep + "*")
    generateTypesHal(xls)
    generateSt(xls)
    generateDefaultConfig(xls)
    generateModuleConfig(xls)
    return 'output'


def main():
    ls = []
    file = ''
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
    path = gene_xls(file)

    print(g_out_path)
    return g_out_path


if __name__ == '__main__':
    main()
