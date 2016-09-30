import socket
#
def is_port_open(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if s.connect_ex((ip, int(port))) == 0:
        print "Port 22 open!"
        return True
    else:
        print "Port 22 closed!"
        return False

def check_if_ip(ip):
    try:
        socket.inet_aton(ip)
    except socket.error:
        return False
    return True
