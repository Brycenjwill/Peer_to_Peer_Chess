import socket

s = socket.socket()
print("Socket successfully created")

port = 56789

#Bind socket to port, first value is the ip we will be listening for
s.bind(('', port))
print(f"Socket binded to port {port}")

#Set socket to listen mode, sets the limit to 1 connections.
s.listen(1)
print("Socket is listening")

#Run
while True:
    #Set variables to be gotten on accept, addr is the ip
    c, addr, = s.accept()
    print('Got connection from', addr)
    message = "Thank you for connecting with us!"

    #Send info back to client, encoded as bytes. 
    c.send(message.encode())
    #Close connection once message haas been sent
    c.close()
