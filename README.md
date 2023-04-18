# Lotus Net Tools                      
                          
A set of network tools coded in Python3 for monitoring of your network. I originally created these tools to monitor changes in devices on my home network. I had it run periodically from a raspberry pi 3B+. It is NOT intended for unauthorized use on public networks. I am not responsible for any use outside of the intended scope of your own personal network. It makes use of the argparse library to allow you to enter arguments.

---

## Net Listener
Given a specific IP, set of IPs, or Network IP as the target, scan for the device on your network. If it is found, it will return the MAC address, IP, and manufactuer (if possible) to print out. This tool uses threading to process larger networks. This is useful for finding missing devices on a network that uses static ip addresses, finding the number of devices on your network, finding the MAC address for a device on your network.

### Arguments

-t, --target: The target IP or list of IPs (seperated by a space)<br>
-a, --all: The subnet mask (in xxx.xxx.xxx.xxx format, e.g. 255.255.255.0) that is used to grab all the devices given the Network IP as the target<br>
-l, --log: Outputs the result as a .txt file log<br>
