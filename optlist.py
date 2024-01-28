#  OpenJDKのソース globals.hpp から起動オプションの一覧を作成する

import os
#import sys
#import time
import re
#import datetime
#import locale
#import subprocess
#import argparse
from datetime import timedelta

version = "1.00"     

appdir = os.path.dirname(os.path.abspath(__file__))
#inputfile = appdir + "/globals.hpp"
filelist = appdir + "/filelist.txt"
outfile = appdir + "/optlist.htm"
templatefile = appdir + "./optlist_templ.htm"
globallist = []
debug = 0
out = ""

#  各オプションの情報は 辞書 option_info に格納
#  キー  name オプション名  type 型  default デフォルト値  desc 説明  range 範囲  fname
#  option_list に option_info をリストとして格納
option_list = []

def main_proc():
    global option_list

    read_globalfile()
    parse_template()

def read_globalfile() :
    global globallist
    with open(filelist) as f:
        for line in f:
            globallist.append(line.strip())

def analize_global(infile) :
#    re_product = "^ *product("
    re_comment  = r'"(.*)"'
#    re_name2 = "^\*\*-XX:[+-]*(.*?)$"

    f = open(infile, 'r')
    filename = os.path.basename(infile)
    while True:
        s = f.readline()
        if s  == '':
            break
        s = s.replace("\\","").strip()
        m = re.match(r' *product.*\(', s)
        if m :
            s = s.replace("product_pd(","")
            s = s.replace("product(","")
            arglist = s.split(",")
            option_info = {}   
            option_info['name'] = arglist[1]
            option_info['type'] = arglist[0]
            option_info['default'] = arglist[2]
            option_info['fname'] = filename
            #print(arglist[0],arglist[1],arglist[2])
            desc = ""
            while True:
                s = f.readline()
                s = s.replace("\\","").strip()
                m = re.search(re_comment,s)
                if m :
                    desc = desc + m.group(1)
                    #rint(m.group(1))
                else :
                    break
                if s.endswith(")")  :
                    break
            option_info['desc'] = desc

            s = f.readline()
            s = s.replace("\\","").strip()
            option_info['range'] = ""
            if "range(" in s :
                range_str = s.replace("range(","")
                position = range_str.rfind(")")
                range_str = range_str[:position]
                option_info['range'] = range_str
                #print(range_str)

            option_list.append(option_info)
    f.close()

def contents() :
    for infile in globallist :
        option_list = []
        #infile = inputfile
        analize_global(infile)
    output_option_info()

def parse_template() :
    global out 
    f = open(templatefile , 'r', encoding='utf-8')
    out = open(outfile,'w' ,  encoding='utf-8')
    for line in f :
        if "%contents%" in line :
            contents()
            continue
        if "%total%" in line :
            out.write(f'オプション総数 : {len(option_list)} ')
            continue
        out.write(line)

    f.close()
    out.close()

def output_wiki() :
    sorted_option_list = sorted(option_list, key=lambda option_info: option_info['name'])
    for info in sorted_option_list :
        print(f"|{info['name']}|{info['type']}|{info['default']}|{info['desc']}|")
    
def output_option_info() :
#    out.write("<table>")
#    out.write("<tr><th>オプション</th><th>型</th><th>デフォルト</th><th>説明</th><th>定義ファイル</th></tr>")
    sorted_option_list = sorted(option_list, key=lambda option_info: option_info['name'])
    for info in sorted_option_list :
        out.write(f"<tr><td>{info['name']}</td><td>{info['type']}</td>"
                  f"<td>{info['default']}</td><td>{info['desc']}</td><td>{info['fname']}</td></tr>")

#    out.write("</table>")
#------------------------------------------------------
main_proc()
