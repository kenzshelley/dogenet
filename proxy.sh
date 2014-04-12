#!/bin/sh
PROXY_IP=192.168.1.137
##PROXY_IP=10.0.0.137
PROXY_PORT=3000
LAN_IP=`nvram get lan_ipaddr`
LAN_NET=$LAN_IP/`nvram get lan_netmask`

iptables -t nat -A PREROUTING -i br0 -s $LAN_NET -d $LAN_NET -p tcp --dport 80 -j ACCEPT
iptables -t nat -A PREROUTING -i br0 -s ! $PROXY_IP -p tcp --dport 80 -j DNAT --to $PROXY_IP:$PROXY_PORT
iptables -t nat -I POSTROUTING -o br0 -s $LAN_NET -d $PROXY_IP -p tcp -j SNAT --to $LAN_IP
iptables -I FORWARD -i br0 -o br0 -s $LAN_NET -d $PROXY_IP -p tcp --dport $PROXY_PORT -j ACCEPT

iptables -t nat -I PREROUTING -i br0 -s 192.168.1.137 -j ACCEPT