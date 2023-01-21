import scapy.all as scapy
from scapy_http import http

def listen_packets(interface):
    scapy.sniff(iface="eth0", store=False, prn=analyze_packets)
    #prn = callback function paketler geldikce hangi fonsiyonuna yollayacaginizi belirlersiniz

def analyze_packets(packet):
    #packet.show()
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            print(packet[scapy.Raw].load)

listen_packets("eth0")