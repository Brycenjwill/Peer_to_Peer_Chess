# Overview

This is an extension of my "Chess" program in order to allow for users to play against one another from different devices.

[Peer to Peer Chess Demo and Code Overview](https://youtu.be/clDdPHm2t2I)

# Network Communication

The architecture I used was a mix between client-server and peer to peer, as the server  acts as an intermediary between two peers. The program is set to assign to port 9999, and uses TCP for connections. The messages sent between the clients are formatted as 'utf-8' and are decoded/encoded on recieve/send. 

# Development Environment

I created this program in VSCode in Python. The main libraries I used are as follows:
- Pygame for the client program interface
- Socket for the server setup/ connections
- Threading to allow for the server/clients to constantly be waiting for messages while also carrying out other tasks.

# Useful Websites

{Make a list of websites that you found helpful in this project}
* [Python Socket Documentation](https://docs.python.org/3/library/socket.html)
* [Python Threading Documentation](https://docs.python.org/3/library/threading.html)

# Future Work

{Make a list of things that you need to fix, improve, and add in the future.}
* Checkmate detection for the client programs
* Processes to allow for one server to run multiple games at once/after each other
* Change the display of the client program so that the team you are playing as is drawn to the bottom
(ex. so that the player who is playing as the black team will have the black pieces on the bottom of the board.)