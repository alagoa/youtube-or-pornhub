import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import warnings
import scalogram
import scipy.stats as stats
import scipy.signal as signal
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def calcScalogram(data):
	N=300
	dj=1/64
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
	
	test=np.loadtxt('../data/for_testing/youtube/youtube-test3')				# capture to test (can be more than one)

	########### normalizing data ######################
	youtubedown = youtubedown / youtubedown.max(axis=0)
	browsingdown = browsingdown / browsingdown.max(axis=0)
	spotifydown = spotifydown / spotifydown.max(axis=0)
	pornhubdown = pornhubdown / pornhubdown.max(axis=0)

	########### Profiling YouTube caps ###########
	print("Profiling YouTube caps...")
	scalogramAvgYoutube,scales = calcScalogram(youtubedown)
	M1=np.mean(youtubedown,axis=0)
	Md1=np.median(youtubedown,axis=0)
	V1=np.var(youtubedown,axis=0)
	S1=stats.skew(youtubedown)
	K1=stats.kurtosis(youtubedown)
	#p=[25,50,75,90,95]
	#Pr1=np.array(np.percentile(youtubedown,p,axis=0)).T

	np.array([M1,Md1,V1,S1,K1])
	
	########### Profiling regular browsing caps ###########
	print("Profiling regular browsing caps...")
	scalogramAvgBrowsing, scales = calcScalogram(browsingdown)

	M2=np.mean(browsingdown,axis=0)
	Md2=np.median(browsingdown,axis=0)
	V2=np.var(browsingdown,axis=0)
	S2=stats.skew(browsingdown)
	K2=stats.kurtosis(browsingdown)
	#p=[25,50,75,90,95]
	#Pr2=np.array(np.percentile(browsingdown,p,axis=0)).T
	
	########### Profiling Spotify caps ###########
	print("Profiling Spotify caps...")
	scalogramAvgSpotify,scales = calcScalogram(spotifydown)
	M3=np.mean(spotifydown,axis=0)
	Md3=np.median(spotifydown,axis=0)
	V3=np.var(spotifydown,axis=0)
	S3=stats.skew(spotifydown)
	K3=stats.kurtosis(spotifydown)
	#p=[25,50,75,90,95]
	#Pr3=np.array(np.percentile(spotifydown,p,axis=0)).T

	########### Profiling PornHub caps ###########
	print("Profiling PornHub caps...")
	scalogramAvgPornhub, scales = calcScalogram(pornhubdown)
	M4=np.mean(pornhubdown,axis=0)
	Md4=np.median(pornhubdown,axis=0)
	V4=np.var(pornhubdown,axis=0)
	S4=stats.skew(pornhubdown)
	K4=stats.kurtosis(pornhubdown)
	#p=[25,50,75,90,95]
	#Pr4=np.array(np.percentile(pornhubdown,p,axis=0)).T

	M = np.concatenate((M1,M2,M3,M4),axis=0).reshape((40,1))
	Md = np.concatenate((Md1,Md2,Md3,Md4),axis=0).reshape((40,1))
	V = np.concatenate((V1,V2,V3,V4),axis=0).reshape((40,1))
	S = np.concatenate((S1,S2,S3,S4),axis=0).reshape((40,1))
	K = np.concatenate((K1,K2,K3,K4),axis=0).reshape((40,1))
	print(M.shape)
	#Pr=np.c_[Pr1,Pr2,Pr3,Pr4]
	#features = np.c_[[M],[Md],[V],[S],[K]]
	features = np.concatenate((M,Md,V,S,K),axis=1)
	########### Performing the test ###########

	print("Performing the test...")

	N=300
	dj=1/64
	s0=2
	J=1/dj * np.log2(0.5*N/s0)
	scales=s0*2**(np.arange(J)*dj)

	St,scales=scalogram.scalogramCWT(test,scales)
	Mt=np.mean(test,axis=0)
	Mdt=np.median(test,axis=0)
	Vt=np.var(test,axis=0)
	St=stats.skew(test)
	Kt=stats.kurtosis(test)
	p=[25,50,75,90,95]
	#Prt=np.array(np.percentile(test,p,axis=0)).T

	featuresT=np.c_[[Mt],[Mdt],[Vt],[St],[Kt]]

	print(features)

	print(featuresT)

	print(features.shape)

	print(featuresT.shape)

	###############################
	### Clustering with K-means ###
	###############################

	print('Clustering with K-Means')
	#K-means assuming 2 clusters
	kmeans = KMeans(init='k-means++', n_clusters=4)
	kmeans.fit(features)
	L=kmeans.labels_
	print('class (from features) data1:',L)
	#prediction/classification of data2
	LT=kmeans.predict(featuresT)
	print('class (from features) data2:',LT)

if __name__ == "__main__":
	main()
