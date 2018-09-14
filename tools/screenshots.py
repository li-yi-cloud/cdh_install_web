#-*- coding=utf-8 -*-
'''
Created on 2016年9月12日

@author: Cloud

selenium 截图模块
'''
import random
from config import BASE_DIR 
from tools import cel_tool

class caputre(object):
    def __init__(self,driver=None,fail_question=None):
        self.driver=driver
        self.file_name=fail_question
    def update_filename(self,filename):
        self.file_name=filename
    def screenshot(self):
        self.driver.execute_script("""
                (function () {
                var y = 0;
                var step = 100;
                window.scroll(0, 0);
                function f() {
                    if (y < document.body.scrollHeight) {
                            y += step;
                            window.scroll(0, y);
                            setTimeout(f, 50);
                    } else {
                            window.scroll(0, 0);
                            document.title += "scroll-done";
                    }
                }
                setTimeout(f, 1000);
                })();
            """)
        for _ in range(30):
                if "scroll-done" in self.driver.title:
                    break
        nowtime=cel_tool.get_time()
        xname='%d'%random.randint(10000,99999)
        paths=BASE_DIR+"/installer/install_log/screenshots/"
        values=paths+"test_capture_"+self.file_name+"_"+nowtime+"_"+xname+".jpg"
        self.driver.save_screenshot(values)

if __name__=="__main__":
    pass