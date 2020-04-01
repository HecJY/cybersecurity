#!/bin/sh

#set the macros
block_ip_1="121.121.121.121"
block_ip_2="101.101.101.101"
local_ip=$(hostname -I | sed 's/ //g')


#
# Remove any previous rules or chains, pg
iptables -t filter -F
iptables -t filter -X
iptables -t nat -F
iptables -t nat -X

# For all outgoing packets, change their source IP address to your own machine’s IP address (Hint: Refer to the MASQUERADE target in the nat table). pg  65
iptables -t nat -A POSTROUTING -j MASQUERADE



# Block a list of specific IP addresses (of your choosing) for all incoming connections.
iptables -A INPUT -s $block_ip_1 -j REJECT
iptables -A INPUT -s $block_ip_2 -j REJECT

echo block the following ip addresses $block_ip_1 $block_ip_2

# Block your computer from being pinged by all other hosts (Hint: ping uses ICMP Echo requests).
iptables -A INPUT -p icmp --icmp-type echo-request -j DROP
echo block from pinged

# pg 54
# Set up port-forwarding from an unused port of your choice to port 22 on your computer. Test if you can SSH into your machine using both ports (Hint: You need to enable connections on the unused port as well).
iptables -t nat -A PREROUTING -p tcp -d $local_ip --dport 80 -j DNAT --to-destination $local_ip:22
echo set port 22

# Allow for SSH access (port 22) to your machine from only the engineering.purdue.edu domain.
iptables -A INPUT -p tcp -s 128.46.0.0 --dport 22 -j ACCEPT
iptables -A INPUT -p tcp -s 0.0.0.0/0 --dport 22 -j DROP


# Assuming you are running an HTTPD server on your machine that can make available your entire home directory to the outside world, write a rule that allows only a single IP address in the internet to access your machine for the HTTP service.
iptables -A INPUT -p tcp -s 111.111.111.111 --dport 111 -j ACCEPT
iptables -A INPUT -p tcp -s 0.0.0.0/0 --dport 111 -j DROP

# Permit Auth/Ident (port 113) that is used by some services like SMTP and IRC.
iptables -A INPUT -p tcp --dport 113 -j ACCEPT