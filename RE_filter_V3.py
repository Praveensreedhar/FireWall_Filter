import netmiko
from netmiko import ConnectHandler
#from netmiko import exceptions
#from paramiko.ssh_exception import SSHException
import os
from getpass import getpass, getuser
from tqdm import tqdm
from tqdm import tqdm
import time
from termcolor import colored, cprint

os.chdir("C:\\Users\\AXTON\\Desktop\\Automation_IT_Infra")
def get_credentials():
    username = input('Enter username : ')
    #password = None
    #while not password:
    password = getpass('Enter password : ')
    return username, password
print("Before running the script please make sure, IP adddress details are copied into  /AUTOMATION/FILTER in .txt format and mention the file name below with .txt extension")
ip_list = input("Enter the filename which contails IP details to be aaded in RE_Filter : ")
term_name1 = ip_list[ :- 4]
#print(term_name1)
#term_name = input("Enter the term name : ")
ip_add_list = open(ip_list)

f = ip_add_list.readlines()

username, password = get_credentials()
device_type = 'juniper'
devices = open('devices.txt')
row = 0

netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)


for IP in devices:
    dev = {
        'device_type' : 'juniper',
        'ip' : IP,
        'username' : username,
        'password' : password
              }
    cprint("Connecting to " + IP, 'blue')
    
    global filter_name


    try:
        connection_1 = ConnectHandler(**dev)
        filter_check = connection_1.send_command("show configuration | display set | match lo0 | match filter")
        filter_split = filter_check.split()
        filter_name = filter_split[-1]
        print(filter_name)
        print("Building Configuration for " + IP + "with filter name " + filter_name)
        for i in tqdm(range(10)):
            time.sleep(0.3)
        for ip_b in f:
          
            outside_in = ("set firewall family inet filter " + filter_name + " term Accept" + " from source-address " +  ip_b)
            print(outside_in)
            connection_1.send_config_set(outside_in, exit_config_mode=False)
            #connection_1.commit()
        cprint("Pushing configuration to " + IP, 'green')
        for i in tqdm(range(3)):
            time.sleep(0.2)
        print ("Commmiting configuration to ", IP)
        for i in tqdm(range(5)):
            time.sleep(0.2)
        connection_1.send_config_set("commit")
        connection_1.disconnect()
    except netmiko_exceptions as e:
        cprint("Failed to login..... " + IP, 'red')