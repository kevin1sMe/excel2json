#!/usr/bin/env python
#coding=utf-8
'''
#========================================================================
#   FileName: create_global_conf.py
#     Author: kevinlin
#       Desc: 我们游戏中有一些通用的配置，零碎且不好归类，策划有可能需要变化，
              那么将其写到excel中，然后通过工具生成程序侧用的配置表，这大概是个好选择吧。。
#      Email: linjiang1205@qq.com
# LastChange: 2013-12-19 16:58:04
#========================================================================
'''
import os
import xlrd
import sys
import re
import commands
import logging


reload(sys)
sys.setdefaultencoding( "utf-8" )

#LOG_LEVEL = logging.WARN
LOG_LEVEL = logging.DEBUG
logging.basicConfig(level=LOG_LEVEL, format="[%(levelname)s]%(message)s")

class CardInterpreter:
    def __init__(self, xls_file_path, sheet_name):
        self._xls_file_path = xls_file_path
        self._sheet_name = sheet_name

        try :
            self._workbook = xlrd.open_workbook(self._xls_file_path)
        except BaseException, e :
            logging.error("open xls file(%s) failed!" %(self._xls_file_path))
            raise

        self._sheet = None;
        logging.debug('sheet_name:%s'%(self._sheet_name))
        try:
            self._sheet = self._workbook.sheet_by_name(self._sheet_name)
        except Exception, e:
            logging.error("open sheet(%s) failed!"%(self._sheet_name))
            raise

        # 行数和列数
        self._row_count = self._sheet.nrows
        self._col_count = self._sheet.ncols
        logging.debug("nrows: " + str(self._row_count))
        logging.debug("ncols: " + str(self._col_count))

       #定义了表格的头部；那些结构。。用于后续数据的读取和解析
        self._header = []

        #产生的lua结果集
        self._context = ""

    def ParseOneRow(self, row):
        #为简单起见，这里进行了很多假定
        return_str = ""
        read_txt = self._sheet.cell(row, 0).value
        var_name = read_txt.strip()
        logging.debug("var_name: " + str(var_name))

        read_txt =  self._sheet.cell(row, 1).value
        var_type = str(read_txt).strip()
        logging.debug("var_type: " + str(var_type))

        read_txt =  self._sheet.cell(row, 2).value
        var_value = str(read_txt).strip()

        read_txt =  self._sheet.cell(row, 3).value
        var_desc = str(read_txt).strip()

        #if len(var_desc) > 0 : 
            #return_str += "--" + var_desc + "\n"

        if var_type == "digit" or var_type == "int":
            return_str +=  "\"" + var_name + "\": " + str(int(float(var_value)))
        elif var_type == "digit array" or var_type == "int array":
            split_value = re.split('[;,|:]',var_value)
            output_str = ",".join(split_value)
            return_str +=  "\"" + var_name + "\": " + "[" + " " + output_str + " ]"
        elif var_type == "string":
            return_str += "\"" + var_name + "\": \"" + var_value + "\""
        elif var_type == "string array":
            split_value = re.split('[;,|:]',var_value)
            #output_str = ",".join("\"" + split_value + "\"")
            new_split_value = [ "\"" + x + "\""  for  x in split_value ]
            output_str = ",".join(new_split_value)
            return_str +=  "\"" + var_name + "\": " + "[" + " " + output_str + " ]"
        else:
            pass

        logging.info("return_str: " + return_str)
        return return_str

    def Interpreter(self) :
        #清空旧东西以便重入
        self._header = []
        self._context = "{\n"

        lines = []
        for row in range(1, self._row_count):
            lines.append(self.ParseOneRow(row))

        self._context += ",\n".join(lines)
        self._context += "\n}"
        return self._context

def Write2File(file_name,context) :
    """输出到文件"""
    open_lua_file = file_name
    lua_file = open(open_lua_file, "w+")
    lua_file.write(context)
    lua_file.close()

def GetFileName(svr_or_client, sheet_name):
    return sheet_name.strip().lower() + ".json"

def TestJsonFile(filename):
    command = "python check_json.py " + filename
    status, output = commands.getstatusoutput(command)
    if (status != 0) :
        logging.debug("\x1B[0;31;40m WARNING: \e[1;35m Test " + filename + "\t--> FAILED!" + str(status) + output + "\x1B[0m")
        print "\x1B[0;31;40m[ERROR]: Test " + filename + " --> FAILED!\x1B[0m"
        print  "\x1B[0;35;40m\t" + str(status) + output + "\x1B[0m"
        #sys.exit(-1)
    else :
        print "\x1B[0;32;40m[SUCCESS]: Test " + filename + " --> OK\x1B[0m"



if __name__ == '__main__' :
    if len(sys.argv) < 2 :
        print "Usage: %s excel_file sheet_name" %(sys.argv[0])
        sys.exit(-1)

    xls_file_name = sys.argv[1]
    #读取sheet名，转为大写字母
    sheet_name = sys.argv[2].upper(); 
    parse = CardInterpreter(xls_file_name, sheet_name)
    parse.Interpreter()

    content = ""
    file_name = GetFileName('CLIENT', sheet_name)
    content += parse.Interpreter()
    Write2File(file_name, content)
    TestJsonFile(file_name)

