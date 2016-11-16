import socket


clientsock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
clientsock.connect(('127.0.0.1',10045)

clientsock.sendAll('Hello Sever')

response=''
while response!=None:
      response=clientsock.recv(1024)
      print(response.strip())
