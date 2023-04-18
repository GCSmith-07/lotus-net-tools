import queue
from datetime import datetime

import net_listener
import argparse
import signal


# Function to print the menu
def print_menu():
    flower = '''                           @@@@                   #@@@@                         
                         &@@@, @@     @@@@@@     @. %@@@                        
            @@%         @@@        @@@@@@@@@@@@       @@@(          &@          
            @@  ,@@,   @@@       @@@@@     %@@@@@      ,@@     @@%(@@@          
            @@@        @@      @@@@@         .@@@@@     @@@        @@@          
        *@   @@.       @@     @@@@             @@@@@    @@%       @@@   @/      
        @@@@  @@@      @@    (@@@               @@@@    @@       @@.  @@@       
         @@@@@  /@@     ,@    @@(                @@@   @@      @@   @@@@@       
      @@    %@@@@(  @@(   @@  @@@               @@@  @@   .@@  ,@@@@@@   @@@    
      @@@@@@@@@@@@@@%.       @ ,@               @& @.      .(@@@@@@@@@@@@@@.    
       @@@  /@@@@@@@@@@@@@@@@@   @             @   (@@@@@@@@@@@@@@@@&  @@@%     
        @@@@               .@@@@@  @         @ .@@@@@#.              @@@@       
   &@*    @@@@                    /%         @                     @@@@     @@  
 .@@@.       @@@@                          @                    @@@@,       @@@ 
     @@@@@         (@@@@/      /@@     @ @    &@@@      %@@@@@(.      .@@@@@@.  
                     @@@@@@@@        @@  %@@       @@@@@@@@@                    
                      &@@@@@@@%/@@@@@      @@@@@@@@@@@@@@@                      
                          .@@@@@&             ,@@@@@@@                         '''

    print("---------------------------------------------------------------------------------\n" + flower + "\n\n\n"
          + "\t\tLOTUS NET TOOLS V1.0\tBy: Graeson Smith" +
          "\n\n\n----------------------------------------------------------------------------------\n")


# 'main' function that runs on start
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='tool', help='The tool to use')

    # Listener Parser Arguments
    listener_parser = subparsers.add_parser('listener', help='A network listener tool')
    listener_parser.add_argument('-t', '--target', metavar='IP', nargs='+', type=str, dest='target',
                                 help='Target IP address/addresses')
    listener_parser.add_argument('-a', '--all', dest='mask',
                                 help='Scan all devices within the ip range given a subnet mask')
    listener_parser.add_argument('-l', '--log', type=str, dest='log',
                                 const=f"log_{datetime.now().strftime('%Y_%m_%d_[%H.%M]')}.txt", nargs='?',
                                 help='Exports the output log to a file')

    # Sniffer Parser Arguments
    # sniff_parser = subparsers.add_parser('sniff', help='Sniffs packets')
    # sniff_parser.add_argument('-t', '--target', nargs='+', type=str, dest='target', help='Target MAC address/addresses')
    # sniff_parser.add_argument('-f', '--filter', nargs='+', type=str, dest='filter', help='Filter arguments')
    # sniff_parser.add_argument('-inf', '--interface', nargs='+', type=str, dest='interface', help='Interface to sniff')
    # sniff_parser.add_argument('-c', '--count', type=int, dest='count', const=10,
    #                           help='Limit for the number of packets to sniff. Default is 10')
    # sniff_parser.add_argument('-pcap', type=str, dest='pcap', help='The pcap file to store the captures in')
    # sniff_parser.add_argument('-s', '--summary', nargs='?', dest='summary', help='Option to include summary')

    # Exit Parser Arguments
    exit_parser = subparsers.add_parser('exit', help='Exit the program')

    print_menu()

    while True:
        try:
            print("\n")
            u_in = input(">>> ")
            args = parser.parse_args(u_in.split())

            if args.tool == 'listener':
                net_listener.run(args)

            if args.tool == 'exit':
                break

        except SystemExit:
            continue
