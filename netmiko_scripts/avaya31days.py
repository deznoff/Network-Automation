import getpass
import re
from netmiko import ConnectHandler

switch = input('Input stack name:')
username = input('Input username:')
password = getpass.getpass('Input password:')
avaya_edge = {
    'device_type': 'extreme_ers',
    }
avaya_edge['host'] = switch
avaya_edge['username'] = username
avaya_edge['password'] = password

net_connect = ConnectHandler(**avaya_edge)
#net_connect.find_prompt()
output = net_connect.send_command('show int verbose')
#print(output)
output = output.splitlines()
#print(output)
new_string = ""
for line in output:
        if line[0:4] == "Unit" or line[0:6] == "    La" or line[0:20] == "    Oper Status:  Do" :
                new_string += line

down_ports = ""
final_string = new_string.split("Unit/")
for port in final_string:
    if port[16:32] == "Oper Status:  Do":
        down_ports += port + "\n"
#print(down_ports)

port_list = down_ports.split("\n")
port_list = [x for x in port_list if x]

unused_ports = ""
for port in port_list:
    if int(re.findall(r'\d+', port)[2]) >= 62:
        unused_ports += port + "\n"

print(unused_ports)
