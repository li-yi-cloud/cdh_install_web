#conding:utf-8
'''
Created By  
@LiJunlei
20170616
'''
import subprocess,re
from helper.Corelogger import logerror,loginfo 

class read_config(object):
    def __init__(self):
        ret=[]
        with open("host.conf","r") as cf:
            for i in cf.readlines():
                ret1=[x for x in re.split(r"[\|\||\n|\r]",i) if x !=""]
                if ret1:
                    ret.append(ret1)
        self.conf=ret

def shell_command(command,info="",prin_t=True):
    loginfo(command)
    cm=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    _,err=cm.communicate()
    if cm.returncode != 0:
        logerror(err)
        logerror("Non zero exit code:%s executing: %s" % (cm.returncode, info))
        raise StandardError
class configure(object):
    def __init__(self):
        conf=read_config()
        self.conf=conf.conf
    def start(self):
        for node in self.conf:
            ip,sshport=node[0],node[3]
            shell_command("ssh -p %s -o StrictHostKeyChecking=no root@%s 'cp /opt/cm-5.11.1/share/cmf/lib/mysql-connector-java-5.1.42-bin.jar /opt/cloudera/parcels/CDH/jars/'"%(sshport,ip),"copy mysql-collector to cdh")
            shell_command("ssh -p %s -o StrictHostKeyChecking=no root@%s 'ln -s /opt/cloudera/parcels/CDH/jars/mysql-connector-java-5.1.42-bin.jar /opt/cloudera/parcels/CDH/lib/hive/lib/mysql-connector-java-bin.jar'"%(sshport,ip))

if __name__=="__main__":
    config_hive=configure()
    config_hive.start()