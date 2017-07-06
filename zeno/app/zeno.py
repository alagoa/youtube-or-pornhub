import sys
import argparse
import pyshark
import numpy as np
import matplotlib.pyplot as plt
from utils import utils
from netaddr import IPNetwork, IPAddress, IPSet
import threading
import time
from app import thread_pcap

class getDataThread (threading.Thread):
   def __init__(self, threadID, name, counter, args):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.args = args
   def run(self):
      time.sleep(1)
      print("\n\n+---------------+")
      print("| Starting " + self.name + str(self.threadID) + " |")
      print("+---------------+")
      #print_time(self.name, self.counter, 5)
      thread_pcap.pcap(self.args)
      print("\n\n+---------------+")
      print("| Exiting " + self.name + str(self.threadID) + " |")
      print("+---------------+")

def start(args):
	print("+-----------------------+")
	print("|  Starting Main thread |")
	print("+-----------------------+")

	print("Launching capture thread...")
	pcap_thread = getDataThread(1, "pcap", 1, args)

	pcap_thread.start()

	print("+----------------------+")
	print("|  Exiting Main thread |")
	print("+----------------------+")

if __name__ == '__main__':
    start()