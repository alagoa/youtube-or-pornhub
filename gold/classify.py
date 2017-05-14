import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import time
import sys
import warnings
import scalogram

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
	
	test=np.loadtxt('../data/for_testing/spotify_test1')				# capture to test (can be more than one)
	
	N=len(youtubedown)
	dj=1/64
	s0=2
	J=1/dj * np.log2(0.5*N/s0)
	scales=s0*2**(np.arange(J)*dj)

	########### Profiling YouTube caps ###########
	print("Profiling YouTube caps...")

	allS=np.zeros((10,len(scales)))
	for i in range(10):
		S,scales=scalogram.scalogramCWT(youtubedown[:,i],scales)
		allS[i,:]=S
		#plt.plot(scales,S,'b')
		#plt.show()
		#idx=argrelextrema(S, np.greater)[0]
		#threshold=.5*max(S)
		#idxM=[j for j in idx if S[j]>threshold]
		#print(scales[idxM])
		#waitforEnter()
	
	averageS1=np.mean(allS,axis=0)
	plt.plot(scales,averageS1,'r',lw=3)
	plt.show()
	waitforEnter()

	########### Profiling regular browsing caps ###########
	print("Profiling regular browsing caps...")

	allS=np.zeros((10,len(scales)))
	for i in range(10):
		S,scales=scalogram.scalogramCWT(browsingdown[:,i],scales)
		allS[i,:]=S
		#plt.plot(scales,S,'r')
		#plt.show()
		#idx=argrelextrema(S, np.greater)[0]
		#threshold=.5*max(S)
		#idxM=[j for j in idx if S[j]>threshold]
		#print(scales[idxM])
		#waitforEnter()
	
	averageS2=np.mean(allS,axis=0)
	plt.plot(scales,averageS2,'b',lw=3)
	plt.show()
	waitforEnter()

	########### Profiling Spotify caps ###########
	print("Profiling Spotify caps...")

	allS=np.zeros((10,len(scales)))
	for i in range(10):
		S,scales=scalogram.scalogramCWT(spotifydown[:,i],scales)
		allS[i,:]=S
		#plt.plot(scales,S,'r')
		#plt.show()
		#idx=argrelextrema(S, np.greater)[0]
		#threshold=.5*max(S)
		#idxM=[j for j in idx if S[j]>threshold]
		#print(scales[idxM])
		#waitforEnter()
	
	averageS3=np.mean(allS,axis=0)
	plt.plot(scales,averageS3,'g',lw=3)
	plt.show()
	waitforEnter()

	########### Profiling PornHub caps ###########
	print("Profiling Spotify caps...")

	allS=np.zeros((10,len(scales)))
	for i in range(10):
		S,scales=scalogram.scalogramCWT(pornhubdown[:,i],scales)
		allS[i,:]=S
		#plt.plot(scales,S,'r')
		#plt.show()
		#idx=argrelextrema(S, np.greater)[0]
		#threshold=.5*max(S)
		#idxM=[j for j in idx if S[j]>threshold]
		#print(scales[idxM])
		#waitforEnter()
	
	averageS4=np.mean(allS,axis=0)
	plt.plot(scales,averageS4,'y',lw=3)
	plt.show()
	waitforEnter()

	
	########### Performing the test ###########
	print("Performing the test...")

#	for i in range(1,20):
	S,scales=scalogram.scalogramCWT(test[:],scales)
	plt.plot(scales,S,'g')
	plt.show()
	waitforEnter()

	d = {"YouTube"  : curveDistance(averageS1,S),
		 "Browsing" : curveDistance(averageS2,S),
		 "Spotify"  : curveDistance(averageS3,S),
		 "PornHub"	: curveDistance(averageS4,S)}

	print(min(d, key=d.get))
		
	waitforEnter()
#	plt.plot(scales,S,'b')
#	plt.show()

if __name__ == "__main__":
	main()
