#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import platform
import sys
import re
import os

MAC_URL = "http://standards-oui.ieee.org/oui.txt"


def usage():
    print("Usage: MACLookup [MAC ADDRESS]")
    print("\nAccepted formats:"
          "\n\t- MACLookup FC:FB:FB:01:FA:21"
          "\n\t- MACLookup FC-FB-FB-01-FA-21"
          "\n\t- MACLookup FCFBFB01FA21")
    sys.exit(1)


def download():
    # Remove old list
    if os.path.exists(MAC_ADDRESS_PATH):
        os.remove(MAC_ADDRESS_PATH)

    addresses = requests.get(url=MAC_URL)
    soup = BeautifulSoup(addresses.text, "lxml").text

    with open(MAC_ADDRESS_PATH, "a", encoding="utf8") as MAC_ADDRESS:
        for line in soup.split("\n"):
            if "(base 16)" in line:
                MAC_ADDRESS.write(line.replace("(base 16)", ""))
                
                
if platform.system() == "Windows":
    MAC_ADDRESS_PATH = os.path.dirname(os.path.realpath(__file__)) + "\MAC_ADDRESS.txt" 
else:
    MAC_ADDRESS_PATH = os.path.dirname(os.path.realpath(__file__)) + "/MAC_ADDRESS.txt" 
    
# Check if we have the MAC address list, if not, ask if user wants to download it
if not os.path.exists(MAC_ADDRESS_PATH):
    y_n = input("[?] MAC_ADDRESS.txt not found, do you want to download it? [y/n]: ")
    if y_n[0].lower() == "y":
        download()
    else:
        sys.exit(1)

# Check if enough arguments are provided, else, verify input
if len(sys.argv) == 1:
    usage()
else:
    # Make format equal to our datas format so that we can process it properly
    mac_address = sys.argv[1].replace(":", "").replace("-", "").upper()
    
    # Verify MAC address
    if not re.match("^([0-9A-Fa-f]{12})$", mac_address):
        print("[!] Invalid MAC address\n")
        usage()

with open(MAC_ADDRESS_PATH, "r", encoding="utf8") as m:
    # Compare entered MAC address with addresses in text file
    MAC_ADDRESS = m.read()
    for address in MAC_ADDRESS.split("\n"):
        if address[0:6] == mac_address[0:6]:
            print(address[7:].strip())
            break
    else:
        print("[!] MAC address not found")
