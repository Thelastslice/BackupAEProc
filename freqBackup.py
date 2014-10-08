from math import floor
from numpy.fft import fft, fftfreq, ifft, fftshift
from numpy import asarray, mean, var, sqrt
from scipy.signal import periodogram

class backfreqProcessor(object):
    ''' This class will be used to process equally spaced time series data'''
    def __init__(self, x, fs, y=None):
        self.x = x
        self.y = y
        self.fs = float(fs)
        self.df = fs/len(x)
        self.freq = fftfreq(len(x),1.0/fs)
        self.blockFreq = None
        
        self.xfft = None
        self.yfft = None
        
        self.xPSD = None
        self.yPSD = None
        self.xyPSD = None
        
        self.avgxPSD = None
        self.avgyPSD = None
        self.avgxyPSD = None
               
    def getxfft(self,x=None): #helper function for PSD
        if x==None:
            if self.xfft == None:
                xbar = mean(self.x)
                xhat = [i-xbar for i in self.x]
                self.xfft = fft(xhat)
                return self.xfft
            else:
                return self.xfft
        else:
            xbar = mean(x)
            xhat = [i-xbar for i in x]
            return fft(xhat) 
            
    def getyfft(self,y=None): #helper function for PSD
        if y==None:
            if self.yfft == None:
                ybar = mean(self.y)
                yhat = [i-ybar for i in self.y]
                self.yfft = fft(yhat)
                return self.yfft
            else:
                return self.yfft
        else:
            yhat = mean(self.y)
            yhat = [i-yhat for i in self.y]
            return fft(yhat)      
    
    def getPSD(self,x=None):
        if x==None:
            if self.xPSD == None:
                self.xPSD = [abs(i*i.conjugate()/(self.fs**2/self.df)) for i in self.getxfft()]
                return self.freq, self.xPSD
            else:
                return self.freq, self.xPSD
        else:
            xbar = mean(x)
            xhat = [i-xbar for i in x]
            x1 = fft(xhat)
            df = self.fs/len(x1)
            tempxPSD = [abs(i*i.conjugate()/(self.fs**2/df)) for i in x1]
#             tempF, tempxPSD = periodogram(x,fs=self.fs,return_onesided=False)
            return tempxPSD
                
    def getCrossPSD(self, x=None, y=None):
        if x==None and y==None:
            if self.xyPSD == None:
                self.xyPSD = [abs(i*j.conjugate()/(self.fs**2/self.df)) for i,j in zip(self.getxfft(),self.getyfft())]
                return self.xyPSD
            else:
                return self.xyPSD
        else:
            if len(x)==len(y):
                df = self.fs/len(x)
                tempCrossPSD = [abs(i*j.conjugate()/(self.fs**2/df)) for i,j in zip(self.getxfft(x),self.getyfft(y))]
                return tempCrossPSD
            else:
                raise ValueError('x and y must be the same length')
                
    def avgPSD(self,n):
        PSD = list()
        blockLength = int(floor(len(self.x)/n))
#         blockFreq = fftfreq(blockLength,1.0/self.fs)
#         df = blockFreq[1] - blockFreq[0]
        for i in range(n):
            xBlock = self.x[i*blockLength:(i+1)*blockLength] 
            PSD.append([self.getPSD(xBlock)])
            
        PSD = asarray(PSD)
        temp = mean(PSD, axis=0)   
        return temp[0]
    
    def avgPSDNorm(self,n):
        PSD = list()
        blockLength = int(floor(len(self.x)/n))
#         blockFreq = fftfreq(blockLength,1.0/self.fs)
#         df = blockFreq[1] - blockFreq[0]
        for i in range(n):
            xBlock = self.x[i*blockLength:(i+1)*blockLength]
            xBlockVar = var(xBlock)
            R = self.getPSD(xBlock)
            print xBlockVar
            print 'yolo'
            R = [i/xBlockVar for i in R] 
            
            PSD.append([R])
                      
        PSD = asarray(PSD)
        temp = mean(PSD, axis=0)
        
        return temp[0]
    
    
    def avgCrossPSD(self,n):
        crossPSD = list()
        blockLength = int(floor(len(self.x)/n))
#         blockFreq = fftfreq(blockLength,1.0/self.fs)
#         tau = range(blockLength)/self.fs
#         tauBar = mean(tau)
#         tau = [i-tauBar for i in tau]
#         df = blockFreq[1] - blockFreq[0]
        for i in range(n):
            xBlock = self.x[i*blockLength:(i+1)*blockLength]
            yBlock = self.y[i*blockLength:(i+1)*blockLength]            
            blockVar = var(zip(xBlock,yBlock))
            print blockVar
            print 'swag'
            crossSave = [self.getCrossPSD(xBlock,yBlock)]
            crossNorm = [i/blockVar for i in crossSave]
            crossPSD.append(crossNorm)   
                      
        crossPSD = asarray(crossPSD)
        temp = mean(crossPSD, axis=0)
        
        return temp[0]
    

    def avgAutoCorrelation(self,n=None):
        if n==None:
            n=1
        avgPSD = self.avgPSD(n)
        R = ifft(avgPSD)*self.fs
        return R
    
    def avgAutoCorrelationNorm(self,n=None):
        if n==None:
            n=1
        avgPSD = self.avgPSDNorm(n)
        R = ifft(avgPSD)*self.fs
        R = fftshift(R)
        return R

    def avgCrossCorrelation(self,n=None):
        if n==None:
            n=1
        crossPSD = self.avgCrossPSD(n)
        R = ifft(crossPSD)*self.fs
        R = fftshift(R)
        return R       
         
    def getFrequency(self,x=None):
        if x==None:
            blockLength = len(self.x)
        else:
            blockLength = len(x)
        freq = fftfreq(blockLength,1.0/self.fs)
        return freq
    
    def getTau(self,x=None):
        if x==None:
            blockLength = len(self.x)
        else:
            blockLength = len(x)
        mid = range(blockLength)
        tau = [mid[i]/self.fs for i in mid]
        
        tauBar = mean(tau)
        tau = [i-tauBar for i in tau]
        return tau
    
    def getAvgPSD(self,n=None):
        if n==None:
            n=1
        PSD = self.avgPSD(n)
        freq = self.getFrequency(PSD)
        return freq, PSD
    
    def getAvgAutoCorrelation(self,n=None):
        if n==None:
            n=1
        R = self.avgAutoCorrelation(n)
        tau = self.getTau(R)
        return tau,R
    
    def getAvgCrossCorrelation(self,n=None):
        if n==None:
            n=1
        R = self.avgCrossCorrelation(n)
        tau = self.getTau(R)
        return tau, R
    
    def getAvgAutoCorrNorm(self,n=None):
        if n==None:
            n=1
        R = self.avgAutoCorrelationNorm(n)
        tau = self.getTau(R)
        return tau,R
    
        
        
        
        
        
        
        
        