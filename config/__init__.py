#coding:utf-8
'''
公共配置参数
'''

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
authorized_keys_path= BASE_DIR + u"\\Interaction\\config\\id_rsa"
TEST_URL = 'http://172.17.200.67:8080/#/home'
root_password="hundsun"
HOST = '172.17.200.67'
host_port="22"

#postgresql config
USER = 'ambari'
PASSWORD = 'bigdata'

#script config
__all__=["invariable_conf"]
from invariable_conf import service_checkbox_path_css,master_add_btn,system_manage_icon_element_path,\
     manager_user_element_path,componets_icon_element_path,componets_url,\
     handle_components_element_path,service_page_icon_element_path,\
     service_quick_links,service_config_page_icon_path,filter_rules,\
     group_menue,role_manage_opt