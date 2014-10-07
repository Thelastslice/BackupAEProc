import numpy as np
import matplotlib.pyplot as plt
import freqBackup as fB
t1 = 1e5
t2 = 1e6

fs = np.float(1*10**3)
N = np.float(1*10**4)
x = (fs/N)
freq = np.float(50)
time = np.arange(0,x,x/N)
shift = 0.005*(2*np.pi*freq)
print shift

sin1 = np.sin(2*np.pi*freq*time)
# with np.errstate(invalid='ignore'):
#     sin2 = sin1/(2*np.pi*freq*time)
# sin1+=sin2 #+np.random.normal(0,1,N)
plt.figure(0)
plt.subplot(311)
# plt.plot(time,sin1)
plt.plot(time,sin1)

'''
Our Auto Code
'''

trial1 = fB.backfreqProcessor(sin1,fs,sin1)
autoCorr = trial1.getAvgAutoCorrNorm(n=1)

Z = autoCorr[1]
freq = autoCorr[0]
# time = np.arange(0,)
plt.subplot(312)
# plt.semilogy()
# plt.ylim(1e-8,1e1)
plt.plot(freq,Z)

'''
Pandas Version
'''
# 
# def acf(series):
#     n = len(series)
#     data = np.asarray(series)
#     mean = np.mean(data)
#     c0 = np.sum((data - mean) ** 2) / float(n)
#     
#     def r(h):
#         acf_lag = ((data[:n - h] - mean) * (data[h:] - mean)).sum() / float(n) / c0
#         return round(acf_lag, 3)
#     x = np.arange(n) # Avoiding lag 0 calculation
#     acf_coeffs = map(r, x)
#     return acf_coeffs
# 
# xValues = acf(sin1)
# plt.subplot(213)
# plt.plot(time,xValues)

'''
Stack Exchange Auto Corr
'''
def estimated_autocorrelation(x):
    """
    http://stackoverflow.com/q/14297012/190597
    http://en.wikipedia.org/wiki/Autocorrelation#Estimation
    """
    n = len(x)
    variance = x.var()
    x = x-x.mean()
    print 'calculating'
    r = np.correlate(x, x, mode = 'full')[-n:]
#     assert np.allclose(r, np.array([(x[:n-k]*x[-(n-k):]).sum() for k in range(n)]))
    result = r/(variance*(np.arange(n, 0, -1)))
    return result
plt.subplot(313)       
stackValues = estimated_autocorrelation(sin1)
print stackValues.shape
print 'plotting'
plt.plot(time,stackValues)
plt.show()