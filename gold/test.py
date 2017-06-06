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
	dj=1/16
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


def predict(test):

	with open("yt_scalo", 'rb') as f:
		scalogramAvgYoutube = pickle.load(f)
	with open("br_scalo", 'rb') as f:
		scalogramAvgBrowsing = pickle.load(f)
	with open("ph_scalo", 'rb') as f:
		scalogramAvgPornhub = pickle.load(f)
	with open("sp_scalo", 'rb') as f:
		scalogramAvgSpotify = pickle.load(f)

	########### Performing the test ###########
	print("Performing the test...")

	N=300
	dj=1/16
	s0=2
	J=1/dj * np.log2(0.5*N/s0)
	scales=s0*2**(np.arange(J)*dj)

	S,scales=scalogram.scalogramCWT(test,scales)

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

def main():
	test=np.loadtxt('../data/for_testing/spotify/spotify_test1')				# capture to test (can be more than one)
	predict(test)

if __name__ == "__main__":
	main()
