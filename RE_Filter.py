import netmiko
from netmiko import ConnectHandler
#from netmiko import exceptions
#from paramiko.ssh_exception import SSHException
import os
from getpass import getpass, getuser
os.chdir("C:\\Users\\AXTON\\Desktop\\Automation_IT_Infra")
def get_credentials():
    username = input('Enter username : ')
    #password = None
    #while not password:
    password = getpass('Enter password : ')
    return username, password

username, password = get_credentials()
device_type = 'juniper'
devices = open('devices.txt')
row = 0
os.chdir("C:\\Users\\AXTON\\Desktop\\Automation_IT_Infra")

for IP in devices:
    dev = {
        'device_type' : 'juniper',
        'ip' : IP,
        'username' : username,
        'password' : password
              }

    for ip_b in devices:
    #print(ip_b)
        
        outside_in = ("set firewall family inet filter OUTSIDE-ACCESS-IN term " + "RE_FILTER" + " from source-address " +  ip_b)
        print(outside_in)
    
