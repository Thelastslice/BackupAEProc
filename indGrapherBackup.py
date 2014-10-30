import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

import numpy as np
import os
import time
import gc

# plotDir1 = '/Volumes/The Pit/FAC PiezoSensor/Data/flow_80%/noO2/temp_95/trial_1_June_2014/processedData/Test/avePiezo'
# plotDir1 = '/Volumes/The Pit/FAC PiezoSensor/Data/flow_80%/noO2/temp_95/trial_1_June_2014/processedData/Test/avePiezo'
# plotDir1 = '/Volumes/The Pit/FAC PiezoSensor/Data/flow_30%/noO2/temp_95/trial_1_Feb_2014/processedData/piezos'
plotDir2 = '/Volumes/The Pit/FAC PiezoSensor/Data/flow_30%/noO2/temp_95/trial_2_Mar_2014/processedData/avePiezo'
# plotDir3 = '/Volumes/The Pit/FAC PiezoSensor/Data/flow_30%/noO2/temp_95/trial_1_Feb_2014/processedData/accelerometer'
plotDir4 = '/Volumes/The Pit/FAC PiezoSensor/Data/flow_30%/noO2/temp_95/trial_2_Mar_2014/processedData/accelerometer'


xNew = np.load(os.path.join(plotDir2, 'avePSDX.npy'))
yNew = np.load(os.path.join(plotDir2, 'avePSDY.npy'))
zNew = np.load(os.path.join(plotDir2, 'avePSDZ.npy'))
xNew = np.asarray(xNew)
print xNew.shape
yNew = np.asarray(yNew)
print yNew.shape
zNew = np.asarray(zNew)
print zNew.shape

# xOld = np.load(os.path.join(plotDir1, 'avePSDX.npy'))
# yOld = np.load(os.path.join(plotDir1, 'avePSDY.npy'))
# zOld = np.load(os.path.join(plotDir1, 'avePSDZ.npy'))
# xOld = np.asarray(xOld)
# print xNew.shape
# yNew = np.asarray(yNew)
# print yNew.shape
# zNew = np.asarray(zNew)
# print zNew.shape
 
# xAccel = np.load(os.path.join(plotDir4, 'avePSDXAccel.npy'))
# yAccel = np.load(os.path.join(plotDir4, 'avePSDYAccel.npy'))
zAccel = np.load(os.path.join(plotDir4, 'accelChan.npy'))


# np.savetxt(os.path.join(plotDir2, '80zReadout'), zNew)
# 
# xAccel = np.asarray(xAccel)
# print xAccel.shape
# yAccel = np.asarray(yAccel)
# print yAccel.shape
zAccel = np.asarray(zAccel)
print zAccel.shape

zNew = np.transpose(zNew)
zAccel = np.transpose(zAccel)

# xAccel = np.asarray(xAccel)
# print xAccel.shape
# yAccel = np.asarray(yAccel)
# print yAccel.shape
# zAccel = np.asarray(zAccel)
# print zAccel.shape

# zNew = np.transpose(zNew)
#  
# ySplit = np.split(yNew,[1])
# ySplit = np.asarray(ySplit)
# ysplitShape = ySplit.shape
# yCut = ySplit[1]
# print yCut.shape
#   
# zSplit = np.split(zNew,[1])
# zSplit = np.asarray(zSplit)
# splitShape = zSplit.shape
# zCut = zSplit[1]
# print zCut.shape

# xSplit = np.split(yNew,[1])
# xSplit = np.asarray(xSplit)
# xSplitShape = xSplit.shape
# xCut = xSplit[1]
# print xCut.shape
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
# zCut = np.transpose(zCut)


# zOld = [i*6 for i in zOld]
# plt.plot(freq,PSD,'', label='Theirs')
# plt.plot(yNew,zNew[0],'', label='Ours')
# minValZ = np.min(zNew[np.nonzero(zNew)])
# maxValZ = np.max(zNew[np.nonzero(zNew)])
# minValY = np.min(yCut[np.nonzero(yCut)])
# maxValY = np.max(yCut[np.nonzero(yCut)])
# print minValY 
# print maxValY
 
# print minValZ 
# print maxValZ 
# print np.log10(minValZ)
# print np.log10(maxValZ)
# zsubbed = zCut - yCut
# lvls = np.logspace(np.log10(minValZ),np.log10(maxValZ),20)
# plt.subplot(311)
# CF = plt.contourf(xNew,yNew,zNew,norm=LogNorm(),labels='...')
# plt.subplot(312)
# CF = plt.contourf(xNew,xCut,yCut,norm=LogNorm(),labels='...')
# plt.subplot(313)
# CF = plt.contourf(xNew,xCut,zsubbed,norm=LogNorm(),labels='...')

# plt.plot(y1s,z1s,'',label='Time = 0min')
# plt.plot(y1s,z1s,'',label='Time = 0min')
# plt.plot(y1s,z1s,'',label='Time = 0min')
# 
# plt.plot(y1s,z1s,'',label='Time = 0min')
# plt.plot(y1s,z1s,'',label='Time = 0min')
# plt.plot(y1s,z1s,'',label='Time = 0min')
# plt.plot(y1s,z1s,'',label='Time = 0min')
# plt.plot(y1s,z1s,'',label='Time = 0min')
# plt.plot(y1s,z1s,'',label='Time = 0min')
plt.subplot(121)
plt.plot(yNew,zNew[12], label = '2 Hours')
plt.plot(yNew,zNew[991], label = '7 Days')
plt.title('PSD Ave. Piezo.')
plt.legend(loc='best')
plt.xlabel('Hz (cyc/s)')
plt.ylabel('Volt^2/Hz')
# plt.ylim(100,100000)
# plt.xlim(100,500000)
plt.loglog()
plt.subplot(122)
plt.plot(yNew,zAccel[12],label = '2 Hours')
plt.plot(yNew,zAccel[991],label = '7 Days')
plt.tight_layout(pad = 1, h_pad = 0.75, w_pad = 0.18)
# from matplotlib.ticker import LogFormatter
# l_f = LogFormatter(10, labelOnlyBase=False)
# plt.semilogy()
# plt.ylim(100,100000)
# plt.xlim(100,500000)
plt.loglog()
plt.title('PSD Ave. Accel.')
plt.legend(loc='best')
plt.xlabel('Hz (cyc/s)')
plt.ylabel('Volt^2/Hz')
plt.tight_layout(pad = 1, h_pad = 0.75, w_pad = 0.18)
# cbar = plt.colorbar(CF, ticks=lvls, format=l_f)
plt.show()