# encoding: utf-8

from CppHeaderParser import CppHeader
import xlwt
import os
import sys
import re

sys.path = ["../"] + sys.path
# try:
#     cppHeader = CppHeader(r"input/types.hal", encoding='utf-8')
# except CppParseError as e:
#     print(e)
#     sys.exit(1)


class Cpp2Xls:
    __NAME = 'enum name'
    __COMMENT = 'comments'
    __PCOMMENT = 'prop comment'
    __PNAME = 'prop'
    __PVALUE = 'prop value'
    __VGROUP = 'VehiclePropertyGroup'
    __VTYPE = 'VehiclePropertyType'
    __VAREA = 'VehicleArea'
    __colName = [__NAME, __PNAME,
                 __PVALUE, __VGROUP, __VTYPE, __VAREA, __PCOMMENT, __COMMENT]

    def __init__(self):
        self.__cols = dict(
            (zip(self.__colName, range(1, len(self.__colName) + 1))))

    def __openFile(self, outputFile):
        if os.access(outputFile, os.F_OK) is True:
            os.remove(outputFile)
        outputXls = xlwt.Workbook(encoding='utf-8')
        return outputXls

    def __generateHeaders(self, sheet, row):
        for x in self.__colName:
            sheet.write(row, self.__cols[x], x)

    def __fillName(self, enum, sheet, row):
        nameCol = self.__cols[self.__NAME]
        sheet.write(row, nameCol, enum["name"])

    def __fileComment(self, enum, sheet, row, propCount):
        commentCol = self.__cols[self.__COMMENT]
        doxygen = ''
        if 'doxygen' in enum.keys():
            doxygen = enum["doxygen"]
        sheet.write_merge(row, row + propCount - 1,
                          commentCol, commentCol, doxygen)

    def __fillPropComment(self, prop, sheet, row):
        if 'doxygen' in prop.keys():
            doxygen = prop["doxygen"]
            sheet.write(row, self.__cols[self.__PCOMMENT], doxygen)
        sheet.write(row, self.__cols[self.__PNAME], prop["name"])

    def __isVihicleProp(self, value):
        svalue = str(value)
        if svalue.find(self.__VGROUP) >= 0 or svalue.find(self.__VTYPE) >= 0 or svalue.find(self.__VAREA) >= 0:
            return True
        else:
            return False

    def __getRawDataRealValue(self, value):
        if self.__isVihicleProp(value) is False:
            return value
        ret = str(value).replace('(', '')
        ret = str(ret).replace(')', '')
        ret = str(ret).split('|')
        return str(ret[0]).strip()

    def __fillPropValue(self, prop, sheet, row):
        value = ''
        if 'raw_value' in prop.keys():
            value = prop["raw_value"]
            sheet.write(row, self.__cols[self.__PVALUE], value)
        else:
            value = prop["value"]
            realValue = self.__getRawDataRealValue(value)
            sheet.write(row, self.__cols[self.__PVALUE], realValue)
            if isinstance(value, str):
                self.__fillPropValueInfos(value, sheet, row)

    def __fillPropValueInfos(self, value, sheet, row):
        vinfo = re.findall(
            r"VehiclePropertyGroup : (\w+)", value, re.IGNORECASE)
        if vinfo != None and len(vinfo) > 0:
            sheet.write(row, self.__cols[self.__VGROUP], vinfo[0])
        vinfo = re.findall(r"VehiclePropertyType : (\w+)",
                           value, re.IGNORECASE)
        if vinfo != None and len(vinfo) > 0:
            sheet.write(row, self.__cols[self.__VTYPE], vinfo[0])
        vinfo = re.findall(r"VehicleArea : (\w+)", value, re.IGNORECASE)
        if vinfo != None and len(vinfo) > 0:
            sheet.write(row, self.__cols[self.__VAREA], vinfo[0])

    def generate(self, inputFile, outputFile):
        cppHeader = CppHeader(r"input/types.hal", encoding='utf-8')
        # open file
        outputXls = self.__openFile(outputFile)
        # add a sheet
        sheet0 = outputXls.add_sheet("enums")
        row_b = 1
        self.__generateHeaders(sheet0, row_b)
        propRow = row_b + 1
        for enum in cppHeader.enums:
            propCount = len(enum['values'])
            if propCount == 0:
                continue
            # col:name
            self.__fillName(enum, sheet0, propRow)
            # col:comments
            self.__fileComment(enum, sheet0, propRow, propCount)
            # props
            for prop in enum['values']:
                # col:prop comment
                self.__fillPropComment(prop, sheet0, propRow)
                # col: prop_value ,vgroup,vtye,varea
                self.__fillPropValue(prop, sheet0, propRow)
                propRow += 1
        outputXls.save(outputFile)


cpp2xls = Cpp2Xls()
cpp2xls.generate(r"input/types.hal", r'output/test2.xls')

sys.exit(0)
