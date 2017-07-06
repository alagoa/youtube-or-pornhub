import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import time
import sys
import warnings
import scalogram
import pickle

def calcScalogram(data):

	N=300
	dj=1/128
	s0=2
	J=1/dj * np.log2(0.5*N/s0)
	scales=s0*2**(np.arange(J)*dj)

	allS=np.zeros((10,len(scales)))
	for i in range(10):
		S,scales=scalogram.scalogramCWT(data[:,i],scales)
		allS[i,:]=S
	
	average=np.mean(allS,axis=0)
	return average,scales

def waitforEnter():
	if sys.version_info[0] == 2:
		raw_input("Press ENTER to continue.")
	else:
		input("Press ENTER to continue.")

def curveDistance(c1, c2):
	return np.mean((c2-c1)**2)


def main():
	########### Loading files and configuring ###########
	plt.ion()
	youtubedown=np.loadtxt('../data/youtubedown')
	browsingdown=np.loadtxt('../data/browsingdown')
	spotifydown=np.loadtxt('../data/spotifydown')
	pornhubdown=np.loadtxt('../data/pornhubdown')

	test=np.loadtxt(sys.argv[1])				# capture to test (can be more than one)

	########### Profiling YouTube caps ###########
	print("Profiling YouTube caps...")
	scalogramAvgYoutube,scales = calcScalogram(youtubedown)
	plt.plot(scales,scalogramAvgYoutube,'r',lw=3) 
	plt.show()
	waitforEnter()

	########### Profiling regular browsing caps ###########
	print("Profiling regular browsing caps...")
	scalogramAvgBrowsing, scales = calcScalogram(browsingdown)
	plt.plot(scales,scalogramAvgBrowsing,'b',lw=3)
	plt.show()
	waitforEnter()

	########### Profiling Spotify caps ###########
	print("Profiling Spotify caps...")
	scalogramAvgSpotify,scales = calcScalogram(spotifydown)
	plt.plot(scales,scalogramAvgSpotify,'g',lw=3)
	plt.show()
	waitforEnter()

	########### Profiling PornHub caps ###########
	print("Profiling PornHub caps...")
	scalogramAvgPornhub, scales = calcScalogram(pornhubdown)
	plt.plot(scales,scalogramAvgPornhub,'y',lw=3)
	plt.show()
	waitforEnter()


	print(scalogramAvgYoutube)
	with open('scalo_data/yt_scalo', 'wb') as f:
		pickle.dump(scalogramAvgYoutube, f)
	with open('scalo_data/br_scalo', 'wb') as f:
		pickle.dump(scalogramAvgBrowsing, f)
	with open('scalo_data/ph_scalo', 'wb') as f:
		pickle.dump(scalogramAvgPornhub, f)
	with open('scalo_data/sp_scalo', 'wb') as f:
		pickle.dump(scalogramAvgSpotify, f)

	########### Performing the test ###########
	print("Performing the test...")

	N=300
	dj=1/128
	s0=2
	J=1/dj * np.log2(0.5*N/s0)
	scales=s0*2**(np.arange(J)*dj)

	#for i in range(1,20):
	S,scales=scalogram.scalogramCWT(test,scales)
	plt.plot(scales,S,'m')
	plt.show()
	waitforEnter()

	print('\nCurve Distances:')

	print("Youtube -> " + str(curveDistance(scalogramAvgYoutube, S)))
	print("Browsing -> " + str(curveDistance(scalogramAvgBrowsing, S)))
	print("Spotify -> " + str(curveDistance(scalogramAvgSpotify, S)))
	print("PornHub -> " + str(curveDistance(scalogramAvgPornhub, S)))

	d = {"YouTube"  : curveDistance(scalogramAvgYoutube,S),
		 "Browsing" : curveDistance(scalogramAvgBrowsing,S),
		 "Spotify"  : curveDistance(scalogramAvgSpotify,S),
		 "PornHub"	: curveDistance(scalogramAvgPornhub,S)}

	print("This is a " + str(min(d, key=d.get)) + " capture.")
		
	waitforEnter()

if __name__ == "__main__":
	main()
