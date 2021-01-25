#requirements：
#pysnmp and pyasn1

from pysnmp.entity.rfc3413.oneliner import cmdgen

oTable = {
    "entLogicalCommunity": (1, 3, 6, 1, 2, 1, 47, 1, 2, 1, 1, 4),
    "entPhysicalModelName": (1, 3, 6, 1, 2, 1, 47, 1, 1, 1, 1, 13, 1),
    "entLogicalDescr": (1, 3, 6, 1, 2, 1, 47, 1, 2, 1, 1, 2),
    "dot1dBasePort": (1, 3, 6, 1, 2, 1, 17, 1, 4, 1, 1),
    "dot1dTpFdbPort": (1, 3, 6, 1, 2, 1, 17, 4, 3, 1, 2),
    "dot1dBasePortIfIndex": (1, 3, 6, 1, 2, 1, 17, 1, 4, 1, 2),
    "dot1dTpFdbAddress": (1, 3, 6, 1, 2, 1, 17, 4, 3, 1, 1),
    "ifDescr": (1, 3, 6, 1, 2, 1, 2, 2, 1, 2),
    "ifName": (1, 3, 6, 1, 2, 1, 31, 1, 1, 1, 1),
    "ifSpeed": (1, 3, 6, 1, 2, 1, 2, 2, 1, 5),
    "ifAlias": (1, 3, 6, 1, 2, 1, 31, 1, 1, 1, 18),
    "sysName": (1, 3, 6, 1, 2, 1, 1, 5, 0),
    "sysDescr": (1, 3, 6, 1, 2, 1, 1, 1, 0),
    "dot3StatsDuplexStatus": (1, 3, 6, 1, 2, 1, 10, 7, 2, 1, 19),
    "ifAdminStatus": (1, 3, 6, 1, 2, 1, 2, 2, 1, 7),
    "ifOperStatus": (1, 3, 6, 1, 2, 1, 2, 2, 1, 8),
    "atPhysAddress": (1, 3, 6, 1, 2, 1, 3, 1, 1, 2),
    "ipAdEntAddr": (1, 3, 6, 1, 2, 1, 4, 20, 1, 1),
    "ipAdEntIfIndex": (1, 3, 6, 1, 2, 1, 4, 20, 1, 2),
    "ARP": (1, 3, 6, 1, 2, 1, 3, 1, 1, 2),
    "ipNetToMediaTable": (1, 3, 6, 1, 2, 1, 4, 22, 1, 2)
}


def walk(dswitch, commVlan, oid  ):
    """This function will return the table of OID's that I am walking"""
    errorIndication, errorStatus, errorIndex, \
        generic = cmdgen.CommandGenerator().nextCmd(cmdgen.CommunityData('test-agent', commVlan), \
        cmdgen.UdpTransportTarget((dswitch, 161)), oid)
    if errorIndication:
        return errorIndication
    return generic

def getarptab(host, community):
    """
    snmp扫描并获取核心交换机的arp表
    input:
        host:switch's ip
        community:团体属性
    output:arp_table
    """
    entaddr = walk(host, community, oTable["ipNetToMediaTable"])
    arp_table = []
    for i in entaddr:
        temp = ''
        for j in i:
            temp += str(j)
        temp = temp.replace("SNMPv2-SMI::mib-2.4.22.1.2.", "")
        temp = temp[temp.find('.')+1:]
        temp = temp.split(' = ')
        arp_table.append(temp)
