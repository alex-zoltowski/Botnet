from Tkinter import *
import tkMessageBox as mbox
import tkFileDialog
import tkSimpleDialog
import socket
import datetime

class Traurig(Frame):

    #self.currentips = []

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.Traurig_Setup()

    def Traurig_Setup(self):

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
        #mbox.showinfo('Still Being Implemented', 'This feature is still being implemented and will be a part of Traurig soon!')
        userfile = tkFileDialog.askopenfilename()
        if userfile != None:
            chosen_file = open(userfile, 'r')
            iplist = []
            portlist = []
            errorlist = []
            current_value = 1
            open_value = ''
            results = ['RESULTS:']


            for line in chosen_file.readlines():
                if line.endswith('\n'):
                    true_line = line[:-1]
                if check_if_ip(true_line):
                    iplist.append(true_line)
                elif check_if_port(true_line):
                    portlist.append(true_line)
                else:
                    errorlist.append((true_line, current_value))
                current_value += 1

            for ipval in iplist:
                results.append(("\n{0}".format(ipval.strip('\n'))))
                for portval in portlist:
                    if is_port_open(ipval, portval):
                        open_value = 'open'
                    elif is_port_open(ipval, portval) == False:
                        open_value = 'not open'
                    results.append('\nPort ' + str(portval).strip('\n') + ' ' + open_value)
            results.append('\nERRORS:')

            for error in errorlist:
                thing_to_append = ('Line ' + str(error[1]).strip('\n') + ': \'' + str(error[0]).strip('\n') + '\' is not a valid IP or Port')
                results.append('\n' + thing_to_append)

            results_string = ''
            for x in results:
                results_string += x

            #mbox.showinfo('Results', results_string)
            current_time = datetime.datetime.now().time()
            filename = 'results_from_' + str(current_time) + '.txt'
            results_file = open(filename, 'w')
            results_file.write(results_string)
            mbox.showinfo('Results Saved', filename + ' has been created in the same directory as Taurig.')


    def onEnterCheckPort(self):
        #open a new window and ask for ip and port
        ip_entered = tkSimpleDialog.askstring('Enter IP Address', 'Enter the IP Address you would like to check: ')
        if ip_entered == None:
            #if they enter nothing, cancel and don't open any more windows
            pass
        else:
            #if they enter a value, check if it is an ip, and then
            if check_if_ip(ip_entered):
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
    result = s.connect_ex((ip, int(port)))
    if result == 0:
        return True
    else:
        return False

def check_if_ip(ip):
    split_ip = ip.split('.')
    if len(split_ip) == 4:
        try:
            socket.inet_aton(ip)
        except socket.error:
            return False
        return True
    else:
        return False


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
