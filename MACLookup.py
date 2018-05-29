#!/usr/bin/python3
from MAC_INFO import MAC_ADDRESS
import sys
import re


def usage():
    print("Usage: MACLookup [MAC ADDRESS]")
    print("\nAccepted formats:"
          "\n\t- MACLookup FC:FB:FB:01:FA:21"
          "\n\t- MACLookup FC-FB-FB-01-FA-21"
          "\n\t- MACLookup FCFBFB01FA21")
    sys.exit(1)


# Check if enough arguments are provided
if len(sys.argv) == 1:
    usage()

# Validate entered MAC address
if not re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", sys.argv[1].lower()):
    print("[!] Invalid MAC address\n")
    usage()

# Change MAC address format if needed
if "-" in sys.argv[1] or ":" in sys.argv[1]:
    mac_address = sys.argv[1].replace(":", "")
    mac_address = mac_address.replace("-", "").upper()
else:
    mac_address = sys.argv[1].upper()

# Compare entered MAC address with addresses in "MAC_INFO"
for address in MAC_ADDRESS:
    if address[0:6] == mac_address[0:6]:
        print(address[7:])
        sys.exit(0)

print("[!] MAC address not found")
