import scapy.all as scapy
import optparse

#1) arp request
#2) broadcast
#3) response

def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-i","--ipaddress",dest="ip_address",help="Enter IP Address")

    (user_input,arguments) = parse_object.parse_args()
    if not user_input.ip_address:
        print("Enter IP Address")

    return user_input


def scan_my_network(ip):
    #ls help gorevi goren bir methoddur. scapy.ARP() hakklinda bilgi verir
    #scapy.ls(scapy.ARP())
    arp_request_packet = scapy.ARP(pdst=ip)
    #scapy.ls(scapy.Ether()) ile scapy.Ether hakkinda bilgi alabiliriz
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #iki paketi birlestiriyoruz.
    combined_packet = broadcast_packet/arp_request_packet
    #paketleri yollayip cevaplarini almak(verilen verilmeyen) icin srp kullanilir
    #timeout=1 degeri cevap verilmediginde beklemeden devam edilmesini saglar.
    (answered_list,unanswered_list) = scapy.srp(combined_packet,timeout=1)
    #print(list(answered_list))
    answered_list.summary()

user_ip_address = get_user_input()
scan_my_network(user_ip_address.ip_address)
