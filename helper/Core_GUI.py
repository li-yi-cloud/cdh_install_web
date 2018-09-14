#coding=utf-8
'''
Created on 2016年9月12日

@author: Cloud

selenium 接口二次封装，未发现元素时不会抛出异常
查找页面元素并返回列表，验证元素是否存在，点击元素，输入文本，获取元素属性、获取元素中的文本信息
'''
from helper.Corelogger import loginfo,logwarning, logerror
from time import sleep

#查找元素
def find_elements(driver,method,para):
    if verify_element(driver,method,para):
        return driver.find_elements(method,para)
    else:
        return []
#验证元素是否存在
def verify_element(driver,method,para,times=3):
    loginfo(u'[%s]开始查找元素:%s'%(method,para))
    ret=False
    for i in range(times):
        sleep(1)
        ret=verify_element_(driver, method, para,i==times-1)
        if ret:
            break
    return ret
def verify_element_(driver,method,para,islog=False):
    try:
        driver.find_element(method,para)
        return True
    except Exception, e:
        if islog:
            logwarning(u'[%s]未发现元素:%s\n%s' %(method,para,e))
        return False
#向元素输入文本
def input_text(driver,method,para,text):
    ele=find_elements(driver, method, para)
    if ele and len(ele)==1:
        try:
            loginfo(u'[%s]开始向元素:%s中输入字符:%s' %(method,para,text))
            ele[0].clear()
            ele[0].send_keys(text)
            return True
        except Exception,e:
            logerror(u'[%s]向元素:%s输入字符失败\n%s' %(method,para,e))
            return False
    elif len(ele)>1:
        logwarning(u'[%s]元素:%s不唯一' %(method,para))
        return False
    else:
        return None
#点击元素
def click_element(driver,method,para):
    ele=find_elements(driver, method, para)
    if ele and len(ele)==1:
        try:
            loginfo(u'[%s]开始点击元素:%s' %(method,para))
            ele[0].click()
            return True
        except Exception,e:
            logerror(u'[%s]点击元素:%s失败\n%s' %(method,para,e))
            return False
    elif len(ele)>1:
        logwarning(u'[%s]元素:%s不唯一' %(method,para))
        return False
    else:
        return None
#获取元素中的文本信息
def get_element_text(driver,method,para):
    ele=find_elements(driver, method, para)
    if ele and len(ele)==1:
        try:
            loginfo(u'[%s]开始获取元素:%s中的文本'%(method,para))
            result=ele[0].text
            return result
        except Exception,e:
            logerror(u'[%s]获取元素:%s中的文本失败\n%s' %(method,para,e))
            return None
    elif len(ele)>1:
        logwarning(u'[%s]元素:%s不唯一' %(method,para))
        return False
    else:
        return None
#获取元素中的属性
def get_element_attribute(element,att):
    loginfo(u'开始获取元素中的属性')
    try:
        result=element.get_attribute(att)
        loginfo(u'元素属性:%s=%s'%(att,result))
        return result
    except:
        return 0