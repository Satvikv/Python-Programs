import sys
import io
import socket
import tkinter as tk
#from javax.swing import JFrame
class SocketClientTest:
	 ServerIP="127.0.0.1"
	 ServerPort=1100
	 test='123'
	 def __init__(self):
		 self.messageString=''
		 self.top=tk.Tk()
		 self.clientName=""
		 
		 self.channelName=""
		 self.messageInput=""
	      	
	 def showTK(self):	 
		 self.chatFrame=tk.Frame(self.top,bg='white')
		 self.chatFrame.pack()
		 self.chatTextBox=tk.Entry(self.top)
		 self.chatTextBox.pack(side="top")
		 self.chatTArea=tk.Text(self.top)
		 self.chatTArea.pack(side="bottom")
		 self.chatButton=tk.Button(self.top,text="Send",command=self.sendToServer)
		 self.chatButton.pack(side="right")
		 self.top.mainloop()
		 
	 def sendToServer(self):
		 self.messageInput=	self.chatTextBox.get()
		 print(self.messageInput)
		 self.chatTArea.insert(tk.INSERT,self.messageInput+"")
		 self.chatTArea.pack(side="bottom")
		 if( not self.messageInput.startsWith("CHANNELSLIST")):
                    #messageArea.append(clientName+ ":" + textInput+"\n");
					self.chatTArea.insert(tk.INSERT,(clientName+":"+self.messageInput+"\n"))
                    
		 #self.fHandle.write(channelName.join(":".join(self.messageInput)))
		 self.clientSock.send(channelName.join(":".join(self.messageInput)))
		 self.chatTextBox.delete(0,len(self.messageInput))
	 def socketRun(self):
		 self.clientSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		 self.clientSock.connect(ServerIP,ServerPort);
		 self.sendToServer()
	 
    
    
	

s=SocketClientTest()
print(s.test)
s.showTK()
