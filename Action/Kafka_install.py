#coding:utf-8
import time
from selenium.webdriver.common.by import By
from helper.Core_GUI import find_elements,click_element,\
     get_element_text,get_element_attribute,verify_element
from helper.Corelogger import FuncResult
from tools.screenshots import caputre
from tools.cel_tool import get_ele_index
#from Action.configure import shell_command

class kafka_install():
    def __init__(self,driver,logger,data):
        self.driver=driver
        self.logger=logger
        self.data=data
    def verify_install_result(self,ele_select,endtime,para):
        status=''
        while time.time()<endtime:
            status=get_element_attribute(find_elements(self.driver,By.CSS_SELECTOR,ele_select)[0],"class")
            if para==status:
                break
            else:
                time.sleep(3)
        return status
    def Kafka_deploy(self):
        self.logger.info(u"%sKafka install parcel%s\n"%('+'*12,'+'*12))
        cur_url=self.driver.current_url
        install_url=cur_url.split(":7180")[0]+":7180/cmf/parcel/status"
        self.driver.get(install_url)
        time.sleep(2)
#        self.driver.execute_script("$('tbody .name>span>span').attr(\"style\",\"\")")
        parcel_name_list=map(lambda x:x.text,find_elements(self.driver,By.CSS_SELECTOR,"tbody .name>span>span"))
        parcel_version_list=map(lambda x:x.text,find_elements(self.driver,By.CSS_SELECTOR,"tbody .version>span>span"))
        Kafka_name_index=[i for i, x in enumerate(parcel_name_list) if x == u"KAFKA"]
        Kafka_version_index=[i for i, x in enumerate(parcel_version_list) if x == u"2.1.1-1.2.1.1.p0.18"]
        kafka_index=[i for i in Kafka_version_index if i in Kafka_name_index][0]
        kafka_status=get_element_text(self.driver,By.CSS_SELECTOR,"tbody>tr:nth-child(%s)>.version+td>div"%(kafka_index*2+1,))
        if u"Downloaded" in kafka_status:
            click_element(self.driver,By.CSS_SELECTOR,"tbody>tr:nth-child(%s)>.actions button[title*=\"Distribute\"]"%(kafka_index*2+1,))
            status=self.verify_install_result("tbody>tr:nth-child(%s)>td:nth-child(3)>div"%(kafka_index*2+1,),time.time()+300,u'distributed clickable')
            if u'distributed clickable'!=status:
                return FuncResult(False,u"Kafka install parcel distribute", caputre(self.driver))
            click_element(self.driver,By.CSS_SELECTOR,"tbody>tr:nth-child(%s)>.actions button[title*=\"Activate\"]"%(kafka_index*2+1,))
            if verify_element(self.driver,By.CSS_SELECTOR,"#parcelRestartInfoDialog button[data-bind$=\"onClickActivateOnly\"]",5):
                click_element(self.driver,By.CSS_SELECTOR, "#parcelRestartInfoDialog button[data-bind$=\"onClickActivateOnly\"]")
            else:
                return FuncResult(False,u"Kafka install parcel Activate", caputre(self.driver))
            status=self.verify_install_result("tbody>tr:nth-child(%s)>td:nth-child(3)>div"%(kafka_index*2+1,),time.time()+300,u'activated clickable')
            if u'activated clickable'!=status:
                return FuncResult(False,u"Kafka install parcel Activate", caputre(self.driver))
        elif u"Distributed" in kafka_status and u"Activated" not in kafka_status:
            click_element(self.driver,By.CSS_SELECTOR,"tbody>tr:nth-child(%s)>.actions button[title*=\"Activate\"]"%(kafka_index*2+1,))
            if verify_element(self.driver,By.CSS_SELECTOR,"#parcelRestartInfoDialog button[data-bind$=\"onClickActivateOnly\"]",5):
                click_element(self.driver,By.CSS_SELECTOR, "#parcelRestartInfoDialog button[data-bind$=\"onClickActivateOnly\"]")
            else:
                return FuncResult(False,u"Kafka install parcel Activate", caputre(self.driver))
            status=self.verify_install_result("tbody>tr:nth-child(%s)>td:nth-child(3)>div"%(kafka_index*2+1,),time.time()+300,u'activated clickable')
            if u'activated clickable'!=status:
                return FuncResult(False,u"Kafka install parcel Activate", caputre(self.driver))
        elif u"Distributed, Activated" in kafka_status:
            pass
        return FuncResult(True,u"Kafka install parcel", caputre(self.driver))
    def add_kafka_service(self):
        self.logger.info(u"%sadd Kafka service%s\n"%('+'*12,'+'*12))
        cur_url=self.driver.current_url
        home_url=cur_url.split(":7180")[0]+":7180/cmf/home"
        self.driver.get(home_url)
        click_element(self.driver,By.CSS_SELECTOR,"#statusPaneContent .cluster-drop-down>a")
        click_element(self.driver,By.CSS_SELECTOR,"a[data-event=\"Add Service\"]")
        for _ in range(5):
            if u"add-service" in self.driver.current_url:
                break
            else:
                time.sleep(2)
        self.logger.info("$('#serviceType_KAFKA').click()")
        self.driver.execute_script("$('#serviceType_KAFKA').click()")
        click_element(self.driver,By.CSS_SELECTOR,"button[data-bind*=\"onClickContinue\"]")
        for _ in range(10):
            if u"roleAssignmentsStep" in self.driver.current_url:
                break
            else:
                time.sleep(2)
        self.logger.info(self.driver.current_url)
        return FuncResult(u"roleAssignmentsStep" in self.driver.current_url,"add kafkaservice")
    def Assign_role(self):
        self.logger.info(u"%sAssign role%s\n"%('+'*12,'+'*12))
        role_name_list=map(lambda x:x.text,find_elements(self.driver,By.CSS_SELECTOR,".label-service-kafka+.name"))
        for rolename in self.data.keys():
            if self.data[rolename]:
                rolename_index=get_ele_index(role_name_list,rolename)
                if rolename_index !=None:
                    self.logger.info("%s : $('div:nth-child(%s)>div>.role-type-btn').click()"%(rolename,rolename_index+1,))
                    self.driver.execute_script("$('div:nth-child(%s)>div>.role-type-btn').click()"%(rolename_index+1,))
                    role_checkbox_list=find_elements(self.driver,By.CSS_SELECTOR,"tbody i")
                    role_hostname=map(lambda x:x.text, find_elements(self.driver,By.CSS_SELECTOR,"tbody>tr>td[data-bind$=\"hostName\"]"))
                    for checkbox in role_checkbox_list:
                        if u" check" in get_element_attribute(checkbox,"class"):
                            checkbox.click()
                            time.sleep(0.5)
                    for hostname in self.data[rolename]:
                        hostname_index=get_ele_index(role_hostname,hostname)
                        if hostname_index !=None:
                            role_checkbox_list[hostname_index].click()
                        else:
                            self.logger.error(u"host name is invalid")
                    if not click_element(self.driver,By.CSS_SELECTOR,"form #modalDialog .modal-footer>.btn+.btn"):
                        return FuncResult(False,"kafka install select host:%s"% rolename)
                else:
                    self.logger.error(u"Kafka rolename:%s is invalid")
        click_element(self.driver, By.CSS_SELECTOR,"button[data-bind*=\"onClickContinue\"]")
        time.sleep(3)
        ele_text=get_element_text(self.driver,By.CSS_SELECTOR,"#reviewStep h2")
        ret=u"Review Changes" in ele_text
        return FuncResult(ret,"kafka assign role")
    def config_service(self):
        self.logger.info(u"%sconfig service%s\n"%('+'*12,'+'*12))
        endTime=time.time()+60
        while time.time()<endTime:
            if find_elements(self.driver,By.CSS_SELECTOR,"#reviewStep .param-spec-property"):
                break
#        time.sleep(1)
#         shell_command("mysql -uadmin -paaaaaa --execute 'use cm;update CONFIGS set VALUE=1024 where ATTR=\"broker_max_heap_size\";update CONFIGS_AUD set VALUE=1024 where ATTR=\"broker_max_heap_size\";'")
#        shell_command("sshpass -p aaaaaa ssh root@10.94.1.60 -o StrictHostKeyChecking=no sh /home/mysql_kafka_config.sh")
        time.sleep(3)
        click_element(self.driver, By.CSS_SELECTOR, "#bottomButtons button[data-bind*=\"onClickContinue\"]")
        for _ in range(5):
            c_url=self.driver.current_url
            self.logger.info(c_url)
            if u"commandDetailsStep" in c_url:
                break
            else:
                time.sleep(2)
#         ele_text=get_element_text(self.driver,By.CSS_SELECTOR,"#commandDetailsStep>div>div:first-child>h2:first-child .muted")
        c_url=self.driver.current_url
        self.logger.info(c_url)
        ret=u"commandDetailsStep" in c_url
        return FuncResult(ret,u"config service", caputre(self.driver))
    def start_service(self):
        self.logger.info(u"%sstart service%s\n"%('+'*12,'+'*12))
        endtime=time.time()+1200
        fail=1
        while time.time()<endtime:
            result=get_element_attribute(find_elements(self.driver,By.CSS_SELECTOR,"#commandDetailsStep>div>div:first-child>h2:first-child>i:first-child")[0],"class")
            if u"error" in result and fail==1:
                fail=fail+1
                click_element(self.driver,By.LINK_TEXT,"Retry")
            elif u"error" in result and fail==2:
                return FuncResult(False,u"start service", caputre(self.driver))
            elif u"success" in result:
                break
            else:
                time.sleep(5)
        time.sleep(2)
        click_element(self.driver,By.CSS_SELECTOR,"#bottomButtons button[data-bind*=\"onClickContinue\"]")
        time.sleep(1)
        ele_text=get_element_text(self.driver,By.CSS_SELECTOR,"#finishStep h2")
        ret=u"Congratulations!" in ele_text
        return FuncResult(ret,u"start service", caputre(self.driver))
    def install_finished(self):
        self.logger.info(u"%sinstall finished%s\n"%('+'*12,'+'*12))
        click_element(self.driver,By.CSS_SELECTOR,"#bottomButtons button[data-bind*=\"onClickContinue\"]")
        for _ in range(5):
            if u"7180/cmf/home" in self.driver.current_url:
                break
            else:
                time.sleep(2)
        ret=u"7180/cmf/home" in self.driver.current_url
        return FuncResult(ret,u"install finished", caputre(self.driver))
    def start(self):
        self.Kafka_deploy()
        self.add_kafka_service()
        self.Assign_role()
        self.config_service()
        self.start_service()
        self.install_finished()
