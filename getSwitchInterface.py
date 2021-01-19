# -*- coding:utf-8 -*-
import re
import os
import time
import platform
 
def snmpWalk(host, community, oid):
    """
    利用os模块打开一个管道运行snmpwalk工具结合host，团体字符串，OID获取交换机路由器状态
        OID	                描述	         备注	请求方式
   .1.3.6.1.2.1.1.1.0	  获取系统基本信息	 SysDesc	GET
   .1.3.6.1.2.1.2.1.0	  网络接口的数目	   IfNumber	GET
   .1.3.6.1.2.1.2.2.1.2	网络接口信息描述	 IfDescr	WALK
   .1.3.6.1.2.1.2.2.1.3	网络接口类型	     IfType	WALK
   .1.3.6.1.2.1.2.2.1.4	接口发送和接收的最大IP数据报[BYTE]	IfMTU	WALK
   .1.3.6.1.2.1.2.2.1.5	接口当前带宽[bps]	                IfSpeed	WALK
   .1.3.6.1.2.1.2.2.1.6	接口的物理地址	                   IfPhysAddress	WALK
   .1.3.6.1.2.1.2.2.1.8	接口当前操作状态[up|down]	        IfOperStatus	WALK
    """
    result = os.popen('snmpwalk -v 2c -c '   community   ' '  host   ' '   oid).read().split('\n')[:-1]
    return result
 
def getSwitchinfo(host,community):
    device_mib = snmpWalk(host, community, 'RFC1213-MIB::sysDescr')
    SwitchInfoString = item.split(':')[3].strip()
    return SwitchInfoString
   
def getPortDevices(host,community):
    """
    获取端口信息
    """
    device_mib = snmpWalk(host, community, 'RFC1213-MIB::ifDescr')
    device_list = []
    for item in device_mib:
        device_list.append(item.split(':')[3].strip())
    return device_list
 
def getPortStatus(host,community):
    """
    获取端口状态信息
    """
    device_mib = snmpWalk(host, community, 'RFC1213-MIB::ifOperStatus')
    device_list = []
    for item in device_mib:
        device_list.append(item.split(':')[3].strip())
    return device_list
 
def main():
        host = input("Enter IP Address:\n")
        print("Enter String:")
        community =input("Enter Community String:\n")
        print('=' * 10   host   '=' * 10)
        start = time.time()
        switchinfo = getSwitchinfo(host,community)
        #print("system info: {0}".format(switchinfo))  #system info: H3C Switch S2626-PWR Software Version 5.20.99, Release 1109Copyright©2004-2017 New H3C Technologies Co., Ltd. All rights reserved.
        
        DeviceList = getPortDevices(host,community)
        DeviceStatus = getPortStatus(host,community)
        for item in DeviceList:
                index = DeviceList.index(item)
                #以思科为例：1表示up；2表示down；3表示testing；4表示unknown；5表示dormant；6表示notPresent；7表示lowerLayerDown
                #print("Port:" item " Status:" DeviceStatus[index]) #Port: GigabitEthernet1/0/1 Status: 1
                
if __name__ == '__main__':
    main()
