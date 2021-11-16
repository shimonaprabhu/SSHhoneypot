#Nihar T.
#Shimona P.
#Pratibha A.

import paramiko
import threading
import socket
import logging
import sys
from datetime import date

today = date.today()

HOST_KEY = paramiko.RSAKey(filename='server.key')
PORT = 2222
logfile = 'ssh_honeypot_{}.log'.format(today.strftime('%m_%d_%Y'))

logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO,
    filename = logfile)


class sshHoneyPot(paramiko.ServerInterface):

    client_ip = None
    
    def __init__(self, client_ip):
        print("instantiating sshHoneyPot")
        print("client_ip {}".format(client_ip))
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

    def check_channel_shell_request(self, chanid):
        self.event.set()
        return True


def parsecommand(cmd, channel, client_ip):
    
    cmd = cmd.strip()

    logging.info('client {} is running comand {}'.format(client_ip, cmd))

    if cmd == 'ls':
        channel.send('users.txt\r\n')
    elif cmd == 'pwd':
        channel.send('/home/users\r\n')
    elif cmd == 'exit':
        #sys.exit(0)
        return False
    elif cmd == '':
        #do nothing
        return True
    else:
        channel.send('Permission denied.\r\n')

    return True

def handle_connection(client, addr):
    
    client_ip = addr[0]
    logging.info('New connection coming from {}'.format(client_ip))

    print("starting transport setup")
    transport = paramiko.Transport(client)
    print("trying to add server key")
    transport.add_server_key(HOST_KEY)

    print("added key")

    try:
        server_handler = sshHoneyPot(client_ip)
        print("going to start server_handler")
        transport.start_server(server=server_handler)
        channel = transport.accept(10)
    except Exception as e:
        print(e)

    print("started_server")
    print("setup channel")
    
    if channel is None:
        print("Channel is none")

    run_flag = True

    server_handler.event.wait(50)
    channel.settimeout(50)

    channel.send("Welcome to Ubuntu\r\n")
    while(run_flag):
        channel.send('ubuntu@ip-172-31-40-131:~$ ')
        cmd = ''
        while not (cmd.endswith('\n') or cmd.endswith('\r') or cmd.endswith('\r\n')):
            cmd_part = channel.recv(1024)
            print(type(cmd_part))
            #channel.send(cmd_part)
            cmd += str(cmd_part, 'UTF-8')
        
        
        run_flag = parsecommand(cmd, channel, client_ip)
        print(run_flag)


    print("Leaving run_flag while loop")
    channel.close()
    logging.info('Conection from {} closing'.format(client_ip))




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

        connect_flag = True

        
        print("Entering connect_flag while")
        while(connect_flag):
            try:
                client_socket, client_addr = server.accept()
                threading.Thread(target=handle_connection, args=(client_socket, client_addr)).start()
            except Exception as e:
                print('Error')
                print(e)
                connect_flag = False


    except Exception as e:
        print('Big error')
        print(e)



main()
