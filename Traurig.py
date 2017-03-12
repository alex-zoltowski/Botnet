from Tkinter import *
import tkMessageBox as mbox
import tkFileDialog
import tkSimpleDialog
import socket
from threads import Botnet

class Traurig(Frame):

    #self.currentips = []

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.Traurig_Setup()

    def Traurig_Setup(self):

        botnet = Botnet("/etc/ips", "/etc/pass")
        botnet.connect()
        botnet.send_command("ls -la")
        botnet.print_output()
        botnet.disconnect()

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        hostmenu = Menu(menubar)
        hostmenu.add_command(label='From File', command=self.onFromFile)
        hostmenu.add_command(label='Ping Scan', command=self.onPingScan)
        hostmenu.add_command(label='Load Previous', command=self.onLoadPrev)
        hostmenu.add_command(label='Check Port', command=self.onCheckPort)
        menubar.add_cascade(label='Host', menu=hostmenu)

    def onFromFile(self):
        #list of ips, each on new line
        pass
        '''
        filepath = tkFileDialog.askopenfilename()
        ips = open(filepath, 'r')
        self.currentips = []
        for x in len(ips):
            currentips.append(x)
        '''


    def onPingScan(self):
        #open new window to plug in options
        pass

    def onLoadPrev(self):
        #open new window with previous hosts timestamped for easily redo-able configurations
        pass

    def onCheckPort(self):
        #ask the user if they have a file with ips and ports to check, if so then go to onFileCheckPort
        #else go to onEnterCheckPort
        answer = mbox.askyesno('Import A File?', 'Would you like to import a file of IPs and ports to check?')
        if answer:
            self.onFileCheckPort()
        else:
            self.onEnterCheckPort()

    def onFileCheckPort(self):
        '''
        file may look like:
        ip
        ip
        ip
        port
        port

        file may also look like:
        port
        port
        port
        port
        ip
        ip

        file could even look like:
        port
        ip
        port
        ip
        ip
        ip
        port

        all will be accepted and accounted for by Traurig
        the only requirement of the file is that each value is on
        its own line

        if the file has an invalid ip or port on one of the lines,
        then Traurig will ignore that line, making note of it so
        that it can display the error on the line with the results.


        Traurig output formatting: (displayed in a window with an option to save as .txt file for use later)

        ***********************************
        RESULTS:
        ***********************************
        <ip address 1 here>:
            <port 1 here> = Open
            <port 2 here> = Not Open
            <port 3 here> = Not Open
            etc....
        <ip address 2 here>:
            <port 1 here> = Not Open
            <port 2 here> = Open
            <port 3 here> = Not Open
        etc...

        ***********************************
        ERRORS:
        ***********************************
        <errored port here> on line <line number from orig. file here> = Inavlid Port
        <errored ip here> on line <line number from orig. file here> = Invalid IP Address
        etc...

        '''

        '''
        First, we should prompt for the user to pick a file
        after that, we should check if each line in the folder is either an ip or a port
        if the line is an ip, add it to the ip list
        if the line is a port, add it to the port list
        if the line is an invalid ip or an invalid port or just plain wrong, add it to error list as a tuple with (linenum, error)
        3 possible errors:
            1) proper ip format but incorrect values (i.e. 444.444.444.441 is not a valid ip)
            2) proper port format but incorrect value (i.e. -123 or 123456789)
            3) improper ip format/port format (i.e. lolimwreckingthecoders was entered, and could not be determined to be a port or an ip)
        '''
        mbox.showinfo('Still Being Implemented', 'This feature is still being implemented and will be a part of Traurig soon!')


    def onEnterCheckPort(self):
        #open a new window and ask for ip and port
        ip_entered = tkSimpleDialog.askstring('Enter IP Address', 'Enter the IP Address you would like to check: ')
        if ip_entered == None:
            #if they enter nothing, cancel and don't open any more windows
            pass
        else:
            #if they enter a value, check if it is an ip, and then
            is_ip = check_if_ip(ip_entered)
            if is_ip:
                #prompt for port to scan on
                port_entered = tkSimpleDialog.askstring('Enter Port To Check', 'Enter the port you would like to check: ')
                if port_entered == None:
                    pass
                else:
                    if check_if_port(port_entered):
                        port_entered = int(port_entered)
                        if is_port_open(ip_entered, port_entered):
                            mbox.showinfo('Port Open', 'Port ' + str(port_entered) + ' is open on ' + ip_entered)
                        else:
                            mbox.showinfo('Port Not Open', 'Port ' + str(port_entered) + ' is not open on ' + ip_entered)
                    else:
                        mbox.showerror('Invalid Port', 'You did not enter a valid port.')

            else:
                #ask to retry the ip entry
                retry = mbox.askretrycancel('Retry?', 'You did not enter a proper ip. Would you like to try again?')
                if retry:
                    self.onEnterCheckPort()
                else:
                    pass



def is_port_open(ip, port): #takes in ip as a string, port as string or int
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if s.connect_ex((ip, int(port))) == 0:
        return True
    else:
        return False


def check_if_ip(ip):
    try:
        socket.inet_aton(ip)
    except socket.error:
        return False
    return True


def check_if_port(entered_port):
    try:
        port = int(entered_port)
        if (port > 0) and (port <= 65535):
            return True
        else:
            return False
    except ValueError:
        return False




def main():
    root = Tk()
    root.title('Traurig')
    t_obj = Traurig(root)
    root.geometry("250x150+300+300")
    root.mainloop()

if __name__ == '__main__':
    main()
