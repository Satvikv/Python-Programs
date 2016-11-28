import socketserver

class IRCHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    HOST, PORT = "localhost", 1100
    clients=set()
    client_in_channels=dict()
    channels=set()
    def handle(self):
        # self.request is the TCP socket connected to the client
        print("an incoming connection detected")
        while(True):
           self.request.sendall("ProvideAName")
           self.data = self.request.recv(1024).strip()
           print("{} wrote:".format(self.client_address[0]))
           print(self.data)
           if (self.data.startswith("USER")):
               username=self.data.split(" ")[1]
               if username in self.clients.keys():
                  self.request.sendall("ProvideAName")
               else:
			      self.clients.add({username:self.client_address[0]})
           elif(self.data.startswith("MSG")):          
		          channel=self.data.split()[1]
				  message=self.data.split()[2]
				  if channel in client_in_channels.keys():
				     self.broadcastToClients(channel,message);
				  else:
				     self.request.sendall("ERROR_INVALID_CHANNEL")


	def broadcastToClients(self,channelName,message):
        clientsList=client_in_channels[channelName];
         for client in clientsList
		     send.request.sendall(message)

        # just send back the same data, but upper-cased
        #self.request.sendall(self.data.upper())

if __name__ == "__main__":


    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((IRCHandler.HOST, IRCHandler.PORT), IRCHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print("serving")
    server.serve_forever()
