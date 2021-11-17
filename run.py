import os
import subprocess
import keyboard



os.system("ls -al")
os.system("python3 main.py &")


while True:
    print('tip tip')
    if keyboard.read_key() == 'q':
        os.system('ps -ef | grep "python main.py" | kill -9 awk "{print $1}"')
        print('yoohoo')
        break
