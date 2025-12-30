#!/usr/bin/env python3
import json
import socket
import datetime
from scapy.all import ARP, Ether, srp

INTERFACE = "enp0s3"
OUTPUT_FILE = "scan.json"


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def arp_scan(subnet):
    devices = []

    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    answered = srp(packet, iface=INTERFACE, timeout=2, verbose=False)[0]

    for _, rcv in answered:
        devices.append({
            "ip": rcv.psrc,
            "mac": rcv.hwsrc
        })

    return devices


def main():
    local_ip = get_local_ip()
    subnet = ".".join(local_ip.split(".")[:-1]) + ".0/24"

    devices = arp_scan(subnet)

    output = {
        "timestamp": str(datetime.datetime.now()),
        "local_ip": local_ip,
        "devices": devices
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
