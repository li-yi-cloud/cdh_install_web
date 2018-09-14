# -*- coding: utf-8 -*-
'''
Created on 2016年6月12日

@author: Minkyo
发送邮件模块
'''
import smtplib  
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage
import os,time,datetime  

def send_mail(file_name):  
    sender = 'liuyy1@hunktimes.com' 
    receiver = ['liuyy1@hunktimes.com',]
    smtpserver = 'smtp.exmail.qq.com'  
    username = 'liuyy1@hunktimes.com'  
    password = 'lyy495287Lgeo'  
    
    file_name = u'E:/workspace/service_config/src/testlog/' + file_name 
    
    yes_day = str(datetime.date.today() + datetime.timedelta(days=-1))
    year = yes_day.split('-')[0]
    month = yes_day.split('-')[1]
    day = yes_day.split('-')[2]

    msgRoot = MIMEMultipart('related')  
    msgRoot['Subject'] = u'LEAP自动化测试报告'
    msgRoot['From'] = sender
    msgRoot['To'] = ";".join(receiver)  
    #msgRoot['To'] = []
    
    print "=======================begin send mail"
    #构造附件  
    att = MIMEText(open(file_name, 'r').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'  
    att["Content-Disposition"] = 'attachment; filename="LEAP自动化测试报告.html"'  
    
    html = """
            <html>
                <head></head>
                <body>
                    <p>尊敬的LEAP组成员，附件是LEAP自动化测试报告，请查收<br>
                </body>
            </html>
            """
    content = html
    att3 = MIMEText(content, 'html', 'utf-8') 

    msgRoot.attach(att)
    msgRoot.attach(att3)  
    
    smtp = smtplib.SMTP()  
    smtp.connect(smtpserver)  
    smtp.login(username, password)  
    smtp.sendmail(sender, receiver, msgRoot.as_string())  
    smtp.quit()  

if __name__ == '__main__':
    file_name = u'E:/workspace/service_config/src/testlog/'+u'LEAP_Cluster_config-2016-09-21-11_09_52.html'
    send_mail(file_name)
