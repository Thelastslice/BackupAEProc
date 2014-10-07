import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import piezoBackup as pF
import numpy as np
import os
import time
import gc

# plotDir1 = '/Volumes/The Pit/FAC PiezoSensor/Data/flow_80%/noO2/temp_95/trial_1_June_2014/processedData/Test/avePiezo'
# plotDir1 = '/Users/Whatsgood/Downloads/flow_35%/highO2/temp_95/flow_ramping/trial_2_June_2014/processedData/Test/avePiezo'
plotDir1 = 'G:/FAC PiezoSensor/Data/flow_35%/highO2/temp_95/flow_ramping/trial_2_June_2014/processedData/Test/crossCorr'

# testCase = pF.piezoTrialNew(plotDir2, dataType='PSD', aliveChan=8)
# test = testCase.getAvgGroup(m=3, n=5)
# freq = test[0]
# PSD = test[1]
# print freq.shape
# print PSD.shape
# print' '
xNew = np.load(os.path.join(plotDir1, 'aveAutoX.npy'))
yNew = np.load(os.path.join(plotDir1, 'aveCrossTau.npy'))
zNew = np.load(os.path.join(plotDir1, 'aveCrossCorr.npy'))
# np.savetxt(os.path.join(plotDir2, '20zReadout'), zNew)
xNew = np.asarray(xNew)
print xNew.shape
yNew = np.asarray(yNew)
print yNew.shape
zNew = np.asarray(zNew)
print zNew.shape

ySplit = np.split(yNew,[1])
ySplit = np.asarray(ySplit)
ysplitShape = ySplit.shape
yCut = ySplit[1]
print yCut.shape

zSplit = np.split(zNew,[1])
zSplit = np.asarray(zSplit)
splitShape = zSplit.shape
zCut = zSplit[1]
print zCut.shape

# np.savetxt(os.path.join(plotDir1, 'zDelReadout'), zDel)
# xOld = np.load(os.path.join(plotDir1, 'avePSDX_old.npy'))
# yOld = np.load(os.path.join(plotDir1, 'avePSDY_old.npy'))
# zOld = np.load(os.path.join(plotDir1, 'avePSDZ_old.npy'))
# xOld = np.asarray(xOld)
# print xOld.shape
# yOld = np.asarray(yOld)
# print yOld.shape
# zOld = np.asarray(zOld)
# print zOld.shape
# print' '
# 
zNew = np.transpose(zNew)
# zOld = np.transpose(zOld)

# zOld = [i*6 for i in zOld]
# plt.plot(freq,PSD,'', label='Theirs')
plt.plot(yNew,zNew[0],'', label='Ours')
minValZ = np.min(zCut[np.nonzero(zCut)])
maxValZ = np.max(zCut[np.nonzero(zCut)])
minValY = np.min(yCut[np.nonzero(yCut)])
maxValY = np.max(yCut[np.nonzero(yCut)])
print minValY 
print maxValY

print minValZ 
print maxValZ 
print np.log10(minValZ)
print np.log10(maxValZ)

# lvls = np.logspace(np.log10(minValZ),np.log10(maxValZ),20)
# CF = plt.contourf(xNew,yNew,zNew,norm=LogNorm(),labels='...')
# plt.plot(freq,PSD,'',label='old')
# from matplotlib.ticker import LogFormatter
# l_f = LogFormatter(10, labelOnlyBase=False)
# plt.semilogy()
# plt.ylim(200,100000)
# plt.xlim(100,500000)
# plt.loglog()
plt.title('Current Code Using Periodogram and old avggroup def')
plt.legend(loc='best')
plt.xlabel('Hz (cyc/s)')
plt.ylabel('Volt^2/Hz')
# cbar = plt.colorbar(CF, ticks=lvls, format=l_f)
plt.show()