import sys
import argparse
import pyshark
import numpy as np
import matplotlib.pyplot as plt
import utils
import threading
import time
from netaddr import IPNetwork, IPAddress, IPSet


class processDataThread(threading.Thread):
	def __init__(self, threadID, name, counter):
	  threading.Thread.__init__(self)
	  self.threadID = threadID
	  self.name = name
	  self.counter = counter
	def run(self):
      print "Starting " + self.name
      save()
      print "Exiting " + self.name

npkts=0
npkts_up=0
npkts_down=0
len_up=0
len_down=0
t0=0
t=0
dic ={}
inter_interval_down=[]
inter_interval_up=[]


def pkt_callback(pkt):
	global scnets
	global ssnets
	global npkts
	global npkts_up
	global npkts_down
	global len_up
	global len_down
	global t
	global t0
	global dic 
	global lastupload
	global lastdownload
	global inter_interval_down
	global inter_interval_up
	global start

	i = (utils.current_time() - start)
	if(i > 30*1000):
		processData_thread = processDataThread(i, "process_data", i)
		
	if IPAddress(pkt.ip.src) in scnets|ssnets and IPAddress(pkt.ip.dst) in scnets|ssnets:
		t = float(pkt.sniff_timestamp)
		delta = 1
		global k
		k= int((t- t0)/delta)		
		
		stat_line =[0,0,0,0]
		
		if npkts == 0:
			t0=t
			lastupload = pkt 
			lastdownload = pkt 
			
		if IPAddress(pkt.ip.src) in scnets and IPAddress(pkt.ip.dst): #upload 
			if lastupload != None: 
				inter_interval_up.append(t- float(lastupload.sniff_timestamp))
			if k in dic:
				stat_line = dic[k]
				stat_line[0]= stat_line[0]+ int(pkt.ip.len)
				stat_line[1]=stat_line[1]+1
			else:
				stat_line = [int(pkt.ip.len),1,0,0]
			dic.update({k:stat_line})	
			lastupload = pkt
			
		if IPAddress(pkt.ip.src) in ssnets: #download 
			if lastupload != None: 
				inter_interval_down.append(t- float(lastdownload.sniff_timestamp))
			if dic.has_key(k):
				stat_line = dic[k]
				stat_line[2]=stat_line[3]+int(pkt.ip.len)
				stat_line[3]=stat_line[3]+1
			else:
				stat_line = [0,0,int(pkt.ip.len),1]
			dic.update({k:stat_line})	
			lastdownload = pkt
				
		npkts=npkts+1
		#print (str(dic)) 
		
		#if pkt.ip.proto=='17':
			#print('%s: IP packet from %s to %s (UDP:%s) %s'%(pkt.sniff_timestamp,pkt.ip.src,pkt.ip.dst,pkt.udp.dstport,pkt.ip.len))
		#elif pkt.ip.proto=='6':
			#print('%s: IP packet from %s to %s (TCP:%s) %s'%(pkt.sniff_timestamp,pkt.ip.src,pkt.ip.dst,pkt.tcp.dstport,pkt.ip.len))
		#else:
			#print('%s: IP packet from %s to %s (other) %s'%(pkt.sniff_timestamp, pkt.ip.src,pkt.ip.dst,pkt.ip.len))

def save():
	global npkts
	global npkts_up
	global npkts_down
	global len_up
	global len_down
	global t0
	keys = []
	values = []
	
	file_ = open('stats', 'w')
	#file_.write('npkts:'+str(npkts)+'\n')
	#file_.write('npkts_down:'+ str(npkts_down)+'\n') 
	#file_.write('npkts_up:'+ str(npkts_up)+'\n')
	file_.write(str(dic))
	file_.close()

	file_ = open('down', 'w')
	for key,value in dic.items(): 
		keys.append(key)
		values.append(value) 
	 
	for key in keys:
		file_.write(str(dic.get(key)[1]) + "\n")

	v = list(zip(*values)) 	
	plt.plot(v[0], marker='o', color='r', ls='')
	plt.show()
	
	print('\n%d packets captured! Done!\n'%npkts)


def pcap(args):

	cnets=[]
	for n in args.cnet:
		try:
			nn=IPNetwork(n)
			cnets.append(nn)
		except:
			print('%s is not a network prefix'%n)
	print(cnets)
	if len(cnets)==0:
		print("No valid client network prefixes.")
		sys.exit()
	global scnets
	scnets=IPSet(cnets)

	snets=[]
	for n in args.snet:
		try:
			print n
			nn=IPNetwork(n)
			snets.append(nn)
		except:
			print('%s is not a network prefix'%n)
	print(snets)
	if len(snets)==0:
		print("No valid service network prefixes.")
		sys.exit()
		
	global ssnets
	ssnets=IPSet(snets)
		
	if args.udpport is not None:
		cfilter='udp portrange '+args.udpport
	elif args.tcpport is not None:
		cfilter='tcp portrange '+args.tcpport
	else:
		cfilter='ip'
	
	cint=args.interface
	global start
	start = utils.current_time()
	print('Filter: %s on %s'%(cfilter,cint))
	try:
		capture = pyshark.LiveCapture(interface=cint,bpf_filter=cfilter)
		capture.apply_on_packets(pkt_callback)
		print(inter_interval_down)
		print(inter_interval_up)
	except KeyboardInterrupt:
		save()

if __name__ == '__main__':
    main()