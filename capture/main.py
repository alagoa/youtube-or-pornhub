import sys
import argparse
import pyshark
import numpy as np
import matplotlib.pyplot as plt
import utils
from netaddr import IPNetwork, IPAddress, IPSet
import threading
import time
import thread_pcap


class getDataThread (threading.Thread):
   def __init__(self, threadID, name, counter, args):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.args = args
   def run(self):
      time.sleep(1)
      print "\n\n+---------------+"
      print "|Starting " + self.name + str(self.threadID) + " |"
      print "+---------------+"
      #print_time(self.name, self.counter, 5)
      thread_pcap.pcap(self.args)
      print "\n\n+---------------+"
      print "| Exiting " + self.name + str(self.threadID) + " |"
      print "+---------------+"

def main():
	print "+-----------------------+"
	print "|  Starting Main thread |"
	print "+-----------------------+"



	print "Reading arguments..."
	k = 0
	parser=argparse.ArgumentParser()
	parser.add_argument('-i', '--interface', nargs='?',required=True, help='capture interface')
	parser.add_argument('-c', '--cnet', nargs='+',required=True, help='client network(s)')
	parser.add_argument('-s', '--snet', nargs='+',required=True, help='service network(s)')
	parser.add_argument('-t', '--tcpport', nargs='?',help='service TCP port (or range)')
	parser.add_argument('-u', '--udpport', nargs='?',help='service UDP port (or range)')
	args=parser.parse_args()

	print "Launching capture thread..."
	pcap_thread = getDataThread(1, "pcap", 1, args)

	pcap_thread.start()

	print "+----------------------+"
	print "|  Exiting Main thread |"
	print "+----------------------+"

if __name__ == '__main__':
    main()