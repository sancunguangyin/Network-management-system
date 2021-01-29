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
            ����osģ���һ���ܵ�����snmpwalk���߽��host�������ַ�����OID��ȡ������·����״̬
            """
            result = os.popen('snmpwalk -v 2c -c '   community   ' '  host   ' '   oid).read().split('\n')[:-1]
            return result
        
        """
        ===============================
        ����Ϊ�ⲿ�ӿں���
        ===============================
        """
            
        def getSwitchinfo(self):
            """
            ��ȡ������ϵͳ������Ϣ
            """
            device_mib = snmpWalk(self._host, self._community, 'RFC1213-MIB::sysDescr')
            SwitchInfoString = device_mib.split(':')[3].strip()
            return SwitchInfoString
            
        def getSwitchName(self):
            """
            ��ȡ������
            """
            device_mib = snmpWalk(self._host, self._community, 'RFC1213-MIB::SysLocation')
            SwitchName = device_mib.split(':')[3].strip()
            return SwitchInfoString
         
         def getSwitchName(self):
            """
            ��ȡ����������λ�ã�����еĻ���
            """
            device_mib = snmpWalk(self._host, self._community, 'RFC1213-MIB::SysName')
            SwitchLocation = device_mib.split(':')[3].strip()
            return SwitchLocation
            
        def getPortDevices(slef):
            """
            ��ȡ�˿ں�
            """
            device_mib = snmpWalk(self._host, self._community, 'RFC1213-MIB::ifDescr')
            device_list = []
            for item in device_mib:
                device_list.append(item.split(':')[3].strip())
            return device_list
         
        def getPortStatus(self):
            """
            ��ȡ�˿�״̬��Ϣ
            ���أ�UP|DOWN
            """
            device_mib = snmpWalk(self._host, self._community, 'RFC1213-MIB::ifOperStatus')
            device_list = []
            for item in device_mib:
                device_list.append(item.split(':')[3].strip())
            return device_list

