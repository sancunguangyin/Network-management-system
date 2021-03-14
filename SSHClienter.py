import paramiko
import time
import logging


class SSHClienter():
    def __init__(self):
        self.client = paramiko.SSHClient()
        time.sleep(0.2)

    # 此函数实现SSH登录主机
    def login(self,host_ip,username,password,port=22):
        try:
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())	#自动确认陌生设备
            self.client.connect(hostname=hostname,username=username,password=password) #连接
        except:
            logging.critical('网络连接失败'+repr(host_ip))
            return False
        chan = client.invoke_shell()			#打开channel
        chan.send('screen-length 0 tem \n')		#输入命令
        time.sleep(1)
        chan.send('dis cur \n')
        time.sleep(5)							#设置等待时间
        info = chan.recv(99999).decode()		#接收输出信息
        return info



    # 此函数实现执行传过来的命令，并输出其执行结果
    def execute_command(self,command):
        logging.info('开始执行交换机命令：'+command)
        # 执行命令
        stdin, stdout, stderr = self.client.exec_command(command) 
        return stdout.read().decode()

    # 退出ssh连接
    def logout(self):
        self.client.close()
