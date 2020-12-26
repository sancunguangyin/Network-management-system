# -*- coding:utf-8 -*-
import re
import os
import time
import platform
 
def snmpWalk(host, community, oid):
    """
    利用os模块打开一个管道运行snmpwalk工具结合host，团体字符串，OID获取交换机路由器状态
    """
    result = os.popen('snmpwalk -v 2c -c '   community   ' '  host   ' '   oid).read().split('\n')[:-1]
    return result
 
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
        print("Enter IP Address:")
        host = raw_input()
        print("Enter String:")
        community =raw_input()
        print('=' * 10   host   '=' * 10)
        start = time.time()
        print("system info")
        DeviceList = getPortDevices(host,community)
        DeviceStatus = getPortStatus(host,community)
        for item in DeviceList:
                index = DeviceList.index(item)
                print("Port:" item " Status:" DeviceStatus[index])
 
if __name__ == '__main__':
    main()
