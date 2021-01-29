# -*- coding:utf-8 -*-
import re
import os
import platform
   
class SnmpScaner(object):
        def __init__(self, host, commnity):
            self._host = host
            self._commnity = commnity
            
        def snmpWalk(host, community, oid):
            """
            利用os模块打开一个管道运行snmpwalk工具结合host，团体字符串，OID获取交换机路由器状态
            """
            result = os.popen('snmpwalk -v 2c -c '   community   ' '  host   ' '   oid).read().split('\n')[:-1]
            return result
        
        """
        ===============================
        以下为外部接口函数
        ===============================
        """
            
        def getSwitchinfo(self):
            """
            获取交换机系统基本信息
            """
            device_mib = snmpWalk(self._host, self._community, 'RFC1213-MIB::sysDescr')
            SwitchInfoString = device_mib.split(':')[3].strip()
            return SwitchInfoString
            
        def getSwitchName(self):
            """
            获取机器名
            """
            device_mib = snmpWalk(self._host, self._community, 'RFC1213-MIB::SysLocation')
            SwitchName = device_mib.split(':')[3].strip()
            return SwitchInfoString
         
         def getSwitchName(self):
            """
            获取交换机所在位置（如果有的话）
            """
            device_mib = snmpWalk(self._host, self._community, 'RFC1213-MIB::SysName')
            SwitchLocation = device_mib.split(':')[3].strip()
            return SwitchLocation
            
        def getPortDevices(slef):
            """
            获取端口号
            """
            device_mib = snmpWalk(self._host, self._community, 'RFC1213-MIB::ifDescr')
            device_list = []
            for item in device_mib:
                device_list.append(item.split(':')[3].strip())
            return device_list
         
        def getPortStatus(self):
            """
            获取端口状态信息
            返回：UP|DOWN
            """
            device_mib = snmpWalk(self._host, self._community, 'RFC1213-MIB::ifOperStatus')
            device_list = []
            for item in device_mib:
                device_list.append(item.split(':')[3].strip())
            return device_list

