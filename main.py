#coding:utf-8
import os,argparse
from selenium import webdriver
from helper import common
from config import BASE_DIR
from helper.Corelogger import Logger,logerror,FuncResult
from tools.cel_tool import get_time,readJson
from Action.cluster_install import cluster_install
from Action.Kafka_install import kafka_install

def get_para():
    parser = argparse.ArgumentParser(description='Install option:')
    parser.add_argument("option", metavar='option',type=str,nargs='?',help='Install option :cdh_deploy or kafka_deploy')
    args = parser.parse_args()
    return vars(args)

def driverInit():
#    driver = webdriver.PhantomJS()
    driver = webdriver.Firefox()
    driver.implicitly_wait(3)
    driver.delete_all_cookies()
    return driver
    
def login(driver,manager_url):
    driver.get(manager_url)
    driver.maximize_window()
    common.login(driver)   

def dirverEnd(driver):
    driver.quit()
    
def get_cluster_config():
    conf=readJson(BASE_DIR+"/cluster_deploy_conf.json")
    if conf:
        return conf
    else:
        return FuncResult(False,"get cluster conf")

def cluster_deploy(driver,logger,data):
    installer=cluster_install(driver,logger,data["deploy_data"])
    manager_url=data["manager_url"]
#    login(driver,manager_url)
    try:
        login(driver,manager_url)
        installer.start()
    except Exception,e:
        logerror("install fail:\n %s" % e )
    dirverEnd(driver)
    os._exit(0)
def kafka_auto_deploy(driver,logger,data):
    kafka=kafka_install(driver,logger,data["deploy_data"]["Kafka_data"])
    manager_url=data["manager_url"]
#    login(driver,manager_url)
    try:
        login(driver,manager_url)
        kafka.start()
    except Exception,e:
        logerror("install fail:\n %s" % e )
    dirverEnd(driver)
    os._exit(0)
def run(case_name):
    logName=BASE_DIR+"/logs/install_log-%s.log"%(get_time())
    logger=Logger(filename=logName,loglevel=3)
    data=get_cluster_config()
    driver=driverInit()
    if case_name==u"kafka_deploy":
        kafka_auto_deploy(driver, logger, data)
    elif case_name==u"cluster_deploy":
        cluster_deploy(driver, logger, data)
    else:
        logerror("invalid option")
        dirverEnd(driver)
        os._exit(0)
    
if __name__=="__main__":
    case_name=get_para()["option"]
    run(case_name)