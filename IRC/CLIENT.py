#! /usr/bin/env python
# coding: utf-8
#
# WhatsUp Client
# Yet another simple socket multi-user chating program
#
#
# @author: Xin Wang <sutarshow#gmail.com>
# @date: 18-09-2013
#

import socket
import time
import logging
import sys
import select

HOST = '127.0.0.1'
PORT = 8018
TIMEOUT = 5
BUF_SIZE = 1024


class WhatsUpClient():

    def __init__(self, host=HOST, port=PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        logging.info('Connecting to %s:%s' % (host, port))
        sock_list=[sys.stdin,self.sock]
        while 1:
            try:
                read_list,write_list,error_list=select.select(sock_list,[],[])
                for sock in read_list:
                    if sock==self.sock:
                        buf = self.sock.recv(BUF_SIZE)
                        sys.stdout.write(buf.decode('UTF-8'))
                        print("enter")
                    else:
                        cmd = sock.readline()
                        if cmd.strip() == '!q':
                            sys.exit(1)
                        self.sock.send(bytes(cmd,'UTF-8'))
            except:
                self.sock.close()

    def run(self):
        pass


def main():
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] %(levelname)s: %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p')
    client = WhatsUpClient()

if __name__ == '__main__':
    main()