# youtube-or-pornhub

**YoutubeOrPornhub** is a tool that, by analyzing the traffic of a given network, can detect what service is being used. It can detect if the user is browsing, listening to Spotify (or both), watching a Youtube video... and even differentiate it from a Pornhub video!

The analysis of the traffic is non-intrusive, so this will work even on ciphered traffic.

____________________________________________________________________________________________

## Capturing Packets

Use the **pcap.py** tool to capture packets.
Run it by using
```shel
python pcap.py -i [interface] -c [client-networks] -s [service-networks]
```

You can also specify the TCP/UDP port by using _-t_ or _-u_ respectivelly. For example:
```shell
python pcap.py -i eth0 -c 192.1.1.10/0 -s 0.0.0.0/0
```

With the command above we are capturing packets on the interface eth0. The client network is machine's IP on that interface and the service IP is 0.0.0.0/0, which means we will capture all the packets on the network.

By default, this will capture the received/sent packets in intervals of 1 second. 

To stop the capture, press Ctrl-C.

DISCLAIMER: THIS WILL CHANGE
			
The output will be a file named 'down' with one number per line, representing the number of bytes downloaded on a certain interval. For example, if the interval was 1 second:

```shell
400	# [0-1s]
509	# [1-2s]
23	# [2-3s]
4	# [3-4s]
```
_____________________________________________________________________________________________


