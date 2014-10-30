import numpy as np
import matplotlib.pyplot as plt
import freqBackup as fB
fs=100
N = 1e4
x = (fs/N)
 
freq = 100
time = np.arange(0,x,x/N)
print len(time)
# shift = 0.005*(2*np.pi*freq)

sin1 = np.sin(2*np.pi*100*time)
# with np.errstate(invalid='ignore'):
#     sin2 = 1.5*sin1/(np.pi*2*freq*time)+np.random.normal(0,1,N)
#     sin1 = sin1/(np.pi*2*freq*time)
# print sin2
# sin2 = np.nan_to_num(sin2)
# sin1 = np.nan_to_num(sin1)
# print sin2

# sin1+=sin2 #+np.random.normal(0,1,N)
plt.figure(0)
plt.subplot(211)
plt.title('Input Signal')
plt.plot(time,sin1)
plt.xlabel('Tau (s)')
plt.ylabel('Amplitude')
plt.subplot(212)
# plt.plot(time,sin2)
sin1 = np.asarray(sin1)
time = np.asarray(time)
'''
Our Auto Code
'''

trial1 = fB.backfreqProcessor(sin1,fs)
autoCorr = trial1.getAvgAutoCorrNorm(n=1)
Z = autoCorr[1]
freq = autoCorr[0]

# crossCorr = trial1.getAvgCrossCorrelation(n=1)
# 
# Z2 = crossCorr[1]
# freq2 = crossCorr[0]
# print Z[1:10]
# print Z2[1:10]
# time = np.arange(0,)
# plt.subplot(412)
# plt.semilogy()
# plt.ylim(1e-8,1e1)
time2 = time-0.005
plt.plot(time2,Z)
plt.tight_layout(pad = 3, h_pad = 1.75, w_pad = 0.15)
plt.title('Auto-Correlation')
plt.xlabel('Tau (s)')
plt.ylabel('Amplitude')
# 
# ass = np.correlate(sin1,sin2,mode='same')
# assNorm = ass/np.var(sin1)
# plt.subplot(413)
# plt.plot(freq,assNorm/N)
# # print assNorm/np.arange(len(sin1)-1, -1, -1)
# '''
# more stack exchange
# '''
# def acf(x, times):
#     return np.array([1]+[np.corrcoef(x[:-i], x[i:]) for i in range(1, times)])

# print acf(sin1,time)
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

# 
# plt.subplot(414)
# time2 = range(19999)
# 
# plt.plot(freq2,Z2)
plt.show()