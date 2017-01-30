import socket
import threading
import sys
import errno
from time import sleep

class IRCServer:
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    HOST, PORT = "localhost", 1100
    clients = dict()

    channels = set()
    clients_lock=threading.Lock()
    def __init__(self):
        self.data = ''
        self.serversock = None
        self.connected_client = None
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversock.bind((self.HOST, self.PORT))
        self.username = ""
        self.client_in_channels = dict()

    """
    def serverstart(self):
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversock.bind((self.HOST, self.PORT))
        self.serversock.listen()
        connclient, address = self.serversock.accept()
        print("an incoming connection detected")
        self.connected_client = (connclient, address)
        return self.connected_client
    """

    def listen(self):
        self.serversock.listen(5)

        while True:
            clientconn, address = self.serversock.accept()
            #clientconn.settimeout(60)
            threading.Thread(target=self.handleclientmessages, args=(clientconn, address)).start()


    def handleclientmessages(self, clientconn, address):
        # self.request is the TCP socket connected to the client

        while True:
            # self.request.sendall("ProvideAName")
            try:
                print("loop started")
                clientconn.sendall(b'PROVIDEANAME')
                self.data = clientconn.recv(1024)
                print(self.data)
                if self.data:
                    self.data = self.data.decode('UTF-8').strip()
                    with self.clients_lock:
                        if self.data.startswith("USER"):
                            self.username = self.data.split(" ")[1]
                            if self.username in self.clients:
                                continue
                            else:
                                self.clients[self.username] = clientconn
                                print(self.clients)
                                print("user registered")

                                break
                        else:
                            clientconn.send(b'invalidcommand')
                else:
                    raise Exception("Client Discusc")
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    sleep(1)
                    print('No data available')
                    continue
                else:
                    print(e)
                    sys.exit(1)
            else:
                # got a message, do something :)
                print("got a message, do something :)")
        while True:
            try:
                clientconn.sendall(b'SENDCOMMANDS')

                self.data = clientconn.recv(1024)
                if self.data:
                    self.data = self.data.decode('UTF-8').strip()
                    with self.clients_lock:
                        self.check_username(clientconn)
                        if self.data.startswith("CREATE"):
                            print("ghfgfg")
                            channelname = self.data.split()[1]
                            if channelname in self.channels:
                                clientconn.send(b'PROVIDEAGROUPNAME: ')
                                print("room already exists")
                                continue
                            else:
                                print("room created")
                                self.channels.add(channelname)
                                print(self.username)
                                if channelname in self.client_in_channels:
                                    print(self.client_in_channels[channelname])
                                    self.client_in_channels[channelname].append(self.username)
                                else:
                                    self.client_in_channels[channelname]=[self.username]
                                print(self.client_in_channels)

                                print(self.client_in_channels)
                        elif self.data.startswith("JOIN"):
                            channelname = self.data.split()[1]
                            if channelname not in self.channels:
                                clientconn.send(b'ProvideACORRECTGroupName')
                            else:
                                oldclientlist = self.client_in_channels[channelname]
                                print(self.username)
                                if self.username in oldclientlist: continue
                                oldclientlist.append(self.username)
                        elif self.data.startswith("LIST"):
                            listcmd = 'LIST '+str(self.channels)
                            clientconn.send(bytes(listcmd, 'UTF-8'))
                        elif self.data.startswith("MSG"):
                            channel = self.data.split(" ",2)[1]
                            message = self.data.split()[2][0:]
                            if channel in self.client_in_channels:
                                if self.username in self.client_in_channels[channel]:
                                    self.broadcastToClients(channel, message, self.username)
                                else:
                                    clientconn.send(b'ERROR_INVALID_CHANNEL')
                            else:
                                clientconn.send(b'ERROR_INVALID_CHANNEL')
                        else:
                            clientconn.send(b'ERROR_INVALID_MESSAGE')
                else:
                    raise Exception("Client Discusc")
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    sleep(1)
                    print('No data available')
                    continue
                else:
                    # a "real" error occurred
                    print(e)
                    sys.exit(1)
            else:
                print("got a message, do something :)")
            """
            while True:
                self.data = clientconn.recv(1024)
                if self.data:
                    self.data = self.data.decode('UTF-8').strip()
            """

    def broadcastToClients(self, channelName, message, sendername):
        clientslist = self.client_in_channels[channelName]
        for clientname in clientslist:
            if clientname != self.username:
                message = "MESSAGE:" + sendername + ":" + message
                self.clients[clientname].send(bytes(message, 'UTF-8'))
            # just send back the same data, but upper-cased
            # self.request.sendall(self.data.upper())

    def handle_user(self, clientconn):
        clientconn.send(b'PROVIDEAUSERNAME')

    def check_username(self,conn):

        for user_name in self.clients:
            if self.clients.get(user_name) is conn:
                self.username=user_name

if __name__ == "__main__":
    # Create the server, binding to localhost on port 9999
    serverObj = IRCServer()
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    serverObj.listen()
