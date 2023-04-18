# This script scans the network for the given IP address or set of addresses. If the IP is present, it will return the
# MAC address for the device. This program utilizes argparse to pass arguments from the terminal into the script and
# scapy for all network functions. The program uses ARP to find the device with the given IP.
from os import system
import scapy.all as s
import requests
import ipaddress
import threading
import time


# Gets device manufacturer based on the API for MAC vendors
def get_manufacturer(mac_address):
    api_url = f"https://api.macvendors.com/{mac_address}"

    # Request a response from the API url
    response = requests.get(api_url)

    # The status code for found is 200. If found, return response text, otherwise put manufacturer = "Unknown"
    if response.status_code == 200:
        return response.text.strip()
    else:
        return "Unknown"


# Print a progress bar for visual representation of the scan process
def print_progress_bar(progress, total, bar_length=50):
    percent = progress / total
    filled_len = int(bar_length * percent)
    bar = "#" * filled_len + "-" * (bar_length - filled_len)
    print(f"\r[{bar}] {progress}/{total}", end='')


# The scan(ip_list, v) function scans for an IP and returns the MAC address
# 'ip_list' is the IP address or list of addresses to scan for
# 'v' is the option for verbose (true or false) when sending/receiving packets
# Uses threading
def scan(ip_list):
    devices = []  # The list of devices to return after all IPs are scanned
    threads = []  # The list of threads

    progress = 0

    def worker(ip):
        nonlocal progress
        arp_req_frame = s.ARP(pdst=ip)
        broadcast_ether_frame = s.Ether(dst="ff:ff:ff:ff:ff:ff")
        ether_arp_req_frame = broadcast_ether_frame / arp_req_frame

        answered_list = s.srp(ether_arp_req_frame, timeout=3, verbose=0)[0]

        for i in range(0, len(answered_list)):
            cli_dict = {"ip": answered_list[i][1].psrc, "mac": answered_list[i][1].hwsrc,
                        "manufacturer": get_manufacturer(answered_list[i][1].hwsrc), "answered": "True"}
            devices.append(cli_dict)

        # unanswered_list = s.srp(ether_arp_req_frame, timeout=3, verbose=v)[1]
        # for i in range(0, len(unanswered_list)):
        # print("Unanswered Device: " + unanswered_list[i][1].psrc + "\n")

        progress += 1
        print_progress_bar(progress, len(ip_list))

    # Divide ip_list into chunks for threading
    chunk_size = (len(ip_list) // 8) + 1
    chunks = [ip_list[i:i + chunk_size] for i in range(0, len(ip_list), chunk_size)]

    for chunk in chunks:
        t = threading.Thread(target=lambda: [worker(ip) for ip in chunk])
        threads.append(t)
        t.start()

    print(str(chunk_size) + " threads started\n")

    print_progress_bar(progress, len(ip_list))

    for t in threads:
        t.join()
    print("\n\nThreads Finished...\n")

    return devices


# If the 'mask' option is present, then generate a list of all IPs in a network to scan
def scan_all(ip_list, mask):
    all_ip_list = []

    for ip in ip_list:
        ip_network = ipaddress.ip_network(f"{ip}/{mask}", strict=False)

        for network_ip_address in ip_network:
            all_ip_list.append(str(network_ip_address))

    return scan(all_ip_list)


# Prints the results as a table with the IP addresses on the left and their MAC addresses on the right
# 'result' is the result of the scn() function to print out
def display_result(result):
    print(
        "----------------------------------------------------------------\n" +
        "{:<16}\t{:<17}\t{}".format("IP Address", "MAC Address", "Manufacturer") +
        "\n----------------------------------------------------------------")

    for i in result:
        print("{:<16}\t{:<17}\t{}".format(i["ip"], i["mac"], i["manufacturer"]))


# Takes the output and writes it to a given file
# 'result' is the result of the scn() function to output to the file
# 'filename' is the filename to write to
def log(result, filename):
    with open(filename, 'w') as log_file:
        log_file.writelines(
            "----------------------------------------------------------------\n" +
            "{:<16}\t\t{:<17}\t\t{}".format("IP Address", "MAC Address", "Manufacturer") +
            "\n----------------------------------------------------------------\n\n")

        for i in result:
            log_file.write("{:<16}\t\t{:<17}\t\t{}".format(i["ip"], i["mac"], i["manufacturer"]) + "\n")

        log_file.close()


# Runs the program with the given arguments when called
# 'args' are the arguments to pass in
def run(args):

    # Clear screen and print the network scanner header
    system('cls')
    print(
        "----------------------------------------------------------------\nNETWORK SCANNER" +
        "\n----------------------------------------------------------------\n")

    # Turn arguments into easily readable text
    if args.mask:
        mask_str = args.mask
    else:
        mask_str = "NONE"

    if args.log:
        log_str = "Logging Enabled"
    else:
        log_str = "Logging Disabled"

    # Print selected arguments with their options
    print("OPTIONS{IPs: [" + f"{', '.join(args.target)}" + "]" +
          "\tSUBNET MASK: " + mask_str +
          "\tLOGGING: " + log_str + "}\n")

    # If a mask is present, scan all devices in the network given the mask. Otherwise, scan each separately
    if args.mask:
        scn_out = scan_all(args.target, args.mask)
    else:
        scn_out = scan(args.target)

    # Sort the final list of devices
    scn_out = sorted(scn_out, key=lambda x: x["ip"])

    # Display the results
    display_result(scn_out)

    # If logging is enabled, make the log
    if args.log:
        log(scn_out, str(args.log))
