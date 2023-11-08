import threading
import socket

alias = input("Choose an alias: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('SERVER IP', 59000)) #Connect to the server

def client_recieve():
    while True:
        try:
            message = client.recv(1024).decode('utf-8') #Get message from other clients
            if message == "alias?": #If the server is asking for an alias
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print("Error")
            client.close()
            break

def client_send():
    while True:
        message = f'{alias}: {input("")}'
        client.send(message.encode('utf-8'))

recvThread = threading.Thread(target = client_recieve)
recvThread.start()

sendThread = threading.Thread(target = client_send)
sendThread.start()