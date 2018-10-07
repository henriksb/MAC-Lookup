#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import sys
import re
import os

MAC_URL = "http://standards-oui.ieee.org/oui.txt"
# MAC_URL_WIRESHARK = "https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf"
MAC_ADDRESS_PATH = os.path.dirname(os.path.realpath(__file__)) + "/MAC_ADDRESS.txt" 


def usage():
    print("Usage: MACLookup [MAC ADDRESS]"
          "\n       MACLookup update")
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


# Check if enough arguments are provided
if len(sys.argv) == 1:
    usage()

if sys.argv[1].lower() == "update":
    print("[*] Updating..")
    download()
    print("[+] Finished updating")
    sys.exit(0)

# Validate entered MAC address
if not re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", sys.argv[1].lower()):
    print("[!] Invalid MAC address\n")
    usage()

if not os.path.exists(MAC_ADDRESS_PATH):
    y_n = input("[?] MAC_ADDRESS.txt not found, do you want to download it? [y/n]: ")
    if y_n[0].lower() == "y":
        download()
    else:
        sys.exit(1)

MAC_ADDRESS = open(MAC_ADDRESS_PATH, "r", encoding="utf8").read()

# Change MAC address format if needed
if "-" in sys.argv[1] or ":" in sys.argv[1]:
    mac_address = sys.argv[1].replace(":", "").upper()
    mac_address = mac_address.replace("-", "").upper()
else:
    mac_address = sys.argv[1].upper()

# Compare entered MAC address with addresses in text file
for address in MAC_ADDRESS.split("\n"):
    if address[0:6] == mac_address[0:6]:
        print(address[7:].strip())
        sys.exit(0)

print("[!] MAC address not found")
