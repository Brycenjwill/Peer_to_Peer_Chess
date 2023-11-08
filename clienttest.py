import socket
s = socket.socket()
port = 56789

s.connect(('IP', port))

print(s.recv(1024))
s.close()