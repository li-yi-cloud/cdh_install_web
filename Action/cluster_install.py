#coding:utf-8
import time
from selenium.webdriver.common.by import By
from helper.Core_GUI import find_elements,click_element,\
     get_element_text,get_element_attribute,verify_element
from helper.Corelogger import FuncResult
from tools.screenshots import caputre
from tools.cel_tool import get_ele_index
from Action.configure import configure 

class cluster_install():
    def __init__(self,driver,logger,data):
        self.driver=driver
        self.logger=logger
        self.data=data
    def start_install(self):
        self.logger.info(u"%sEnd User License Terms and Conditions%s\n"%('+'*12,'+'*12))
#        click_element(self.driver,By.CSS_SELECTOR,".checkbox>input")
        self.driver.execute_script("$('.checkbox>input').click()")
        click_element(self.driver, By.CSS_SELECTOR,".btn-large+.btn")
        time.sleep(1)
        ele_text=get_element_text(self.driver,By.CSS_SELECTOR, "link+h2")
        ret=ele_text==u'Which edition do you want to deploy?'
        if not ret:
            return FuncResult(ret,u"End User License Terms and Conditions",caputre(self.driver))
        else:
            click_element(self.driver, By.CSS_SELECTOR, ".btn-large+.btn")
        time.sleep(1)
        ele_text=get_element_text(self.driver,By.CSS_SELECTOR, ".Wizard>h1")
        ret=ele_text==u'Thank you for choosing Cloudera Manager and CDH.'
        return FuncResult(ret,u'Select version', caputre(self.driver))
    def choose_cdh(self):
        self.logger.info(u"%sChoose CDH Manager%s\n"%('+'*12,'+'*12))
        click_element(self.driver,By.CSS_SELECTOR,".btn-large")
        time.sleep(1)
        ele_text=get_element_text(self.driver,By.CSS_SELECTOR, ".Wizard>h1")
        ret=ele_text==u'Specify hosts for your CDH cluster installation.'
        return FuncResult(ret,u"Choose CDH Manager",caputre(self.driver))
    def select_hosts(self):
        self.logger.info(u"%sselect hosts%s\n"%('+'*12,'+'*12))
        click_element(self.driver,By.CSS_SELECTOR,"#newOrExistingHostsTabs>li+li>a")
        host_buttons=find_elements(self.driver,By.CSS_SELECTOR,"tr>td>input")
        host_name_list=map(lambda x:x.text,find_elements(self.driver,By.CSS_SELECTOR,"#HostsTable tr>td:nth-child(2) a"))
        for name in self.data["host_name"]:
            index_s=get_ele_index(host_name_list,name)
            if index_s !=None:
                host_buttons[index_s].click()
            else:
                self.logger.warning(u"host name [%] is wrong!"% name)
        time.sleep(1)
        click_element(self.driver,By.CSS_SELECTOR,"#continueExistingButton")
        ele_text=get_element_text(self.driver,By.CSS_SELECTOR, "#repositorySelectionStep>.wizard-step>h2")
        ret=ele_text==u"Select Repository"
        return FuncResult(ret,u"select hosts", caputre(self.driver))
    def Select_Repository(self):
        self.logger.info(u"%sselect Repository%s\n"%('+'*12,'+'*12))
#        kafka_vesion=find_elements(self.driver,By.CSS_SELECTOR,"input[value$=\"p0.115\"][name=\"KAFKA\"]")
        self.driver.execute_script("$('input[value=\"2.1.0-1.2.1.0.p0.115\"][name=\"KAFKA\"]').click()")
        click_element(self.driver,By.CSS_SELECTOR, ".btn-large+.btn-primary")
        time.sleep(1)
        ele_text=get_element_text(self.driver,By.CSS_SELECTOR, "#parcelInstallStep h2")
        ret=u"Installing Selected Parcels" in ele_text
        return FuncResult(ret,u"Select Repository", caputre(self.driver))
    def install_parcels(self):
        self.logger.info(u"%sInstalling Selected Parcels%s\n"%('+'*12,'+'*12))
        install_schedule_ele=find_elements(self.driver,By.CSS_SELECTOR,".parcel-header>div[data-bind$=\"Activation\"]>div>div")
        unpack_schedule_ele=find_elements(self.driver,By.CSS_SELECTOR,"div[data-bind*=\"unpackedPercent\"]")[0]
        destribute_schedule_ele=find_elements(self.driver,By.CSS_SELECTOR,"div[data-bind*=\"distributionProgress\"]")[0]
        endtime= time.time()+1200
        while time.time()<endtime:
            unpack_schedule=get_element_attribute(unpack_schedule_ele, "style")
            destribute_schedule=get_element_attribute(destribute_schedule_ele, "style")
            self.logger.info(u"Distribute schedule:%s || unpack schedule:%s "%(destribute_schedule,unpack_schedule))
            install_schedule_list=map(get_element_attribute,install_schedule_ele,["style" for _ in install_schedule_ele])
            if len(set(install_schedule_list))==1 and u"width: 100%;" in install_schedule_list:
                break;
            else:
                time.sleep(3)
        time.sleep(3)
        next_button_attr=get_element_attribute(find_elements(self.driver,By.CSS_SELECTOR,".btn.btn-large.btn-primary")[0],"disabled")
        if next_button_attr==0:
            return FuncResult(False,u"Installing Selected Parcels", caputre(self.driver))
        else:
            click_element(self.driver,By.CSS_SELECTOR,".btn.btn-large.btn-primary")
        time.sleep(1)
        ele_text=get_element_text(self.driver,By.CSS_SELECTOR,"#hostInspectorStep>div>h2")
        ret= u"Inspect hosts for correctness" in ele_text
        return FuncResult(ret,u"Installing Selected Parcels", caputre(self.driver))
    def inspect_hosts(self):
        self.logger.info(u"%sInspect hosts for correctness%s\n"%('+'*12,'+'*12))
        endtime= time.time()+180
        while time.time()<endtime:
            ele_list=find_elements(self.driver,By.CSS_SELECTOR, ".tiny.glyphicon.success.ok_2")
            if len(ele_list)==19:
                break
            elif len(ele_list)==18 and verify_element(self.driver,By.PARTIAL_LINK_TEXT,"echo never > /sys/kernel/mm/transparent_hugepage/defrag"):
                break
        ele_list=find_elements(self.driver,By.CSS_SELECTOR, ".tiny.glyphicon.success.ok_2")
        if len(ele_list)<19:
            return FuncResult(False,u"Inspect hosts for correctness", caputre(self.driver))
        click_element(self.driver,By.CSS_SELECTOR, ".btn.btn-large.btn-primary")
        time.sleep(1)
#        ele_text=get_element_text(self.driver,By.CSS_SELECTOR,".Wizard.container>h1")
        ret= u"express-add-services" in self.driver.current_url
        return FuncResult(ret,u"Inspect hosts for correctness", caputre(self.driver))
    def select_service(self):
        self.logger.info(u"%sselect service%s\n"%('+'*12,'+'*12))
        click_element(self.driver,By.CSS_SELECTOR,"#package_CUSTOM")
#        self.driver.execute_script("$(window).scrollTop(550,0)")
#        service_input_ele_list=find_elements(self.driver,By.CSS_SELECTOR, "#serviceSelector tbody input")
        service_name_list=map(lambda x:x.text,find_elements(self.driver,By.CSS_SELECTOR, "#serviceSelector tbody td:nth-child(2)>label"))
        install_service=self.data["install_service"]
        for service in install_service:
            service_index=get_ele_index(service_name_list, service)
            if service_index !=None:
#                 if u"YARN" in service or u"ZooKeeper" in service:
#                    self.driver.execute_script("$(window).scrollTop(650,0)")
                self.logger.info("%s $('#serviceSelector tbody>tr:nth-child(%s) input').click()"%(service,1+service_index))
                self.driver.execute_script("$('#serviceSelector tbody>tr:nth-child(%s) input').click()"%(1+service_index))
#                service_input_ele_list[service_index].click()
                time.sleep(1)
            else:
                self.logger.error(u"service name [%s] is invalid"% service)
#        click_element(self.driver,By.CSS_SELECTOR,"input[name*=Navigator]")
        click_element(self.driver,By.CSS_SELECTOR,".btn.btn-large.btn-primary")
        ele_text=get_element_text(self.driver,By.CSS_SELECTOR,"#roleAssignmentsStep>div>h2")
        ret=u'Customize Role Assignments' in ele_text
        return FuncResult(ret,u"select service", caputre(self.driver))
    def add_role(self):
        self.logger.info(u"%sdploy role%s\n"%('+'*12,'+'*12))
        self.logger.info(self.data)
        if self.data["host_role_default"]=="no":
            service_name_list=map(lambda x:x.text,find_elements(self.driver,By.CSS_SELECTOR,".row h3 span"))
            for service_name in self.data["host_role"].keys():
                self.logger.info(service_name)
                service_name_index=get_ele_index(service_name_list, service_name)
                service_role_name_list=map(lambda x:x.text,find_elements(self.driver,By.CSS_SELECTOR,".row:nth-child(%s) .name"% (4+2*service_name_index,)))
#                self.logger.info(service_role_name_list)
#                service_role_ele_list=find_elements(self.driver, By.CSS_SELECTOR,".row:nth-child(%s) div>a")
                for role_name in self.data["host_role"][service_name].keys():
                    time.sleep(1)
                    self.logger.info(role_name)
                    role_index=get_ele_index(service_role_name_list,role_name)
                    if self.data["host_role"][service_name][role_name] and role_index!=None:
                        if verify_element(self.driver,By.CSS_SELECTOR,".row:nth-child(%s)>.span3:nth-child(%s)>div+div>a+ul"%(4+2*service_name_index,1+role_index)):
                            self.logger.info("$('.row:nth-child(%s)>.span3:nth-child(%s)>div+div>a+ul>li>a[data-bind*=\"Custom\"]').click()"%(4+2*service_name_index,1+role_index))
                            self.driver.execute_script("$('.row:nth-child(%s)>.span3:nth-child(%s)>div+div>a+ul>li>a[data-bind*=\"Custom\"]').click()"%(4+2*service_name_index,1+role_index))
                        else:
                            self.logger.info("$('.row:nth-child(%s)>.span3:nth-child(%s)>div+div>a').click()"%(4+2*service_name_index,1+role_index))
                            self.driver.execute_script("$('.row:nth-child(%s)>.span3:nth-child(%s)>div+div>a').click()"%(4+2*service_name_index,1+role_index))
                        role_checkbox_list=find_elements(self.driver,By.CSS_SELECTOR,"tbody i")
                        role_hostname=map(lambda x:x.text, find_elements(self.driver,By.CSS_SELECTOR,"tbody>tr>td[data-bind$=\"hostName\"]"))
                        for checkbox in role_checkbox_list:
                            if u" check" in get_element_attribute(checkbox,"class"):
                                checkbox.click()
                                time.sleep(0.5)
                        for hostname in self.data["host_role"][service_name][role_name]:
                            self.logger.info(hostname)
                            hostname_index=get_ele_index(role_hostname,hostname)
                            if hostname_index !=None:
                                role_checkbox_list[hostname_index].click()
                            else:
                                self.logger.error(u"host name is invalid")
                        if not click_element(self.driver,By.CSS_SELECTOR, "form #modalDialog .modal-footer>.btn+.btn"):
                            click_element(self.driver,By.CSS_SELECTOR,"form #modalDialog .modal-footer>.dismissButton")
#                         ok_button=find_elements(self.driver,By.CSS_SELECTOR,"form #modalDialog .modal-footer>.btn-primary")[0]
#                         if get_element_attribute(ok_button,"disabled")==0:
#                             ok_button.click()
#                         else:
#                             click_element(self.driver,By.CSS_SELECTOR, "form #modalDialog .modal-footer>.btn+.btn")
        elif self.data["host_role_default"]=="yes":
            pass
        click_element(self.driver,By.CSS_SELECTOR,"button[data-bind*=\"onClickContinue\"]")
        ele_text=get_element_text(self.driver,By.CSS_SELECTOR,".db-test-connection-view>h2")
        ret=ele_text==u"Database Setup"
        return FuncResult(ret,u"dploy role", caputre(self.driver))
    def Database_setup(self):
        self.logger.info(u"%sDatabase setup%s\n"%('+'*12,'+'*12))
        service_name_list=map(lambda x:x.text,find_elements(self.driver,By.CSS_SELECTOR,".db-test-connection-view tbody h2"))
#        db_hostname_input_ele_list=find_elements(self.driver,By.CSS_SELECTOR,".db-test-connection-view table[class*=\"body\"] .host")
        db_name_input_ele_list=find_elements(self.driver,By.CSS_SELECTOR,".db-test-connection-view table[class*=\"body\"] .name")
        db_username_input_ele_list=find_elements(self.driver,By.CSS_SELECTOR,".db-test-connection-view table[class*=\"body\"] .username")
        db_passwd_input_ele_list=find_elements(self.driver,By.CSS_SELECTOR,".db-test-connection-view table[class*=\"body\"] .password")
        self.driver.execute_script("$('.db-test-connection-view table[class*=\"body\"] .host').val(\"%s\")"%(self.data["Database_setup"]["mysql_hostname"],))
        for service_name in self.data["Database_setup"].keys():
            if u"mysql_hostname" not in service_name:
                service_name_index=get_ele_index(service_name_list, service_name)
                if service_name_index !=None:
                    db_name_input_ele_list[service_name_index].clear()
                    db_name_input_ele_list[service_name_index].send_keys(self.data["Database_setup"][service_name]["Database Name"])
                    db_username_input_ele_list[service_name_index].clear()
                    db_username_input_ele_list[service_name_index].send_keys(self.data["Database_setup"][service_name]["Username"])
                    db_passwd_input_ele_list[service_name_index].clear()
                    db_passwd_input_ele_list[service_name_index].send_keys(self.data["Database_setup"][service_name]["Password"])
                else:
                    self.logger.error(u"service name [] is invalid"%(service_name,))
        time.sleep(1)
#         click_element(self.driver,By.CSS_SELECTOR,".db-test-connection-view label>input[data-bind*=\"showPassword\"]")
#         click_element(self.driver, By.CSS_SELECTOR, ".db-test-connection-view button[data-bind*=\"testConnection\"]")
        self.logger.info("$('.db-test-connection-view label>input[data-bind*=\"showPassword\"]').click()")
        self.driver.execute_script("$('.db-test-connection-view label>input[data-bind*=\"showPassword\"]').click()")
        self.logger.info("$('.db-test-connection-view button[data-bind*=\"testConnection\"]').click()")
        self.driver.execute_script("$('button[data-bind*=\"testConnection\"]').click()")
        endtime=time.time()+30
        while time.time()<endtime:
            result_ele=find_elements(self.driver,By.CSS_SELECTOR,".bold.message>i")
            test_conn_result=map(get_element_attribute,result_ele,["class" for _ in result_ele])
            if len(set(test_conn_result))==1 and \
               True not in ["error" in result for result  in test_conn_result] and \
               True in ["success" in result for result  in test_conn_result]:
                break
            elif True in ["error" in result for result  in test_conn_result]:
                return FuncResult(False,u"Database setup", caputre(self.driver))
            else:
                time.sleep(3)
        click_element(self.driver, By.CSS_SELECTOR, "#bottomButtons button[data-bind*=\"onClickContinue\"]")
        time.sleep(3)
        ele_text=get_element_text(self.driver,By.CSS_SELECTOR,"#reviewStep h2")
        ret=u"Review Changes" in ele_text
        return FuncResult(ret,u"Database setup", caputre(self.driver))
    def config_service(self):
        self.logger.info(u"%sconfig service%s\n"%('+'*12,'+'*12))
        endTime=time.time()+120
        while time.time()<endTime:
            if find_elements(self.driver,By.CSS_SELECTOR,"#reviewStep .param-spec-property"):
                break
        time.sleep(1)
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
        while time.time()<endtime:
            result=get_element_attribute(find_elements(self.driver,By.CSS_SELECTOR,"#commandDetailsStep>div>div:first-child>h2:first-child>i:first-child")[0],"class")
            if u"error" in result:
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
    def cluster_install_finished(self):
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
        ele_text=get_element_text(self.driver,By.CSS_SELECTOR,"#clouderaEulaStep h2")
        if type(ele_text)==type(u"a") and u"End User License Terms and Conditions" in ele_text:
            self.start_install()
        self.choose_cdh()
        self.select_hosts()
        self.Select_Repository()
        self.install_parcels()
        self.inspect_hosts()
        self.select_service()
        self.add_role()
        self.Database_setup()
        self.config_service()
#       Add Hive mysql connector
        self.logger.info(u"%sConfigure Hive mysql connector%s\n"%('+'*12,'+'*12))
        config_hive=configure()
        config_hive.start()
#         self.logger.info("sshpass -p aaaaaa ssh -p 22 -o StrictHostKeyChecking=no root@10.94.1.60 'sh /home/cloudera-cdh-5.7.6/start.sh configure >/dev/null'")
#         os.system("sshpass -p aaaaaa ssh -p 22 -o StrictHostKeyChecking=no root@10.94.1.60 'sh /home/cloudera-cdh-5.7.6/start.sh configure >/dev/null'")
        self.start_service()
        self.cluster_install_finished()