import os
import re
import csv
import math
import freqBackup as fp
from scipy.signal import butter, lfilter
import numpy as np
import matplotlib.pyplot as plt

class backpiezoTrial(object):
    
    
    def __init__(self, dataDir, dataType, numberOfChannels, outputDir, fs, lastRun = None, dataFile=None):
        
        #Declaring Class Inputs
        self.dataDir = dataDir
        self.dataType = dataType
        self.numberOfChannels = numberOfChannels
        self.outputDir = outputDir
        self.fs  = np.float(fs)
        self.lastRun = lastRun
        self.dataFile = dataFile
        
        #Declaring Class Global Variables
        self.channelList = None
        self.accelerometerList = None
        self.groupList = None
        self.PSDTrue = None
        self.process = None
        self.y = None
        self.aliveChan = None
        
        #Datatype declarations
        self.PSDType = False
        self.autoCorrType = False
        self.crossCorrType = False
        self.covarianceType = False
        self.saveChan = None

        #Piezos Class Global Variables
        self.maxFreq = None
        self.piezoFileName = None
        
        self.X = None
        self.Y = None
        self.Z = None
        
        #Accelerometer Class Global Variables
        self.accZ = None
        self.accY = None
        self.accX = None

        #Making Primary Processed Data Storage Directory
        self.plotDir = self.outputDir+'processedData/Test'+'/'
         
        if not os.path.exists(self.plotDir):
            os.makedirs(self.plotDir)
                   
        #Checksums
        if self.numberOfChannels == 5:
            self.aliveChan = 3
        else:
            self.aliveChan = 6 
        
        #Butterworth Filter Criteria
#         self.fs=10**6
#         self.highcutoff = 200000
        self.lowcutoff = np.float(300)
        self.order = 2
        self.fileType = '.txt'
        
        if fs==1.0*10**6:
            self.highcutoff = np.float(200000)
            print self.highcutoff
             
        else:
            self.highcutoff = fs/2
            print self.highcutoff
        
        if dataFile == None:
            self.dataFile = os.listdir(dataDir)
            self.dataFile = [i for i in self.dataFile if i.endswith(self.fileType)]
            self.dataFile = sorted(self.dataFile,key=self.numericalSort)
        else:
            self.dataFile = dataFile
    
        if self.dataType == 'PSD':
            self.PSDType = True
            self.saveChan = self.plotDir + '/' + 'avePiezo'             
            self.process = 'getAvgPSD'
            self.y = [0,0,0,0,0,0]
            
            if not os.path.exists(self.saveChan):
                os.makedirs(self.saveChan)
                
            print 'Datatype = PSD'
            print 'Calculating Averaged Multifile PSD'
            
        elif self.dataType == 'autoCorr':
            self.autoCorrType = True
            self.saveChan = self.plotDir + '/' + 'AutoCorr' 
            self.process = 'getAvgAutoCorrNorm'
            self.y = [0,0,0,0,0,0]
         
            if not os.path.exists(self.saveChan):
                os.makedirs(self.saveChan)
                
            print 'Datatype = Auto Correlation'
            print 'Calculating Averaged Multifile Auto Correlation'
        
        elif self.dataType == 'crossCorr':
            self.crossCorrType = True
            self.saveChan = self.plotDir + '/' + 'crossCorr' 
            self.process = 'getAvgCrossCorrelation'
            group1 = list()
            
            if not os.path.exists(self.saveChan):
                os.makedirs(self.saveChan)
            
            for i in self.dataFile[0:self.aliveChan]:
                rawData = self.readAECSV(self.dataDir, i,' ')
                y = [float(j[1]) for j in rawData]
                y = self.butter_bandpass_filter(y)
                # Taking the last 90% of the sample to ignore the junk at the beginning of the filtered data
                y = y[math.floor(len(y)*0.1):]
                group1.append(y)
                 
            group1 = np.asarray(group1)
#             self.y = mean(group1, axis=0)    
            self.y = group1
            
            print 'Calculating Averaged Multifile Cross Correlation'
            print 'Datatype =  Cross Correlation'
        
        elif self.dataType == 'covariance':
            self.covarianceType = True
            print 'Datatype =  Covariance'
            print 'No Covariance'
            pass
        
        else:
            raise Exception('Invalid dataType entry, currently available options: "PSD", "autoCorr", "crossCorr", "covariance"')
         
    def numericalSort(self,value):
        numbers = re.compile(r'(\d+)')
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts
        
    def getFileNames(self):
        return self.dataFile
    
    def readAECSV(self,dirname, filename,sep):
        with open(dirname + str(filename)) as csvFile:
            datareader = csv.reader(csvFile, delimiter=sep)
            data = list() 
            append = data.append
            for row in datareader:
                append(row)
            return data
        
    def readAEBin(self,dirname, filename,sep):
        with open(dirname + str(filename), "rb") as binFile:
            datareader = np.fromfile(binFile, dtype=np.float64)
            data = list() 
            append = data.append
            for row in datareader:
                append(row)
            return data

    #Pull all datafiles (text) from the chosen directory
    def getDataFiles(self):
        self.dataFile = self.getFileNames()
        return self.dataFile
    
    #Get last run numbrer from datafiles in chosen directory
    def getLastRun(self):
        if self.lastRun == None: 
            data = self.getDataFiles()
            self.lastRun = int(re.match( r'Run_(.*)_C', data[len(data)-1]).group(1))
        else:
            self.lastRun = self.lastRun
        return self.lastRun
    
    #File name generator for piezo channels
    def fileNameGen(self,i,x):
        self.piezoFileName = 'Chan' + str(i) + x
        return self.piezoFileName  
    
    #Retrieves six piezo channel files for each run
    def getGroupList(self,runNumber,aliveChan):
        groupList = list()
        groupAppend  = groupList.append
        for j in range(self.numberOfChannels):
            fName = 'Run_'+str(runNumber)+'_Channel_'+str(j)+'.txt'
            if j<aliveChan:
                groupAppend(fName)
            else:
                None
        return groupList
            
    #Creates Dictionary that separates each piezo channel into their own respective indices
    def getChannelList(self, runNumber): 
        self.channelList = {}
         
        #Iterate through dataDir to separate txt files by their respective channel #
        for j in range(self.numberOfChannels):
            fName = 'Run_'+str(runNumber)+'_Channel_'+str(j)+'.txt'
            if j == 0:
                self.channelList['Chan0'] = fName 
            elif j == 1:
                self.channelList['Chan1'] = fName   
            elif j == 2:
                self.channelList['Chan2'] = fName
            elif j == 3:
                self.channelList['Chan3'] = fName
            elif j == 4:
                self.channelList['Chan4'] = fName
            elif j == 5:
                self.channelList['Chan5'] = fName
            else:
                None
            
        return self.channelList
    
    #Function to pull only accelerometer runs out of the chosen parent directory
    def getAccelerometerList(self, runNumber,aliveChan):
        
        self.accelerometerList = list()
        aCAppend = self.accelerometerList.append
        
        #Iterate through dataDir to find separate out only the accelerometer channels
        for j in range(8):
            fName = 'Run_'+str(runNumber)+'_Channel_'+str(j)+'.txt'
            if j >= 6:
                aCAppend(fName)
         
        return self.accelerometerList    
    

    def butter_bandpass(self,lowcut,highcut,fs,order):
        nyq = 0.5*fs
        low = lowcut/nyq
        high = highcut/nyq

        b,a = butter(order, [low, high], btype='band')
        return b,a

    def butter_bandpass_filter(self,data,lowcut=None,highcut=None,fs=None,order=None):
        if lowcut==None:
            lowcut = self.lowcutoff
        if highcut==None:
            highcut = self.highcutoff
        if fs==None:
            fs = self.fs
        if order==None:
            order=self.order
        b,a = self.butter_bandpass(lowcut,highcut,fs,order)
        return lfilter(b,a,data) 
    
    def plotFiltered(self):
        for i in self.dataFile:
            rawData = self.readAECSV(self.dataDir, i,' ')
            xRaw = [float(i[1]) for i in rawData]
            filterX = self.butter_bandpass_filter(xRaw)
            plt.plot(xRaw)
            plt.plot(filterX)
            plt.show()
        return None

    def getAvgGroup(self, m=None, n=None):
        #Function specific global declarations to increase efficiency
        groupZ = list()
        rD = self.readAECSV
        #rD = self.readAEBin
        loopButter = self.butter_bandpass_filter
        fD = fp.backfreqProcessor
        
        if m==None:
            m=len(self.dataFile)
        if n==None:
            n=1
            
        for i in range(m):
            rawData = rD(self.dataDir, self.dataFile[i],' ')
            x = [float(j[1]) for j in rawData]
            x = loopButter(x)
            # Taking the last 90% of the sample to ignore the junk at the beginning of the filtered data
            x = x[math.floor(len(x)*0.1):]
            freqData = fD(x,self.fs, self.y[i])
            methodToCall = getattr(freqData, self.process)
            Y, Z = methodToCall(n)
            groupZ.append(Z)
            
        groupZ = np.asarray(groupZ)
        temp = np.mean(groupZ, axis=0)
        return Y,temp
    
    
    def getAvgMultiFiles(self,dataFiles=None, n=None):       
        #Function specific global declarations to increase efficiency
        groupZ = list()
        rD = self.readAECSV
        #rD = self.readAEBin
        loopButter = self.butter_bandpass_filter
        fD = fp.backfreqProcessor
        append = groupZ.append
        
        if dataFiles==None:
            dataFiles=self.dataFile
        if n==None:
            n=1
        fileIter = 0
        
        for i in dataFiles:
            rawData = rD(self.dataDir, i,' ')
            x = [float(j[1]) for j in rawData]
            x = loopButter(x)
            # Taking the last 90% of the sample to ignore the junk at the beginning of the filtered data
            x = x[np.floor(len(x)*0.1):]
            freqData = fD(x,self.fs,self.y[fileIter])
            methodToCall = getattr(freqData, self.process)
            Y,Z = methodToCall(n)
            
            append(Z)
            fileIter = fileIter+1
            
        groupZ = np.asarray(groupZ)
        temp = np.mean(groupZ, axis=0)
        return Y,temp

        return Y,temp

    def PSDChanTimeContour(self, chanNum):
         
        '''
        "chanTimeContour" computes and returns the PSDRun, freqTemp and 
        maxFreq for a given channel number from all runs
        ''' 
        lastRun = self.getLastRun()
        
        self.PSDRun = list()
        self.maxFreq = list()
        self.x1 = list()
         
        PSDget = self.getAvgMultiFiles
        PSDRappend = self.PSDRun.append
        maxFappend = self.maxFreq.append
        npWhere = np.where
        xAppend = self.x1.append
        getChannel = self.getChannelList
       
        for i in range(lastRun):
            while True:
                try:
#                     tic = time.clock()
                    runNumber = i+1
                    channelList = getChannel(runNumber)
                    nameList = list()
                    nameList.append(channelList['Chan'+str(chanNum)])
                    
                    self.freqTemp, PSDTemp = PSDget(nameList,5)
                    PSDRappend(PSDTemp)
                          
                    windowTemp = npWhere(self.freqTemp>=10**1)
                    lowCutOff = windowTemp[0][0]
                    windowTemp = npWhere(self.freqTemp>=10**3)
                    highCutOff = windowTemp[0][0]
                      
                    maxPSD = max(PSDTemp[lowCutOff:highCutOff])
                    maxInd = npWhere(PSDTemp==maxPSD)
                    maxFappend(self.freqTemp[maxInd[0][0]])
                    xAppend(i+1)
                     
                    print 'Run:'+str(i+1)+' '+'Chan:'+str(chanNum) #Visual id of calc status
#                     toc = time.clock()
#                     print toc-tic
                    break
                 
                except IOError:
                    print 'Error at Run:'+str(i+1)+' '+'Chan:'+str(chanNum) +'-> '+ 'File not found'
                    break
             
        return self.PSDRun, self.freqTemp, self.maxFreq, self.x1
    
     
    def getPSDChanTimeContour(self):
       
        #Making the Piezo data file sub-directory
        piezoChan = self.plotDir + '/' + 'avePiezo'
        
        slopePerHour = list()
        slopeAppend = slopePerHour.append
        #Iterates time contour calculation for all runs on each piezo channel
        for i in range(6):
            fun = self.PSDChanTimeContour(i)
            PSDRun = fun[0] 
            freqTemp = fun[1]
            maxFreq = fun[2]
            x1 = fun[3]

            # Calculates the max of each PSD and computes the overall slope w/ time
            maxFreq = np.asarray(maxFreq)
            y1 = maxFreq
            fitMaxFreqCoeff = np.polyfit(x1,y1,1)
            fitMaxClass = np.poly1d(fitMaxFreqCoeff)
            fitMaxData = fitMaxClass(x1)
            slope = fitMaxFreqCoeff[0]*6.0
            slopeAppend(slope)
           
            #Creates Numpy arrays for the time contour plot of each piezo channel
            X = np.asarray(x1)
            Y = np.asarray(freqTemp)
            Z = np.asarray(PSDRun)
            Z = np.transpose(Z)
            
            np.save(os.path.join(piezoChan, self.fileNameGen(i,'X')),X)
            np.save(os.path.join(piezoChan, self.fileNameGen(i,'Y')),Y)
            np.save(os.path.join(piezoChan, self.fileNameGen(i,'Z')),Z)
            np.save(os.path.join(piezoChan, self.fileNameGen(i,'fitMaxData')),fitMaxData)

             
#         #Saves the slope/hour of each piezo channel to a single text file in an array
        sph = np.asarray(slopePerHour)
        np.save(os.path.join(piezoChan, self.fileNameGen(0,'sph')),sph)
    
    def aveTimeContour(self,accel=False):
        
        lastRun = self.getLastRun()
        
        self.Z = list()
        self.Y = list()
        self.X = list()
        self.maxFreq = list()
            
        DataGet = self.getAvgMultiFiles    
        npWhere = np.where
        
        Zappend = self.Z.append
        xAppend = self.X.append
        maxFappend = self.maxFreq.append
        
        #Accelerometer checksum
        if accel == True:
            getGroup = self.getAccelerometerList
            accText = 'Accel'
            
        elif accel == False:
            getGroup = self.getGroupList
            accText = ''
        
        else:
            pass
        
        for i in range(lastRun):
            while True:
                try:
    #                     tic = time.clock()
                    runNumber = i+1
                    groupList = getGroup(runNumber,self.aliveChan)    
                    self.Y, tempZ = DataGet(groupList,5)
                    Zappend(tempZ)
                    xAppend(i+1)
                    
                    if self.PSDType == True:      
                        windowTemp = npWhere(self.Y>=10**1)
                        lowCutOff = windowTemp[0][0]
                        windowTemp = npWhere(self.Y>=10**3)
                        highCutOff = windowTemp[0][0]
                          
                        maxPSD = max(tempZ[lowCutOff:highCutOff])
                        maxInd = npWhere(tempZ==maxPSD)
                        maxFappend(self.Y[maxInd[0][0]])
                    
                    else:
                        pass
                     
                    print 'Run:'+str(i+1)+' '+ self.dataType+' '+accText #Visual id of calc status
    #                     toc = time.clock()
    #                     print toc-tic
                    break
                 
                except IOError:
                    print 'Error at Run:'+str(i+1)+' '+self.dataType+' '+accText+' -> '+ 'File not found'
                    break
    
        return self.Z, self.Y, self.X, self.maxFreq
    

    def getAveTimeContour(self,accel=False):
        '''
        "getAveContourPSD" runs the time contour computation for the averaged 6 piezo channels
        and saves the PSD, frequency and run number to separate and relevantly named
        text files within the piezos sub-directory in the created plot-data directory
        of the chosen run.
        '''
        
        if accel == True:
            acc = 'Accel'
            
        elif accel == False: 
            acc = ''
            
        else:
            raise Exception('Invalid accel entry, currently available options: "True", "False"') 
        
        slopePerHour = list()
        slopeAppend = slopePerHour.append
        
        dataRetrieve = self.aveTimeContour(accel)
        runZ = dataRetrieve[0] 
        runY = dataRetrieve[1]
        runX = dataRetrieve[2]
        maxFreq = dataRetrieve[3]

        #Creates Numpy arrays for the time contour plot of each piezo channel
        X = np.asarray(runX)
        Y = np.asarray(runY)
        Z = np.asarray(runZ)
        Z = np.transpose(Z)
        
        
        if self.PSDType == True:
            
            # Calculates the max of each PSD and computes the overall slope w/ time
            maxFreq = np.asarray(maxFreq)
            y1 = maxFreq
            fitMaxFreqCoeff = np.polyfit(X,y1,1)
            fitMaxClass = np.poly1d(fitMaxFreqCoeff)
            fitMaxData = fitMaxClass(X)
            slope = fitMaxFreqCoeff[0]*6.0
            slopeAppend(slope)
        
            np.save(os.path.join(self.saveChan, 'avePSDX'+acc),X)
            np.save(os.path.join(self.saveChan, 'avePSDY'+acc),Y)
            np.save(os.path.join(self.saveChan, 'avePSDZ'+acc),Z)
            np.save(os.path.join(self.saveChan, 'aveFitMaxData'+acc),fitMaxData)
            sph = np.asarray(slopePerHour)
            np.save(os.path.join(self.saveChan, 'sph'+acc),sph)
            
        elif self.autoCorrType == True:
            np.save(os.path.join(self.saveChan, 'aveAutoCorr'+acc), Z)
            np.save(os.path.join(self.saveChan, 'aveAutoTau'+acc), Y)
            np.save(os.path.join(self.saveChan, 'aveAutoX'+acc), X)
            
        elif self.crossCorrType == True:
            np.save(os.path.join(self.saveChan, 'aveCrossCorr'+acc), Z)
            np.save(os.path.join(self.saveChan, 'aveCrossTau'+acc), Y)
            np.save(os.path.join(self.saveChan, 'aveAutoX'+acc), X)
        
        else:
            print 'Covariance not established'
            pass