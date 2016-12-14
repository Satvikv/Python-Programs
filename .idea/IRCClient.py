import socket
import sys
import select

# from javax.swing import JFrame
class SocketClientTest:
    ServerIP = "127.0.0.1"
    ServerPort = 1104
    test = '123'
    addressFamily = (ServerIP, ServerPort)

    def __init__(self):
        self.messageString = ''
        self.clientName = ""
        self.serverMessage = ""
        self.channelName = ""
        self.messageInput = ""
        self.clientSock = socket.socket()
        self.command=""

    """
    def showTK(self):
        self.chatFrame = tk.Frame(self.top, bg='white')
        self.chatFrame.pack()
        self.chatTextBox = tk.Entry(self.top)
        self.chatTextBox.pack(side="top")
        self.chatTArea = tk.Text(self.top)
        self.chatTArea.pack(side="bottom")
        self.chatButton = tk.Button(self.top, text="Send", command=self.sendToServer)
        self.chatButton.pack(side="right")
        self.top.mainloop()
    """

    def sendtoserver(self, soc,sock_list):
        print("Test")
        # self.messageInput=	self.chatTextBox.get()



        # self.fHandle.write(channelName.join(":".join(self.messageInput)))
        #soc.send(self.channelName.join(":".join(self.messageInput)))
        #self.chatTextBox.delete(0, len(self.messageInput))

    def socketrun(self):
        self.clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSock.connect(self.addressFamily)
        soc=self.clientSock
        socket_list=[sys.stdin,soc]
        print("Connected to server")
        print("For User registration: USER <u_name> \n For creating a group: CREATE <group_name> \n For list of groups: LIST \n For joining multiple groups: JOINMULTIPLE <group_1> <group_2> .. \n For list of users in a group: LISTOFUSERS <group_name> \n  To send a message to a group: MSG <groupname> <message> \n For leaving a group: LEAVE <group_name> \n For personal message to a specific user: @<to_user_name> <message> \n To exit IRC: EXIT \n For manual: MANUAL\n\n\n")
        while True:
            r_list, w_list, err_list = select.select(socket_list, [], [])
            for socket_obj in r_list:

                if socket_obj == soc:
                    #print("Server sent a msg")

                        self.serverMessage = soc.recv(1024).decode('UTF-8').strip()
                        if self.serverMessage:
                            #print("SERVER MESSAGE", self.serverMessage)
                            if self.serverMessage.startswith("PROVIDEANAME"):
                                sys.stdout.write('Register with a user name: [USER <u_name>]\n')

                            elif self.serverMessage.startswith("LIST"):
                                sys.stdout.write("%s\n" % self.serverMessage)
                                # soc.send(bytes(self.channelName,'UTF-8'))
                            elif self.serverMessage.startswith("MESSAGE"):
                                message =self.serverMessage.split(":", 1)[1][0:]
                                sys.stdout.write(message+'\n')
                            elif self.serverMessage.startswith("From"):
                                sys.stdout.write(self.serverMessage+"\n")

                            elif self.serverMessage.startswith("Bye"):
                                sys.stdout.write(self.serverMessage+'\n')
                                sys.exit(1)
                            elif self.serverMessage.startswith("MANUAL"):
                                sys.stdout.write(self.serverMessage.split(" ",1)[1][0:]+'\n')
                            else:
                                print("SERVER's MESSAGE", self.serverMessage)
                            sys.stdout.write('>>>')

                            """
                            elif self.serverMessage.startswith("SENDCOMMANDS"):
                                #print(self.serverMessage.split(" ")[2:])
                                self.command=sys.stdin.readline()
                                soc.send(bytes(self.command,'UTF-8'))
                            """

                            #     soc.send(bytes(message,'UTF-8'))
                        else:
                            print("Server is down")
                            socket_obj.close()
                            sys.exit(1)


                else:
                    #print("Waiting for a command")
                    cmd = socket_obj.readline()
                    soc.send(bytes(cmd, 'UTF-8'))
                sys.stdout.flush()



s = SocketClientTest()
print(s.test)
s.socketrun()
