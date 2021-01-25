# Register your models here.
from .models import Information
from .models import ip_state
from .models import switch
from .models import Department
from django.utils.safestring import mark_safe

from extra_apps.ExecuteSwitchCommds import execSwitchCmd
import xadmin


# global aclNumber = 1000   #ACL全局号，防止表冲突

class DepartmentInformation(object):
    list_display = ('department', 'department_detail', 'revise_date')
    search_fields = ('department', 'department_detail')
    list_filter = ('department', 'department_detail')
    pass


class IpInformation(object):
    list_display = ('ip_number', 'ip_state', 'ip_department', 'revise_date')
    search_fields = ('ip_number', 'ip_state', 'ip_department')
    list_filter = ('ip_number', 'ip_state', 'ip_department')
    pass


class SwitchInformation(object):
    list_display = ('switch_number', 'ip', 'community', 'location', 'model_type', 'version')
    search_fields = ('switch_number', 'ip', 'community', 'location', 'model_type', 'version')
    list_filter = ('switch_number', 'ip', 'community', 'location', 'model_type', 'version')
    pass


class PortInformation(object):
    list_display = ('switch_port_number', 'band', 'location', 'seat_number', 'status', 'bind_ip', 'bind_mac')
    search_fields = ('switch_port_number', 'band', 'location', 'seat_number', 'status', 'bind_ip', 'bind_mac')
    list_filter = ('switch_port_number', 'band', 'location', 'seat_number', 'status', 'bind_ip', 'bind_mac')
    pass


class StaffInformation(object):
    list_display = ('staff_name', 'job_number', 'Department', 'seat_number', 'mac_address', 'ip_address', 'port_switch',
                    'revise_date')
    search_fields = ('staff_name', 'job_number', 'Department', 'port_switch', 'ip_address')
    list_filter = ('Department', 'port_switch', 'staff_name', 'ip_address', 'port_switch')

    def getCommands(self, obj):
        """
        根据交换机品牌，产生对应的命令集
        """
        brand = obj.port_switch_id.factory  #brand 为交换机品牌，其格式需为'Huawei'、'Cisco'二者其一！
        commands = []
        try:
            if brand == 'Huawei':
                acl_number = '4' + obj.portnumber    #需要提供交换机的端口号，格式须为如'001'，'002'
                commands.append('system-view')
                if flag:
                    commands.append('arp static {0} {1}'.format(obj.ip_address_id, obj.mac_address))
                    commands.append('mac number {0}'.format(acl_number))
                    commands.append('rule 5 permit souce-mac {0}'.obj.mac_address)
                    commands.append('rule 10 deny')
                    commands.append('interface {0}'.format(obj.port_switch))  # GigabitEthernet0/0/15
                    commands.append('traffic-filter inbound acl {0}'.format(acl_number))
                 else:
                    commands.append('undo arp static {0} {1}'.format(obj.ip_address_id, obj.mac_address))
                    commands.append('undo mac number {0}'.format(acl_number))
            elif brand == 'Cisco':
                acl_number = 'mac' + obj.portnumber      #需要提供交换机的端口号，格式须为如'001'，'002'
                commands.append('config terminal')
                if flag:
                    commands.appned('arp {0} {1} arpa'.format(obj.ip_address_id, obj.mac_address))
                    commands.append('mac access-list extended {0}'.format(acl_number))
                    commands.append('permit host {0} any'.format(obj.mac_address))
                    commands.append('deny any any')
                    commands.append('interface {0}'.format(obj.port_switch))  # FastEthernet0/1
                    commands.append('mac access-group {0} in'.format(acl_number))
                 else:
                    commands.appned('no arp {0} {1}'.format(obj.ip_address_id, obj.mac_address))
                    commands.appned('no mac access-list extended {0}'.format(acl_number))

        except Exception as e:
            print('---------->', e)
        return commands

    def save_models(self):
        """
        在保存员工信息时，调用mac和交换机绑定的功能，同时改变ip和switch的状态为已分配。
        :return:
        """
        obj = self.new_obj
        request = self.request
        obj.save()
        # bind_ip_mac()
        # bind_mac_switch()
        # 必须确定存在
        obj.ip_address.ip_state = 0
        obj.port_switch.bind_ip = obj.ip_address.ip_number
        obj.port_switch.state_mac = obj.mac_address
        # 执行交换机命令 绑定用户ip和mac 绑定交换机和mac

        flag = true
        commands = getCommands(obj, flag)
        execSwitchCmd(obj.port_switch.state_ip, obj.port_switch.account_switch, obj.port_switch.password_switch,
                      commands)

        obj.ip_address.save()
        obj.port_switch.save()

    def delete_model(self):
        """
        在删除员工信息时，调用mac和交换机解绑的功能，同时，改变ip和switch的状态为未分配。
        :return:
        """
        obj = self.obj
        
        flag = false
        commands = getCommands(obj, flag)
        # 执行用户ip和mac绑定
        execSwitchCmd(obj.port_switch.state_ip, obj.port_switch.account_switch, obj.port_switch.password_switch, commands)
        obj.ip_address.ip_state = 1
        obj.port_switch.state_ip = " "
        obj.port_switch.state_mac = " "

        obj.ip_address.save()
        obj.port_switch.save()
        obj.delete()
        pass


class GlobalSettings(object):
    site_title = "网络后台管理系统"
    site_footer = "版权所有"
    # menu_style = "accordion"


class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(Department, DepartmentInformation)
xadmin.site.register(ip_state, IpInformation)
xadmin.site.register(switch, SwitchInformation)
xadmin.site.register(Information, StaffInformation)
xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)
# Register your models here.
