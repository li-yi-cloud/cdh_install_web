#coding:utf-8
'''
Created on 2016年9月12日
@author: Cloud

工具类方法
'''
import time,types,codecs,json,math
from time import sleep
from helper.Corelogger import logerror
#from bs4 import BeautifulSoup

def get_time():
    now_time=time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
    return now_time
def get_cookies(driver):
    cookies=driver.get_cookies()
    return cookies
def add_cookies(driver,values):
    driver.add_cookie(values)
    sleep(3)
def close_window(driver,windowlist):
    handles=driver.window_handles
    for handle in handles:
        if handle in list(windowlist):
            driver.switch_to_window(handle)
            driver.close()
def get_close_window_list(driver,not_close_window):
    handles=driver.window_handles
    window_list=[]
    if type(not_close_window) is types.UnicodeType and type(not_close_window) is not types.ListType:
        not_close_window=not_close_window.split(" ")
    else:
        logerror("parameter is wrong") 
    for handle in handles:
        if handle not in not_close_window:
            window_list.append(handle)
    return window_list
'''
def get_value_from_xml(filename):
    with open(filename,'r') as xml:
        Bau=BeautifulSoup(xml,'lxml')
        names=Bau.select('name')
        values=Bau.select('value')
        name_list=[]
        value_list=[]
        for i in range(len(names)):
            name_list.insert(i,names[i].get_text())
            value_list.insert(i, values[i].get_text())
        return dict(zip(name_list,value_list))
'''
def get_file_value(filename):
    try:
        with open(filename,'r') as file_read:
            values=file_read.read()
        return values
    except:
        logerror("File:(%s) is not find"%(filename,))
        return None
#将字符写入到文本中
def write_in_file(filename,contents):
    with codecs.open(filename, 'w','utf-8') as fail_log:
        fail_log.write(contents)
#将文本文件中的字符加载成json对象l
def readJson(filename):
    try:
        return json.loads(get_file_value(filename))
    except:
        return {}
#获取列表中元素的索引
def get_ele_index(target_list,target_element):
    try:
        path=[i for i, x in enumerate(target_list) if x == target_element][0]
        return path
    except:
        return None
def choose_possibly_count(option_number,select_number):
    if select_number>option_number:
        return 0
    else:
        return (math.factorial(option_number)/math.factorial(select_number))/math.factorial(option_number-select_number)
    
if __name__=="__main__":
    pass