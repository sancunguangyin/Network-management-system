from SSHClienter import SSHClienter

# 执行多条交换机命令
def execSwitchCmds( host, username, password, commands):
    '''
    :param host:主机ip地址
    :param username:用户名
    :param password:密码
    :param commands:列表命令集
    '''
    logging.info('开始执行交换机命令【'+repr(commands)+'】')
    # return True
    ssh_client = SSHClienter()
    msg = ''
    # 如果登录结果返加True，则执行命令，然后退出
    if ssh_client.login(host,username,password) :
        #msg += telnet_client.execute_some_command('system-view')
        for command in commands :
            msg += ssh_client.execute_some_command(command)
        telnet_client.logout()    
    return msg
