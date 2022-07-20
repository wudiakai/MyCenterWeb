# encoding: utf-8

import xlrd
import util

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class TemplatesData:
    def __init__(self):
        self.__templates = {}

    def getTemplate(self, typeName):
        return self.__templates[typeName]

    def addTemplate(self, typeName, template):
        self.__templates[typeName] = template

    def dump(self):
        print(self.__templates)


class StrcutData:
    __KEY_STRUCT_NAME = 'struct name'
    __KEY_PROP_TYPE = 'prop type'
    __KEY_PROP_NAME = 'prop name'
    __KEY_PROP_VALUE = 'prop_value'
    __KEY_STRUCT_COMMENT = 'struct commets'
    __KEY_PROP_COMMENT = 'prop commets'
    # meta
    __KEY_STRUCT_PROPS = 'props'
    meta = {__KEY_STRUCT_NAME: "",
            __KEY_PROP_TYPE: __KEY_STRUCT_PROPS,
            __KEY_PROP_NAME: __KEY_STRUCT_PROPS,
            __KEY_PROP_VALUE: __KEY_STRUCT_PROPS,
            __KEY_STRUCT_COMMENT: "",
            __KEY_PROP_COMMENT: __KEY_STRUCT_PROPS,
            }

    def __init__(self):
        self.__datas = {'props': []}

    def setData(self, data):
        self.__datas = data

    def getName(self):
        return self.__datas[self.__KEY_STRUCT_NAME]

    def getComment(self):
        return self.__datas[self.__KEY_STRUCT_COMMENT]

    def getPropLines(self):
        propLines = ''
        props = self.__datas[self.__KEY_STRUCT_PROPS]
        propCount = len(props)
        propLines = ''
        for i in range(0, propCount):
            prop = props[i]
            propLines += '\n    '
            propLines += '/* '
            propLines += prop[self.__KEY_PROP_COMMENT]
            propLines += ' */\n    '
            propLines += prop[self.__KEY_PROP_TYPE]
            propLines += ' '
            propLines += prop[self.__KEY_PROP_NAME]
            propValue = prop[self.__KEY_PROP_VALUE]
            if propValue != '':
                propLines += ' = '
                propLines += str(propValue)
            propLines += ';\n'
        return propLines

    def dump(self):
        print(self.__datas)


class EnumData:
    # colums
    __KEY_NAME = 'enum name'
    __KEY_COMMENT = 'comments'
    __KEY_PROP_NAME = 'prop'
    __KEY_PROP_VALUE = 'prop value'
    __KEY_V_PROP_GROUP = 'VehiclePropertyGroup'
    __KEY_PROP_TYPE = 'VehiclePropertyType'
    __KEY_PROP_AREA = 'VehicleArea'
    __KEY_PROP_COMMENT = 'prop comment'
    # meta
    __KEY_PROPS = 'props'
    meta = {__KEY_NAME: "",
            __KEY_COMMENT: "",
            __KEY_PROP_NAME: __KEY_PROPS,
            __KEY_PROP_VALUE: __KEY_PROPS,
            __KEY_V_PROP_GROUP: __KEY_PROPS,
            __KEY_PROP_TYPE: __KEY_PROPS,
            __KEY_PROP_AREA: __KEY_PROPS,
            __KEY_PROP_COMMENT: __KEY_PROPS,
            }

    def __init__(self):
        self.__datas = {self.__KEY_PROPS: []}

    def __orValue__(self, propLines, prop, extraKey):
        extraData = prop[extraKey]
        if extraData != '':
            propLines += '|' + extraKey + '::' + str(extraData)
        return propLines

    def getMeta(self):
        return self.__meta

    def setData(self, datas):
        self.__datas = datas

    def getName(self):
        return self.__datas[self.__KEY_NAME]

    def getComment(self):
        if self.__KEY_COMMENT in self.__datas.keys():
            return self.__datas[self.__KEY_COMMENT]
        else:
            return ""

    def getPropLines(self):
        propLines = ''
        props = self.__datas[self.__KEY_PROPS]
        propCount = len(props)
        propLines = ''
        for i in range(0, propCount):
            prop = props[i]
            # comment
            propComment = prop[self.__KEY_PROP_COMMENT]
            if propComment != '':
                propLines += '    '
                lfCount = str(propComment).count("\n")
                util.dump(lfCount)
                propComment = str(propComment).replace("\n", "\n    ", lfCount)
                propLines += propComment
                propLines += '\n    '
            else:
                propLines += '    '
            # name
            propLines += prop[self.__KEY_PROP_NAME]
            # value
            propValue = prop[self.__KEY_PROP_VALUE]
            if propValue != '':
                propLines += ' = '
                propLines += str(propValue)
                propLines = self.__orValue__(
                    propLines, prop, self.__KEY_V_PROP_GROUP)
                propLines = self.__orValue__(
                    propLines, prop, self.__KEY_PROP_TYPE)
                propLines = self.__orValue__(
                    propLines, prop, self.__KEY_PROP_AREA)
            if i < propCount - 1:
                propLines += ';\n'
                propLines += '\n'
        return propLines

    def dump(self):
        print(self.__datas)


class DefaultConfigData:
    __KEY_NAME = 'prop'
    __KEY_ACCESS = 'access'
    __KEY_CHANGEMODE = 'changeMode'
    __KEY_AREACONFIGS = 'areaConfigs'
    __KEY_CONFIGARRAY = 'configArray'
    __KEY_CONFIGSTRING = 'configString'
    __KEY_MINSAMPLERATE = 'minSampleRate'
    __KEY_MAXSAMPLERATE = 'maxSampleRate'
    __KEY_INITVALUESTYPE = 'initValuesType'
    __KEY_INITVALUES = 'initialValue'
    meta = {__KEY_NAME: "",
            __KEY_ACCESS: "",
            __KEY_CHANGEMODE: "",
            __KEY_AREACONFIGS: "",
            __KEY_CONFIGARRAY: "",
            __KEY_CONFIGSTRING: "",
            __KEY_MINSAMPLERATE: "",
            __KEY_MAXSAMPLERATE: "",
            __KEY_INITVALUESTYPE: "",
            __KEY_INITVALUES: "",
            }

    def __init__(self):
        self.__datas = {}

    def __getInitValuesType(self):
        return self.__getOptionExpression(self.__KEY_INITVALUESTYPE)

    def __getOptionExpression(self, propName):
        result = self.__datas[propName]
        if result != '':
            result = '        .' + propName + ' = ' + str(result) + ','
        return result

    def setData(self, datas):
        self.__datas = datas

    def getName(self):
        return self.__datas[self.__KEY_NAME]

    def getAccess(self):
        return self.__datas[self.__KEY_ACCESS]

    def getChangeMode(self):
        return self.__datas[self.__KEY_CHANGEMODE]

    def getAreaConfigs(self):
        return self.__getOptionExpression(self.__KEY_AREACONFIGS)

    def getConfigArray(self):
        return self.__getOptionExpression(self.__KEY_CONFIGARRAY)

    def getConfigString(self):
        return self.__getOptionExpression(self.__KEY_CONFIGSTRING)

    def getMinSampleRate(self):
        return self.__getOptionExpression(self.__KEY_MINSAMPLERATE)

    def getMaxSampleRate(self):
        return self.__getOptionExpression(self.__KEY_MAXSAMPLERATE)

    def getInitValues(self):
        result = self.__datas[self.__KEY_INITVALUES]
        if result != '':
            result = "    .initialValue = {.%s = %s}," % (
                self.__datas[self.__KEY_INITVALUESTYPE], result)
        return result

    def dump(self):
        print(self.__datas)


class XlsParser:
    file = None

    def __init__(self, path):
        self.file = xlrd.open_workbook(path)
        print(self.file)

    def __getObjects(self, sheet, anchor):
        anchorCol = sheet.col_values(anchor[1], anchor[0] + 1, sheet.nrows)
        objects = list(filter(None, anchorCol))
        anchorCol = sheet.col_values(anchor[1], 0, sheet.nrows)
        objectsRange = []
        for i in range(0, len(objects)):
            rb = anchorCol.index(objects[i])
            objectsRange.append([rb, sheet.nrows - 1])
            if i > 0:
                objectsRange[i - 1][1] = rb - 1
                objectsRange[i][0] = rb
        return [objects, objectsRange]

    def __getMeta(self, objectType):
        if objectType == 'enum':
            return EnumData.meta
        elif objectType == 'struct':
            return StrcutData.meta
        elif objectType == 'DefaultConfigData':
            return DefaultConfigData.meta
        else:
            return None

    def __parseObjects(self, dataSheetName, meta, hasMultiLine=True):
        sheet = self.file.sheet_by_name(dataSheetName)
        anchor = [1, 1]  # for enum/struct col
        objectInfos = self.__getObjects(sheet, anchor)
        objects = objectInfos[0]
        objectsRange = objectInfos[1]
        headers = sheet.row_values(anchor[0], anchor[1], sheet.ncols)
        objectCount = len(objects)
        result = []
        for i in range(0, objectCount):
            singleObject = {headers[0]: objects[i]}
            rowb = objectsRange[i][0]
            rowe = objectsRange[i][1]
            for j in range(rowb, rowe + 1):
                # print("sheetrows#####################################")
                # print(sheet.ncols)
                valueRow = sheet.row_values(j, anchor[1] + 1, sheet.ncols)
                for k in range(0, len(valueRow)):
                    header = headers[k + 1]
                    cellValue = valueRow[k]
                    propName = meta[header]
                    if propName != '':
                        if propName not in singleObject.keys():
                            singleObject[propName] = []
                        if len(singleObject[propName]) < j - rowb + 1:
                            singleObject[propName].append({header: cellValue})
                        else:
                            singleObject[propName][j -
                                                   rowb].update({header: cellValue})
                    elif hasMultiLine is True:
                        # 如果多行均为空，则没该属性
                        if cellValue != '':
                            singleObject.update({header: cellValue})
                    else:
                        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        # print(header)
                        # print(cellValue)
                        singleObject.update({header: cellValue})
            result.append(singleObject)
        return result

    def __getDataObject(self, objectType):
        if objectType == 'enum':
            return EnumData()
        elif objectType == 'struct':
            return StrcutData()
        elif objectType == 'DefaultConfigData':
            return DefaultConfigData()
        else:
            return None

    def __paseData(self, dataSheetName, objectType, hasMultiLine=True):
        result = []
        meta = self.__getMeta(objectType)
        objects = self.__parseObjects(dataSheetName, meta, hasMultiLine)
        for i in range(0, len(objects)):
            objectData = self.__getDataObject(objectType)
            objectData.setData(objects[i])
            result.append(objectData)
        return result

    def parseStructData(self, dataSheetName):
        return self.__paseData(dataSheetName, 'struct')

    def parseEnumData(self, dataSheetName):
        return self.__paseData(dataSheetName, 'enum')

    def parseDefaultConfigData(self, dataSheetName):
        return self.__paseData(dataSheetName, 'DefaultConfigData', False)

    def parseTemplateData(self, templateNameSheet):
        result = TemplatesData()
        sheet = self.file.sheet_by_name(templateNameSheet)
        rowCount = sheet.nrows
        colSliceTypeNames = sheet.col_values(1, 2, rowCount)
        colSliceFormats = sheet.col_values(2, 2, rowCount)
        for i in range(0, len(colSliceTypeNames)):
            result.addTemplate(colSliceTypeNames[i], colSliceFormats[i])
        return result
