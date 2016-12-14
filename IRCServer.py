import socket
import threading
import sys
import errno
import select
from time import sleep

class IRCServer:
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    HOST, PORT = "localhost", 1104
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
        self.clientsock_list=list()

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
        print("IRC server is listening on port",self.serversock.getsockname()[1])
        self.clientsock_list=[self.serversock]
        while True:
            r_list,wlist,err_list=select.select(self.clientsock_list,[],[])
            for sock in r_list:
               if sock is self.serversock:
                    clientconn, address = sock.accept()
                    #clientconn.settimeout(60)
                    self.clientsock_list.append(clientconn);
                    print("Client %s,%s is connected"%address)
                    clientconn.send(b'PROVIDEANAME')

               else:
                    client_data=sock.recv(1024)
                    if client_data:
                        self.check_username(sock)
                        self.handleclientmessages(sock, client_data.decode('UTF-8').strip())
                    else:
                        self.check_username(sock)
                        print("User %s is down"%self.username)
                        self.clientsock_list.remove(sock)
                        sock.close();
    def handleclientmessages(self, clientconn, message):
        # self.request is the TCP socket connected to the client
        manual="For User registration: USER <u_name> \n For creating a group: CREATE <group_name> \n For list of groups: LIST \n For joining multiple groups: JOINMULTIPLE <group_1> <group_2> .. \n For list of users in a group: LISTOFUSERS <group_name> \n To send a message to a group: MSG <groupname> <message> \n For leaving a group: LEAVE <group_name> \n For personal message to a specific user: @<to_user_name> <message> \n To exit IRC: EXIT \n For manual: MANUAL\n\n\n"


            # self.request.sendall("ProvideAName")
        try:

            if message.startswith("USER"):
                self.username = message.split(" ")[1]
                if self.username in self.clients:
                    clientconn.sendall(b'Already exists provide a unique name.')
                else:
                    self.clients[self.username] = clientconn
                    clientconn.send(b'user registered')
            elif message.startswith("CREATE"):
                channelname = message.split()[1]
                if channelname in self.channels:
                    clientconn.send(b'PROVIDE A UNIQUE GROUP NAME: ')
                    print("room already exists")
                else:
                    print("%s Group created"%channelname)
                    self.channels.add(channelname)
                    print(self.username)
                    if channelname in self.client_in_channels:
                        print(self.client_in_channels[channelname])
                        self.client_in_channels[channelname].append(self.username)
                    else:
                        self.client_in_channels[channelname] = [self.username]

                    print("Channels and clients ",self.client_in_channels)
                    msg="Group <%s> is successfully created"%channelname
                    clientconn.send(bytes(msg,'UTF-8'))

            elif message.startswith("JOIN"):
                channels = message.split(" ")[1:]
                for channelname in channels:
                    if channelname not in self.channels:
                        clientconn.send(b'Provide a correct Group Name')
                    else:
                        oldclientlist = self.client_in_channels[channelname]
                        if self.username in oldclientlist: clientconn.send(b'Already joined')
                        oldclientlist.append(self.username)
                        msg="You have successfully joined <%s> group"%channelname
                        clientconn.send(bytes(msg,'UTF-8'))
            elif message=="LIST":
                print("client message:",message)
                listcmd="LIST of available groups: "
                if len(self.channels)==0: listcmd+="No active groups"
                else:
                    for chn in self.channels:
                        listcmd += "%s, "%chn
                    listcmd=listcmd[:-1]
                clientconn.send(bytes(listcmd, 'UTF-8'))

            elif message.startswith("MSG"):
                channel = message.split(" ", 2)[1]
                message = message.split(" ",2)[2][0:]
                if channel in self.client_in_channels:
                    if self.username in self.client_in_channels[channel]:
                        self.broadcastToClients(channel, message, self.username)
                    else:
                        clientconn.send(byes("ERROR_INVALID_CHANNEL:You are not in %s group"%channel,'UTF-8'))
                else:
                    clientconn.send(bytes("ERROR_INVALID_CHANNEL: There is no such group %s"%channel,'UTF-8'))
            elif message.startswith("@"):
                to_user = message.split(" ", 1)[0][1:]
                from_user = self.username
                pmsg = message.split(" ", 1)[1][0:]
                ch_name = ""
                if to_user in self.clients:
                    to_client=self.clients[to_user]
                    to_client.send(bytes("From <%s>: %s" % (from_user, pmsg), 'UTF-8'))
                else:
                    clientconn.send(bytes("%s is unavailable" % to_user,'UTF-8'))

            elif message.startswith("JOINMULTIPLE"):
                 for channel in message.split(" ")[1:]:
                     if(channel in self.client_in_channels):
                        self.client_in_channels[channel].append()
                     else:
                        clientconn.send(bytes("This is not a valid group name",'UTF-8'))
            elif message.startswith("LEAVE"):
                 group_name=message.split()[1]
                 if group_name in self.client_in_channels:
                     self.client_in_channels[group_name].remove(self.username)
                     if len(self.client_in_channels[group_name]) ==0:
                         self.client_in_channels.pop(group_name)
                         self.channels.remove(group_name)
                     clientconn.send(bytes("You have successfully left %s group"%group_name,'UTF-8'))
                 else:
                     clientconn.send(b'Group doesnot exist')
            elif message.startswith("EXIT"):
                 client_name=self.username
                 for k,v in self.client_in_channels.items():
                     if client_name in v:
                         v.remove(client_name)
                 temp_obj=self.client_in_channels
                 for k in list(temp_obj):
                     if len(temp_obj[k])==0:
                         self.channels.remove(k)
                         temp_obj.pop(k)
                 self.client_in_channels=temp_obj;
                 #print(self.client_in_channels)
                 self.clients.pop(client_name)
                 clientconn.send(b'Bye')
            elif message.startswith("LISTOFUSERS"):
                 grp_name=message.split()[1]
                 msg="LIST of users in %s group:"%grp_name.upper()
                 if grp_name in self.client_in_channels:
                     grp_users=self.client_in_channels[grp_name]
                     if self.username in grp_users:
                        for user in grp_users:
                           if user==self.username:
                              user="You"
                           msg = msg + "%s," % user
                        clientconn.send(bytes(msg,'UTF-8'))
                     else:
                         clientconn.send(b'You are not a part of the group')

                 else:
                     clientconn.send(b'Group doesnot exist')
            elif message.startswith("MANUAL"):
                clientconn.send(bytes("MANUAL %s"%manual,'UTF-8'))
            else:
                clientconn.send(b'ERROR_INVALID_MESSAGE')

        except socket.error as e:
            print(e)
            self.serversock.close()
            sys.exit(1)
        else:
            # got a message, do something :)
            print(message)
        """
            try:



                    with self.clients_lock:
                        self.check_username(clientconn)

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

            while True:
                self.data = clientconn.recv(1024)
                if self.data:
                    self.data = self.data.decode('UTF-8').strip()
                                else:
                clientconn.send(b'invalidcommand')
            """

    def broadcastToClients(self, channelName, message, sendername):
        print(message," ",sendername)
        clientslist = self.client_in_channels[channelName]
        for clientname in clientslist:
            if clientname != self.username:
                msg = "MESSAGE:"+" IN <%s>"%channelName+"FROM <%s>: "%sendername+message
                print("Server sent ",msg)
                self.clients[clientname].send(bytes(msg, 'UTF-8'))
            else:
                msg = "MESSAGE:" + " IN <%s>" % channelName + "FROM <you>: "+ message
                self.clients[clientname].send(bytes(msg, 'UTF-8'))
            # just send back the same data, but upper-cased
            # self.request.sendall(self.data.upper())


    def check_username(self,conn):

        for user_name in self.clients:
            if self.clients.get(user_name) is conn:
                self.username=user_name
    """
    def handlepersonalmessages(self,message):
        to_user = message.split(" ", 1)[0][1:]
        from_user = self.username
        pmsg = message.split(" ", 1)[1][0:]
        ch_name=""
        if to_user in self.clients:
            return from_user, pmsg, self.clients[to_user], to_user
        else:
            raise Exception("%s is unavailable" % to_user)

    """



if __name__ == "__main__":
    # Create the server, binding to localhost
    serverObj = IRCServer()
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    serverObj.listen()
