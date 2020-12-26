# encoding=utf-8
import paramiko
import time
client = paramiko.SSHClient()
client.load_system_host_keys()
 
# connect to client
client.connect('192.168.254.141',22,'test','test',allow_agent=False,look_for_keys=False)
 
# get shell
ssh_shell = client.invoke_shell()
# ready when line endswith '>' or other character
while True:
    line = ssh_shell.recv(1024)
    #print line
    if line and line.endswith('>'):
        break;
 
# send command
ssh_shell.sendall( 'ping 192.168.254.142' + '\n')
 
# get result lines
lines = []
while True:
    line = ssh_shell.recv(1024)
    if line and line.endswith('>'):
        break;
    lines.append(line)
result = ''.join(lines)
 
# print result
print result
