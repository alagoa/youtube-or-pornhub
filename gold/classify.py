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
	plt.ion()
	
	youtubedown=np.loadtxt('../data/youtubedown')
	browsingdown=np.loadtxt('../data/browsingdown')
	
	test=np.loadtxt('../data/for_testing/youtube_test1')
	
	N=len(youtubedown)
	dj=1/64
	s0=2
	J=1/dj * np.log2(0.5*N/s0)
	scales=s0*2**(np.arange(J)*dj)
	#scales=np.arange(1,50)
	plt.figure(2)
	plt.clf()
	allS=np.zeros((10,len(scales)))
	for i in range(10):
		S,scales=scalogram.scalogramCWT(youtubedown[:,i],scales)
		allS[i,:]=S
		plt.plot(scales,S,'b')
		plt.show()
		idx=argrelextrema(S, np.greater)[0]
		threshold=.5*max(S)
		idxM=[j for j in idx if S[j]>threshold]
		print(scales[idxM])
		waitforEnter()
	
	averageS1=np.mean(allS,axis=0)
	plt.plot(scales,averageS1,'b',lw=3)
	plt.show()

	allS=np.zeros((10,len(scales)))
	for i in range(10):
		S,scales=scalogram.scalogramCWT(browsingdown[:,i],scales)
		allS[i,:]=S
		plt.plot(scales,S,'r')
		plt.show()
		idx=argrelextrema(S, np.greater)[0]
		threshold=.5*max(S)
		idxM=[j for j in idx if S[j]>threshold]
		print(scales[idxM])
		waitforEnter()
	
	averageS2=np.mean(allS,axis=0)
	plt.plot(scales,averageS2,'r',lw=3)
	plt.show()

#	for i in range(1,20):
	S,scales=scalogram.scalogramCWT(test[:],scales)
	plt.plot(scales,S,'g')
	plt.show()
	if curveDistance(averageS1,S) < curveDistance(averageS2,S):
		print(i, 'Youtube')
	else:
		print(i, 'Browsing')
	waitforEnter()
#	plt.plot(scales,S,'b')
#	plt.show()

if __name__ == "__main__":
	main()
