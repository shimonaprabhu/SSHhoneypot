# SSH Honeypot

## Welcome to the SSH Honeypot GitHub repository

The SSH Honeypot is a Python based SSH shell emulation. Using Paramiko, the SSH honeypot is used to log the attacker's interaction with the shell. 

## Installation

- Create an EC2 instance and set up an elastic IP
- SSH into the instance, where user is the username and localhost is the elastic IP configured on the AWS instance
```
ssh user@localhost
```
- Create a virtual environment and activate it 
```
pip install virtualenv
virtualenv <env_name>
source <env_name>/bin/activate
```
- Install the required dependencies
```
pip install -r requirements.txt
```
- Route the traffic from port 22 (SSH port) to port 2222
```
sudo iptables -A PREROUTING -t nat -p tcp --dport 22 -j REDIRECT --to-port 2222
```
- Run the program
```
python main.py
```
- The logs files are timestamped and created in the current folder, the shell also logs 


