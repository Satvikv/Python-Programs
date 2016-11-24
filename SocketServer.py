import socketserver

class IRCHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    HOST, PORT = "localhost", 9999
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((IRCHandler.HOST, IRCHandler.PORT), IRCHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print("serving")
    server.serve_forever()