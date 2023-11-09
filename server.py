import threading
import socket
host = 'localhost'
port = 9999

#Create the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("", port))

server.listen()
clients = []

#Send message to client
def broadcast(coordinants, client): #Send coordinate list to client
    for player in clients:
        if player != client:
            print("Sending data. . .")
            player.send(coordinants)
            return
        
#Handle client connections
def handleClient(client):
    while True:
        try:
            message = client.recv(1024) #Message comes from client, set max bytes as 1024
            broadcast(message, client) #Send info to other player
            print("Sending message. . .")
        except socket.error:
            clients.remove(client)
            break #End loop

#Main function to get connection
def recieve():
    while True:
        if len(clients) < 3: #Only accept 2 players at once!
            print("Listening for connections. . .")
            client, address = server.accept() #Waiting for any connection
            clients.append(client)
            print(f"Connection is established with player {len(clients)}.")


            thread = threading.Thread(target = handleClient, args=(client,))  #New thread for client
            thread.start()

if __name__ == "__main__":
    recieve()