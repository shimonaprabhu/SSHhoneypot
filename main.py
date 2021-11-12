#Nihar T.
#Shimona P.
#Pratibha A.

import paramiko
import threading
import socket
import logging

HOST_KEY = paramiko.RSAKey(filename='server.key')
PORT = 2222

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='ssh_honeypot.log')


class sshHoneyPot(paramiko.ServerInterface):

    client_ip = None
    
    def __init__(self, client_ip):
        print("instantiating sshHoneyPot")
        self.client_ip = client_ip
        self.event = threading.Event()

    def check_auth_publickey(self, username, key):
        print("in check_auth_publickey")
        logging.info('public key from ip {} username: {} key:{}'.format(
            self,client_ip, username, key))
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_password(self, username, password):
        print("in check_auth_password")
        logging.info('new logging attempt from ip {} username: {} password: {}'.format(
            self.client_ip, username, password))
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        logging.info('client called check_channel_request ({}): {}'.format(
            self.client_ip, kind))
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED


def handle_connection(client, addr):
    
    client_ip = addr[0]
    logging.info('New connection coming from {}'.format(client_ip))

    print("starting transport setup")
    transport = paramiko.Transport(client_ip)
    print("trying to add server key")
    transport.add_server_key(HOST_KEY)

    print("added key")

    try:
        server_handler = sshHoneyPot(client_ip)
        print("going to start server_handler")
        transport.start_server(server=server_handler)
    except Exception as e:
        print(e)

    print("started_server")
    
    channel = transport.accept(1)
    print("setup channel")
    
    if channel is None:
        print("Channel is none")


def main():

    try:
        print('dbg 1')
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('dbg 2')
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print('dbg 3')
        server.bind(('',PORT))
        print('dbg 4')
        server.listen(100)

        print('dbg 5')

        flag = True
        while(flag):
            try:
                client_socket, client_addr = server.accept()
                threading.Thread(target=handle_connection, args=(client_socket, client_addr)).start()
            except Exception as e:
        
                print('Error')
                print(e)
                logging.info(e)

    except Exception as e:
        print('Big error')
        print(e)



main()
