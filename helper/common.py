#coding:utf-8
'''
Created on 2016年9月12日

@author: Cloud

公共方法：登录
'''
from time import sleep
from helper.Corelogger import loginfo,FuncResult
from tools.screenshots import caputre
from tools.cel_tool import get_cookies
from helper.Core_GUI import input_text,click_element
from selenium.webdriver.common.by import By
#集群登录模块：用户名密码形式
def login(driver):
    loginfo(u'%s登录%s\n'%('+'*12,'+'*12))
    input_text(driver,By.CSS_SELECTOR, '#username','admin')
    input_text(driver,By.CSS_SELECTOR, '#password','admin')
#    click_element(driver,By.CSS_SELECTOR,".btn-primary")
    driver.execute_script("$('.btn-primary').click()")
    sleep(3)
#    loginfo("cookie: "+str(get_cookies(driver)))
    current_url=driver.current_url
    login_url=current_url.split(":7180")[0]+":7180/cmf/login"
    loginfo(u'当前页面：'+str(current_url))
    bflag=str(current_url)==login_url
    return FuncResult(not bflag,u"登录",caputre(driver))
#集群登录模块：通过注入cookie的方法
def login_cookie(driver,leap_cookies):
    loginfo(u'%s注入cookie%s\n'%('+'*12,'+'*12))
    home_url=(driver.current_url).split("/#/")+"/#/home"
    driver.get(home_url)
    driver.add_cookie(leap_cookies)
    sleep(2)
    driver.get(home_url)
    sleep(3)
    loginfo(u"Cookie 注入完成")

if __name__=="__main__":
    pass