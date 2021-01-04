class TelnetClient():
    def __init__(self,):
        self.tn = telnetlib.Telnet()
        time.sleep(0.2)

    # 此函数实现telnet登录主机
    def login(self,host_ip,username,password,port=23):
        try:
            # self.tn = telnetlib.Telnet(host_ip,port=23)
            self.tn.open(host_ip,port)
        except:
            logging.critical('网络连接失败'+repr(host_ip))
            return False
        # 等待login出现后输入用户名，最多等待10秒
        self.tn.read_until(b'Username: ',timeout=1)
        self.tn.write(username.encode('ascii') + b'\n')
        self.tn.read_until(b'Password: ',timeout=1)
        self.tn.write(password.encode('ascii') + b'\n')
        # 延时两秒再收取返回结果，给服务端足够响应时间
        time.sleep(0.2)
        # 获取登录结果
        # read_very_eager()获取到的是的是上次获取之后本次获取之前的所有输出
        command_result = self.tn.read_very_eager().decode('ascii')
        if 'Login incorrect' not in command_result:
            return True
        else:
            return False

    # 此函数实现执行传过来的命令，并输出其执行结果
    def execute_some_command(self,command):
        logging.info('开始执行交换机命令：'+command)
        # 执行命令
        self.tn.write(command.encode('ascii')+b'\n')
        time.sleep(0.2)
        # 获取命令结果
        a = []
        a.append(('--- More ---').encode('ascii'))
        command_result = self.tn.read_very_eager().decode('ascii')
        while True:
            b,c,d = self.tn.expect(a,timeout=1)
            command_result += d.decode('ascii')
            if 0 == b:
                time.sleep(0.2)
                self.tn.write(b' \n') #不用\r\n来继续
            else:
                break
        logging.info('命令执行结果:'+repr(command_result))
        if 'Error:' in command_result :
            logging.critical('执行结果中可能包含错误`Error：`，脚本强制退出')
            sendWxMsg('流量调度系统交换机命令执行出现错误，请及时处理！')
            sys.exit()
        return command_result

    # 退出telnet
    def logout(self):
        self.tn.write(b"exit\n")
        self.tn.close()
