#Nihar T.
#Shimona P.
#Pratibha A.

import paramiko
import threading
import socket
import logging

HOST_KEY = paramiko.RSAKey(filename='../server.key')


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='ssh_honeypot.log')


class sshHoneyPot(paramiko.ServerInterface):

    client_ip = None
    
    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        logging.info('new logging attempt from ip {} username: {} password: {}'.format(
            self.client_ip, username, password))
        return paramiko.AUTH_SUCCESSFUL



def handle_connection(client, addr):
    
    client_ip = addr[0]
    logging.info('New connection coming from {}', client_ip)

    transport = paramiko.Transport(client_ip)
    transport.add_server_key(HOST_KEY)

    server_handler = SSHServerHandler()

    transport.start_server(server=server_handler)
    
    channel = transport.accept(1)
    
    if channel is None:
        print("Channel is none")


def main():

    try:
        print('dbg 1')
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('dbg 2')
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print('dbg 3')
        server.bind(('',2222))
        print('dbg 4')
        server.listen(100)

        print('dbg 5')

        flag = True
        while(flag):
            try:
                client_socket, client_addr = server.accept()
                thread.start_new_thread(handleConnection, (client_socket,))
            except:
        
                print('Error')

    except Exception as e:
        print('Big error')
        print(e)



main()
