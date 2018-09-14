#coding:utf-8

# *************************************
#    选择服务
# *************************************
service_checkbox_path_css={
    "HDFS":".HDFS",
    "YARN":".YARN",
    "Hive":".HIVE",
    "HBase":".HBASE",
    "Pig":".PIG",
    "Sqoop":".SQOOP",
    "Oozie":".OOZIE",
    "Zookeeper":".ZOOKEEPER",
    "Flume":".FLUME",
    "Metrics":".AMBARI_METRICS",
    "Kafka":".KAFKA",
    "Spark2":".SPARK2",
    "Hue":".HUE",
    "Slider":".SLIDER"
    }

#====================================================================
# *************************************
#    指派Master
# *************************************
master_add_btn={
    "HBase Master":".HBASE_MASTER-add",
    "ZooKeeper Server":".ZOOKEEPER_SERVER-add",
    "Metrics Collector":".METRICS_COLLECTOR-add",
    "Kafka Broker":".KAFKA_BROKER-add"
    }

#====================================================================

# *************************************
#    管理主界面元素按钮
# *************************************
system_manage_icon_element_path={
    u"logo":"img[src='/img/logo.png']",
    u"LEAP系统管理":".logo+a:span",
    u"首页 ":".menu_home",
    u"监控":".menu_dashboard",
    u"服务":".menu_services",
    u"主机":".menu_hosts",
    u"告警":".menu_alerts",
    u"管理":"li:nth-child(6) .menu_admin",
    u"管理LEAP":"li:nth-child(7) .menu_admin",
    u"视图":".menu_views",
    u"集群名称":".cluster-name:span:nth-child(2)",
    u"集群操作":".cluster-name:span:nth-child(6)",
    u"集群警告":".cluster-name:span:nth-child(12)",
    u"用户":".btn-admin"
    }

#====================================================================

# *************************************
#    主界面用户按钮下拉菜单子元素
# *************************************
manager_user_element_path={
    u"产品手册":"productManual",
    u"":"#technicalSupport",
    u"关于":"#about",
    u"管理LEAP":"#manage-ambari",
    u"设置":"li:nth-child(13) a",
    u"退出":"#sign-out"
    }
#====================================================================

# *************************************
#    管理主界面服务组件按钮
# *************************************
componets_icon_element_path={
    "LEAP-HDFS":"a[href*='HDFS'] div",
    "LEAP-YARN":"a[href*='YARN'] div",
    "LEAP-MapReduce2":"a[href*='MAPREDUCE2'] div",
    "LEAP-Hive":"a[href*='HIVE'] div",
    "LEAP-HBase":"a[href*='HBASE'] div",
    "LEAP-Pig":"a[href*='PIG'] div",
    "LEAP-Sqoop":"a[href*='SQOOP'] div",
    "LEAP-Oozie":"a[href*='OOZIE'] div",
    "LEAP-ZooKeeper":"a[href*='ZOOKEEPER'] div",
    "LEAP-Flume":"a[href*='FLUME'] div",
    "LEAP-Metrics":"a[href*='AMBARI_METRICS'] div",
    "LEAP-Kafka":"a[href*='KAFKA'] div",
    "LEAP-Spark2":"a[href*='SPARK2'] div",
    "LEAP-Slider":"a[href*='SLIDER'] div",
    "LEAP-Storm":"a[href*='STORM'] div",
    "LEAP-Leapid":"a[href*='LEAPID'] div",
    "LEAP-PriestProcess":"a[href*='PRIESTSERVICE'] div",
    "LEAP-PriestSQL":"a[href*='PRIESTSQL'] div",
    "LEAP-Solr":"a[href*='SOLR'] div",
#    "":"",
    }
componets_url={
    "LEAP-HDFS":u"/#/main/services/HDFS/summary",
    "LEAP-YARN":u"/#/main/services/YARN/summary",
    "LEAP-MapReduce2":u"/#/main/services/MAPREDUCE2/summary",
    "LEAP-Hive":u"/#/main/services/HIVE/summary",
    "LEAP-HBase":u"/#/main/services/HBASE/summary",
    "LEAP-Pig":u"/#/main/services/PIG/summary",
    "LEAP-Sqoop":u"/#/main/services/SQOOP/summary",
    "LEAP-Oozie":u"/#/main/services/OOZIE/summary",
    "LEAP-ZooKeeper":u"/#/main/services/ZOOKEEPER/summary",
    "LEAP-Flume":u"/#/main/services/FLUME/summary",
    "LEAP-Metrics":u"/#/main/services/AMBARI_METRICS/summary",
    "LEAP-Kafka":u"/#/main/services/KAFKA/summary",
    "LEAP-Spark2":u"/#/main/services/SPARK2/summary",
    "LEAP-Slider":u"/#/main/services/SLIDER/summary",
    "LEAP-Storm":u"/#/main/services/STORM/summary",
    "LEAP-Leapid":u"/#/main/services/LEAPID/summary",
    "LEAP-PriestProcess":u"/#/main/services/PRIESTSERVICE/summary",
    "LEAP-PriestSQL":u"/#/main/services/PRIESTSQL/summary",
    "LEAP-Solr":u"/#/main/services/SOLR/summary",
#    "":"",
    }
#====================================================================

# *************************************
#    管理主界面操作按钮及子元素
# *************************************
handle_components_element_path={
    u"操作":".btn-green",
    u"添加服务":".btn-green+ul .icon-plus+span",
    u"开始所有":".btn-green+ul .icon-play+span",
    u"停止所有":".btn-green+ul .icon-stop+span",
    u"重启所有必须的":".btn-green+ul icon-repeat+span"
    }
#====================================================================

# *************************************
#    服务管理界面按钮元素
# *************************************
service_page_icon_element_path={
    u"操作":"#service-actions-dropdown-btn",
    u"快速链接":"#quick-links-dropdown-btn",
    u"配置":"#configs-service-tab",
    u"热图":"#heatmap-service-tab",
    u"概览":"#summary-service-tab"
    }

service_quick_links="find_elements(driver, method[3],'.quick-links-dropdown li:a')"

service_config_page_icon_path={
    u"组":"button[class$='first']",
    u"管理配置组":".link-left-pad:span",
    u"过滤":".filter-combobox button",
    }

filter_rules="find_elements(driver, method[3],\".filter-combobox li\")"

group_menue="find_elements(driver, method[3],'button[class$=\"first\"]~ul li')"
#====================================================================
# *************************************
#    角色管理选项
# *************************************
role_manage_opt={
    "Cluster User":"0",
    "Cluster Administrator":"1",
    "Cluster Operator":"2",
    "Service Administrator":"3",
    "Service Operator":"4",
    "None":"5"
    }