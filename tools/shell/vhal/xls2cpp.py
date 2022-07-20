# encoding: utf-8

import re

class CppHeaderGenerator:
    __outputPath = ''
    __headerFile = None

    def __init__(self, __outputPath, template):
        self.__outputPath = __outputPath
        self.__headerFile = open(self.__outputPath, 'w')

    def generateEnums(self, enumDatas, enumTemplate):
        enumCount = len(enumDatas)
        for i in range(0, enumCount):
            enumData = enumDatas[i]
            lines = ['\n']
            lines.append(enumTemplate.safe_substitute(
                COMMENTS=enumData.getComment(),
                NAME=enumData.getName(),
                APPEND=enumData.getPropLines()))
            lines.append('\n')
            self.__headerFile.writelines(lines)
        pass

    def generateStructs(self, structDatas, structTemplate):
        structCount = len(structDatas)
        for i in range(0, structCount):
            structData = structDatas[i]
            lines = ['\n']
            lines.append(structTemplate.safe_substitute(
                STRUCT_COMMENTS=structData.getComment(),
                STRUCT_NAME=structData.getName(),
                APPEND=structData.getPropLines()))
            lines.append('\n')
            self.__headerFile.writelines(lines)
        pass

    def generateDefaultConfigs(self, defaultConfigs, defaultConfigTemplate):
        dcCount = len(defaultConfigs)
        for i in range(0, dcCount):
            dcData = defaultConfigs[i]
            lines = ['\n']
            lines.append(defaultConfigTemplate.safe_substitute(
                PROP=dcData.getName(),
                ACESS=dcData.getAccess(),
                MODE=dcData.getChangeMode(),
                AREA_CONFIGS=dcData.getAreaConfigs(),
                CONFIG_ARRAY=dcData.getConfigArray(),
                CONFIG_STRING=dcData.getConfigString(),
                MIN_SAMPLE_RATE=dcData.getMinSampleRate(),
                MAX_SAMPLE_RATE=dcData.getMaxSampleRate(),
                INIT_VALUES=dcData.getInitValues()))
            lines.append('\n')
            # print('debug lins#################################')
            for x in lines:
                result  = re.sub("[\r\n]+", "\n", x)
                self.__headerFile.writelines(result)
        pass

    def end(self):
        self.__headerFile.close()
