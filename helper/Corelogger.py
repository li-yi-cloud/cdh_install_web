#coding:utf-8
'''
Created on 2016年9月12日

@author: Cloud

Python logger模块封装、Actionresult （返回Action 执行结果）
'''
import logging.handlers,inspect

class Logger(object):
    def __init__(self,filename,loglevel):
        format_dict={
                1 : logging.Formatter('%(asctime)s - %(filename)s [line:%(lineno)d] - %(levelname)s - %(message)s'),
                2 : logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
                }
        loglevel_dict={
                1:logging.NOTSET,
                2:logging.DEBUG,
                3:logging.INFO,
                4:logging.WARNING,
                5:logging.ERROR,
                6:logging.CRITICAL
                }
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        file_handler =logging.handlers.RotatingFileHandler(filename, mode='a', maxBytes=10485760, backupCount=0, encoding="UTF-8", delay=0)
        file_handler.setLevel(loglevel_dict[3])
        
        console = logging.StreamHandler()  
        console.setLevel(loglevel_dict[int(loglevel)])
        
        file_handler.setFormatter(format_dict[1])
        console.setFormatter(format_dict[2]) 
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console)
    def getlog(self):
        return self.logger
    def debug(self,message):
        self.logger.debug(message)
    def info(self,message):
        self.logger.info(message)
    def warning(self,message):
        self.logger.warning(message)
    def error(self,message):
        self.logger.error(message)
    def critical(self,message):
        self.logger.critical(message)

logdebug=logging.debug
loginfo=logging.info
logwarning=logging.warn
logerror=logging.error
logcritical=logging.critical

def FuncResult(result,messages,caputre=None):
    FuncName=inspect.stack()[1][3]
    if result==True:
        loginfo(u'[Run %s action success ]%s'%(FuncName,messages))
    else:
        if caputre:
            caputre.update_filename(messages)
            caputre.screenshot()
        logerror(u'[Run %s action fail ]%s'%(FuncName,messages))
        assert result !=False

if __name__=="__main__":
    pass