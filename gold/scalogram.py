import numpy

def round_2_up(num):
	return  numpy.power(2,numpy.ceil(numpy.log2(num)))

def fMorletWaveletFFT(k, scale, N, precision):
	w=k*2*numpy.pi/N

	if(k>0 and k<int(N/2)):
		basic=numpy.sqrt(scale)*numpy.power(numpy.pi,0.25)*(numpy.exp(-numpy.power(w*scale-precision,2)/2))
	else:
		basic=0
	return basic
	
def CWTfft(data, scales):
	precision=6
	N=int(round_2_up(len(data)))
	fftForw=numpy.fft.fft(data-numpy.mean(data),n=int(N)) #normalize data to mean zero

	kstart=0
	kend=int(N/2)	
	krange=range(kstart,kend+1)
	krangeC=range(kend+1,int(N))
	coefs=numpy.empty((0,N))
	for s in scales:
		fftBack=[]
		for k in krange:
			psi=fMorletWaveletFFT(k,s,N,precision )
			fftBack.append(psi*fftForw[k])
		for k in krangeC:
			fftBack.append(0)
		coefs=numpy.vstack([coefs,abs(numpy.fft.ifft(fftBack))])
	return(coefs[0:,0:len(data)])
    
def scalogramCWT(data,scales):
	C=CWTfft(data, scales)
	centfrq=(6+pow(2+pow(6,2),0.5))/(4*numpy.pi)
		
	C=abs(numpy.power(C,2))
	sC=numpy.sum(C)
	C=100*C/sC
	N=C.shape[1]
	S=numpy.sum(C,axis=1)/N
	fixscales=scales/centfrq;
	
	return S, fixscales
