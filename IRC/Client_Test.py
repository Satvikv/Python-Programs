import socket
import sys
import select


# from javax.swing import JFrame
class SocketClientTest:
    ServerIP = "127.0.0.1"
    ServerPort = 1100
    test = '123'
    addressFamily = (ServerIP, ServerPort)

    def __init__(self):
        self.messageString = ''
        self.clientName = ""
        self.serverMessage = ""
        self.channelName = ""
        self.messageInput = ""
        self.clientSock = socket.socket()
        self.command = ""

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

    def sendtoserver(self, soc):
        # self.messageInput=	self.chatTextBox.get()


        self.serverMessage = soc.recv(1024).decode('UTF-8').strip()
        if self.serverMessage == "PROVIDEANAME":
            self.messageInput = input("Register with a user name: ")
            soc.send(bytes(self.messageInput, 'UTF-8'))
            print(self.messageInput)
        elif self.serverMessage.startswith("LIST"):
            print("List of available groups ", self.serverMessage)
        elif self.serverMessage.startswith("PROVIDEAGROUPNAME"):
            self.channelName = input("Provide a Chat room name: ")
            soc.send(bytes(self.channelName, 'UTF-8'))
        elif self.serverMessage.startswith("SENDCOMMANDS"):
            # print(self.serverMessage.split(" ")[2:])
            self.command = sys.stdin.readline()
            soc.send(bytes(self.command, 'UTF-8'))
        elif self.serverMessage.startswith("MESSAGE"):
            for each in self.serverMessage.split(":")[1:]:
                message = " " + each
            print(message)
            message = input("Response: ")
            soc.send(bytes(message, 'UTF-8'))


            # self.fHandle.write(channelName.join(":".join(self.messageInput)))
            # soc.send(self.channelName.join(":".join(self.messageInput)))
            # self.chatTextBox.delete(0, len(self.messageInput))

    def socketrun(self):
        self.clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSock.connect(self.addressFamily)
        print("Connected to server")
        sock_list = [sys.stdin, self.clientSock]
        while True:
            self.sendtoserver(self.clientSock)

"""
sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send_msg(sock):
    while True:
        data = sys.stdin.readline()
        sock.sendto(data, target)

def recv_msg(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        sys.stdout.write(data)

Thread(target=send_msg, args=(sock_send,)).start()
Thread(target=recv_msg, args=(sockfd,)).start()
"""
s = SocketClientTest()
print(s.test)
s.socketrun()
