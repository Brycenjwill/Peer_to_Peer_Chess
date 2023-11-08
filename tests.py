import sys
import socket
#s stands for socket
#AF_INET is the IPV4 address, SOCK_STREAM is the connection oriented TCP (the node where the connection is established)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print("Socket successfully created!")
except socket.error as err:
    print(f'Socket creation failed with error {err}')

#default port for the socket
port = 80

#Set host for connecting
try:
    host_ip = socket.gethostbyname('www.github.com')
#gaierror is a DNS error
except socket.gaierror:
    print(f"Error resolving the host")
    #End if host error
    sys.exit()

#Connect to host
s.connect((host_ip, port))
print(f"Socket has succesfully connected to Github on port == {host_ip}")