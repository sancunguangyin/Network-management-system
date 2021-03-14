form SSHClienter import SSHClienter

# 执行DHCP配置文件的读写操作
class DHCP():
    def __init__(self, host_, username_, password_):
        """
        :param host:主机ip地址
        :param username:用户名
        :param password:密码
        """
        ssh_client = SSHClineter()
        host = host_
        username = username_
        password = password_
    
    def conf_read(subnet):
        """
        bindinfo: 绑定信息的数据结构
        subnet： 子网号
        """
        msg = ''
        commands_read = ['cd /etc/dhcp', 
                'vi {0}.conf'.format(subnet),
                '此处为DHCP配置文件读命令'，
                 'systemctl restart dhcpd']
        if ssh_client.login(host,username,password):
            for command in commands :
                msg += ssh_client.execute_some_command(commands_read)
            ssh_client.logout()    
        return msg
      
    def conf_read_all(subnet_tab):
        """
        subnet_tab: 一个集和，包含所有子网网段
        """
        ret = []
        for subnet in subnet_tab:
            ret.apend(conf_read(commands_read))
        return ret     
      
    def conf_writer(bindinfo, subnet):
        msg = ''
        commands_wirte = ['cd /etc/dhcp', 
                'vi {0}.conf'.format(subnet),
                '此处为DHCP配置文件写命令'，
                 'systemctl restart dhcpd']
        if ssh_client.login(host,username,password):
            for command in commands :
                msg += ssh_client.execute_some_command(commands_write)
            ssh_client.logout()    
        return msg
