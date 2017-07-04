#!usr/bin/env python
# -*- coding:UTF-8 -*-
###############################################################################
#
# Copyright (c) 2017 Lincentma, Inc. All Rights Reserved
#
###############################################################################

"""
This module provide function to search the train check-in.

Authors: lincentma

Date: 2017/07/03 
"""

import sys
import ConfigParser
import urllib
import urllib2
import re
import json

from prettytable import PrettyTable
import click

from datetime import date

CONF_FILE="default.conf"
STATION_FILE="station.json" 

reload(sys)
sys.setdefaultencoding('utf8')


class myconf(ConfigParser.ConfigParser):  
    def __init__(self,defaults=None):  
        ConfigParser.ConfigParser.__init__(self,defaults=None)  
    def optionxform(self, optionstr):  
        return optionstr 

def get_today_date():
    return ''.join(str(date.today()).split('-'))

def get_search_info(station, number, date, init = False):
    search_info={}
    search_type=-1
    cf=myconf()
    #cf=ConfigParser.ConfigParser()
    cf.read(CONF_FILE)
    dict(cf.items("stationname"))
    
    server_address=cf.get("server", "address")
    
    if(init == True):
        search_type=2
        search_info=dict(cf.items("stationname"))
        search_info["address"]=server_address

    if(init == False and number == ''):
        search_type=0
        search_info=dict(cf.items("stationsearch"))
        search_info["address"]=server_address
        sql_list='["%s","%s"]' % (date.encode('utf-8'), station.encode('utf-8'))
        search_info["sql"]=sql_list
    if(init == False and number != ''):
        search_type=1
        search_info=dict(cf.items("numbersearch"))
        search_info["address"]=server_address
        sql_list='["%s","%s","%s"]' % (date.encode('utf-8'),number.encode('utf-8'),station.encode('utf-8'))
        search_info["sql"]= sql_list
          
    return search_info, search_type

def get_url_data(search_data):
    
    url=search_data["address"]
    headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    del search_data["address"]
    data = urllib.urlencode(search_data)
    request = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(request)
    page = response.read()
    return page

def init_station_info(search_data):
    page=get_url_data(search_data)
    station_dict={}
    json_info=json.loads(page)
    for i in json_info:
        station_dict[i['ZM'].encode('utf-8')]=i['ZMLM'].encode('utf-8')
    jsObj = json.dumps(station_dict)
    fileObject = open(STATION_FILE, 'w')
    fileObject.write(jsObj)
    fileObject.close()
 

def get_station_id(station):
    with open(STATION_FILE, 'r') as f:
        station_dict=json.load(f)
    if(station_dict.has_key(station)):
       return station_dict[station]
    else:
       return ""
def get_train_station_info(search_data):
    get_train_number_info(search_data)

def get_train_number_info(search_data):
    page=get_url_data(search_data)
    if(page == '[]'):
	print "未搜索到相关数据"
    json_info=json.loads(page)
    cf=myconf()
    #cf = ConfigParser.ConfigParser()
    cf.read(CONF_FILE)
    tb = PrettyTable()
    tb.field_names = cf.options("search_info")
    for i in json_info:
        res_list = []
        for k in cf.options("search_info"):
            res_list.append(i[cf.get("search_info",k)])
        tb.add_row(res_list)
    print tb



@click.command()
@click.option('--station', prompt='查询车站', help='输入需要查询的车站名称',default='成都东站')
@click.option('--number', prompt='查询车次', help='输入需要查询的车次', default='')
@click.option('--date', prompt='查询日期', help='输入需要查询的日期', default=get_today_date())


def main(station, number, date):
    
    search_data, search_type=get_search_info(get_station_id(station), number, date, False)
    switcher = {
        0: get_train_station_info,
        1: get_train_number_info,
        2: init_station_info,
    }
    func = switcher.get(search_type, lambda: "nothing")
    func(search_data)
    exit(0)

if __name__ == '__main__':
    main()
