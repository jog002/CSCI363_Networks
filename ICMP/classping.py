"""
A sample program to send ICMP echo requests to a host to demonstrate
how to use the socket module to send and receive ICMP messages.

This requires root privileges to run.

Marchiori, 2023

test sites:

eg.bucknell.edu
bbc.co.uk
asahi-net.jp
google.com
yahoo.com
apple.com

"""

import argparse
import socket
import struct
import time
import random


def icmp_socket(timeout=1, ttl=30):
    "Create a raw socket for ICMP messages"
    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_RAW,
        proto=socket.getprotobyname("icmp"))
    # Set the timeout
    s.settimeout(timeout)
    # Set the TTL
    s.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    return s


def checksum(data):
    "Calculate the checksum for the data"
    sum = 0
    # make 16 bit words out of every two adjacent 8 bit words in the packet
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            sum += (data[i] << 8) + data[i + 1]
        else:
            sum += data[i] << 8
    # take only 16 bits out of the 32 bit sum and add up the carries
    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)

    # one's complement
    return ~sum & 0xffff


def ping(host, skt=None, ttl=30, quiet=False):


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="Host to ping")
    parser.add_argument("-t", "--ttl", help="Time to live", default=30, type=int)
    parser.add_argument('-n', '--num', help="Number of pings", default=3, type=int)
    args = parser.parse_args()

    # if doing multiple pings, you can reuse the same socket
    s = icmp_socket()
    rtts = []
    try:
        # wrap this in a try block so we can close the socket if there is an error
        for i in range(args.num):
            valid, rtt = ping(args.host, skt=s, ttl=args.ttl)
            if valid:
                rtts.append(rtt)

    except KeyboardInterrupt:
        print("^C")
    finally:
        # close the socket when done
        s.close()

    print("---  ping statistics ---")
    print(
        f"{args.num} packets transmitted, {len(rtts)} packets received, {100 * (args.num - len(rtts)) / args.num:3.2f}% packet loss, time {sum(rtts):8.3f}ms")
    if len(rtts) > 0:
        print(f"rtt min/avg/max = {min(rtts):6.3f}/{sum(rtts) / len(rtts):6.3f}/{max(rtts):6.3f} ms")