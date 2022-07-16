#!/usr/bin/python
# encoding: utf-8


import csv

COLUMN_MODULE=0
COLUMN_FUNCNAME=1
COLUMN_FUNC_TYPE=2
COLUMN_PARAM_DATA=3
COLUMN_DATAT_TYPE=4


# GET_FUNC='getInfoInt'
# SET_FUNC='setInfo'

aidl=None
mgr=None
svs=None
status=None


def output(x):
	mgr.write(x + '\n')


# 生成代码函数
def genFuncName(str):
	if status == 'setProp':
		output('int ' + str + 'Module::setProp(const VehiclePropValue& value) {')
		output('\tVehiclePropValue propValue = value;')
		output('')
		output('\t/*update time-stamp on vehicle property*/')
		output('\tpropValue.timestamp = elapsedRealtimeNano();')
		output('')
		output('\tswitch (propValue.prop) {')
	elif status == 'getAllProp':
		output('std::vector<VehiclePropValue> ' + str + 'Module::getAllPropValues() {')
		output('\tstd::vector<VehiclePropValue> props;')
		output('\tVehiclePropValue propValue;')
		output('')
		output('\tpropValue.timestamp = elapsedRealtimeNano();')
		output('')
	else: #recieveTransMsg
		output('int ' + str + 'Module::recieveTransMsg(const TransMsgValue& msg) {')
		output('\tswitch (msg.id) {')

def genFuncEnd():
	if status == 'setProp':
		output('\t}')
		output('\tmHal->onPropUpdate(propValue);')
		output('')
		output('\treturn ModuleBase::setProp(propValue);')
		output('}')
	elif status == 'getAllProp':
		output('\treturn props;')
		output('}')
	else: #recieveTransMsg
		output('\t}')
		output('\treturn ModuleBase::recieveTransMsg(msg);')
		output('}')

def genFunction(str):
	funcName = str[COLUMN_FUNCNAME]
	
	if status == 'setProp':
		output("\t\tcase toInt(VehicleProperty::" + funcName + "):")
		output("\t\t\tif (propValue.value." + str[COLUMN_FUNC_TYPE] + ".size() < 1) {")
		output("\t\t\t\tALOGE(\"%s: " + funcName + " No " + str[COLUMN_FUNC_TYPE] + " available!\", __func__);" )
		output("\t\t\t\treturn Status::INVALID_PARAM_ERROR;")
		output("\t\t\t}")
		if str[COLUMN_DATAT_TYPE] == 'bool':
			output("\t\t\tmState." + str[COLUMN_PARAM_DATA] + " = propValue.value." + str[COLUMN_FUNC_TYPE] + "[0] == 1;")
		elif str[COLUMN_DATAT_TYPE] == 'vector':
			output("\t\t\tmState." + str[COLUMN_PARAM_DATA] + " = propValue.value." + str[COLUMN_FUNC_TYPE] + ";")
		else:
			output("\t\t\tmState." + str[COLUMN_PARAM_DATA] + " = propValue.value." + str[COLUMN_FUNC_TYPE] + "[0];")
		if str[COLUMN_FUNC_TYPE] == 'int32Values':
			output("\t\t\tALOGD(\"%s: " + str[COLUMN_PARAM_DATA] + ": %d\", __func__, propValue.value." + str[COLUMN_FUNC_TYPE] + "[0]);")
		else:
			output("\t\t\tALOGD(\"%s: " + str[COLUMN_PARAM_DATA] + ": %f\", __func__, propValue.value." + str[COLUMN_FUNC_TYPE] + "[0]);")
		output("\t\t\tbreak;")
	elif status == 'getAllProp':
		output("\tpropValue.prop = toInt(VehicleProperty::" + funcName + ");")
		if str[COLUMN_DATAT_TYPE] == 'bool':
			output("\tpropValue.value." + str[COLUMN_FUNC_TYPE] + "[0] = mState." + str[COLUMN_PARAM_DATA] + "? 1 : 0;")
		elif str[COLUMN_DATAT_TYPE] == 'vector':
			output("\tpropValue.value." + str[COLUMN_FUNC_TYPE] + " = mState." + str[COLUMN_PARAM_DATA] + ";") 
		else:
			output("\tpropValue.value." + str[COLUMN_FUNC_TYPE] + "[0] = mState." + str[COLUMN_PARAM_DATA] + ";")
		output("\tprops.push_back(propValue);")
		output("")
	else: #recieveTransMsg
		output("\t\tcase TransMsgType::" + funcName + ":")
		output("\t\t\tif (msg.value." + str[COLUMN_FUNC_TYPE] + ".size() < 1) {")
		output("\t\t\t\tALOGE(\"%s: " + funcName + " No " + str[COLUMN_FUNC_TYPE] + " available!\", __func__);" )
		output("\t\t\t\treturn Status::INVALID_PARAM_ERROR;")
		output("\t\t\t}")
		if str[COLUMN_DATAT_TYPE] == 'bool':
			output("\t\t\tmState." + str[COLUMN_PARAM_DATA] + " = msg.value." + str[COLUMN_FUNC_TYPE] + "[0] == 1;")
		elif str[COLUMN_DATAT_TYPE] == 'vector':
			output("\t\t\tmState." + str[COLUMN_PARAM_DATA] + " = msg.value." + str[COLUMN_FUNC_TYPE] + ";")
		else:
			output("\t\t\tmState." + str[COLUMN_PARAM_DATA] + " = msg.value." + str[COLUMN_FUNC_TYPE] + "[0];")
		if str[COLUMN_FUNC_TYPE] == 'int32Values':
			output("\t\t\tALOGD(\"%s: " + str[COLUMN_PARAM_DATA] + ": %d\", __func__, msg.value." + str[COLUMN_FUNC_TYPE] + "[0]);")
		else:
			output("\t\t\tALOGD(\"%s: " + str[COLUMN_PARAM_DATA] + ": %f\", __func__, msg.value." + str[COLUMN_FUNC_TYPE] + "[0]);")
		output("\t\t\tbreak;")


# make function
def dispatchfunction(line):
	if line[COLUMN_MODULE] == '模块':
		print('标题分类 : ' + line[COLUMN_MODULE])
	else:
		genFunction(line) 
	
# make manager file
def makeModule(ls):
	global mgr
	mgr=open('output/module.cpp', 'w', encoding='utf-8')
	tp = ls[1][0]
	output('#define LOG_TAG \"'  + tp + 'Module\"')
	output('#include <utils/Log.h>')
	output('#include <utils/SystemClock.h>')
	output('#include <vhal_v2_0/VehicleUtils.h>')
	output('#include \"' + tp +'Module.h\"')
	output('#include \"Log.h\"')
	output('#include \"VehicleHalImpl.h\"')

	output('namespace android {')
	output('namespace hardware {')
	output('namespace automotive {')
	output('namespace vehicle {')
	output('namespace V2_0 {')
	output('namespace impl {')
	output('constexpr TransMsgType HvacModule::kTransMsgs[];')
	output('const VehiclePropConfig HvacModule::kVehicleProperties[] = {};')
	output('')
	setStatus('setProp')
	genFuncName(tp)
	for line in ls:
		dispatchfunction(line)
	genFuncEnd()
	setStatus('getAllProp')
	genFuncName(tp)
	for line in ls:
		dispatchfunction(line)
	genFuncEnd()
	setStatus('recieveTransMsg')
	genFuncName(tp)
	for line in ls:
		dispatchfunction(line)
	genFuncEnd()
	output('std::vector<VehiclePropConfig> ' + tp + 'Module::listProperties() {')
	output('    std::vector<VehiclePropConfig> list(kVehicleProperties,')
	output('            kVehicleProperties + sizeof(kVehicleProperties) / sizeof(kVehicleProperties[0]));')
	output('    return list;')
	output('}')
	output('std::unique_ptr<std::vector<TransMsgType>> ' + tp + 'Module::getSupportedTransMsgTypes() {')
	output('    return std::make_unique<std::vector<TransMsgType>>(kTransMsgs,')
	output('            kTransMsgs + sizeof(kTransMsgs) / sizeof(kTransMsgs[0]));')
	output('}')
	output('}')
	output('}')
	output('}')
	output('}')
	output('}')
	output('}')
	mgr.close()
	mgr=None
	

def setStatus(s):
	global status
	status = s
	print('--------------------start make ' + s + '-----------------------')


def generateDefaultModules(inputPath):
	ls=[]

	with open(inputPath) as file:
		fin = csv.reader(file)
		for row in fin:
			ls.append(row)
	file.close()
	makeModule(ls) #make manager file

















