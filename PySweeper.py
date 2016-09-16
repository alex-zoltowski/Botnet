#!/usr/bin/python
import multiprocessing
import subprocess
import os
import socket
from argparse import ArgumentParser
import sys

class PySweeper:

    #subnet = "111.111"
    def __init__(self, network_ip):
        self.network_ip = network_ip

    def subnet(self, subnet):
        return subnet_sweep(self.network_ip + "." + str(subnet))

    def network(self):
        return network_sweep(self.network_ip)

def pinger(job_q, results_q):
    DEVNULL = open(os.devnull,'w')
    while True:
        ip = job_q.get()
        if ip is None: break

        try:
            subprocess.check_call(['ping','-c1',ip],
                                  stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)
    except socket.herror:
        return None, None, None

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def print_ips(ips):
    ips.sort()

    for ip in ips:
        name, alias, addresslist = get_hostname(ip)
        if name is None:
            print ip + "   -   " + "hostname not found"
        else:
            print ip + "   -   " + name

def network_sweep(network_ip):
    ips = []
    for x in range(1, 255):
        sn_ips = subnet_sweep(network_ip + "." + str(x))
        for ip in sn_ips:
            ips.append(ip)
        print network_ip + "." + str(x) + " swept"

    return ips

def subnet_sweep(subnet):
    ips = []
    pool_size = 255

    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [ multiprocessing.Process(target=pinger, args=(jobs,results))
                 for i in range(pool_size) ]

    for p in pool:
        p.start()

    for i in range(1,255):
        jobs.put(str(subnet) + '.{0}'.format(i))

    for p in pool:
        jobs.put(None)

    for p in pool:
        p.join()

    while not results.empty():
        ip = results.get()
        ips.append(str(ip))

    return ips
