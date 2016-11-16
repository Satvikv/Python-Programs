import socket

with socket.socket(AF_INET,SOCK_STREAM) as serversock:
     serversoc.bind('127.0.0.1',10045)
     serversoc.listen()
     consock, addr= serversock.accept()
     print(consock)
