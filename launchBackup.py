import piezoBackup as tdp
import os
import re
import cProfile as cP
# Set the directory of your voltage data
# mainDir = '/Volumes/The Pit/FAC PiezoSensor/Data/'
mainDir = '/Users/Whatsgood/Downloads/flow_35%/highO2/temp_95/flow_ramping/trial_2_June_2014'
# mainDir = 'G:/FAC PiezoSensor/Data/'

for subdir, dirs, files in os.walk(mainDir):
    if subdir.endswith('rawData'):
        print 'Data from: '+subdir
        output = subdir.replace('rawData','')
        print 'Saving to: ' + output
        dataType = 'PSD'
        
        if re.search( r'highO2/temp_95/flow_ramping/trial_2_June_2014', subdir):
            channels = 5
            print 'Only 3 Piezo Channels Active'
            inputFs = 1*10**6
            
        
        elif re.search( r'highO2/temp_95/flow_ramping/trial_3_Sept_2014', subdir):
            channels = 5
            inputFs = 1*10**5
            print 'Only 3 Piezo Channels Active'
                 
        elif re.search( r'noO2/temp_140/', subdir):
            channels = 5
            print 'Only 3 Piezo Channels Active'
            if re.search( r'/temp_140/trial_2', subdir):
                inputFs = 1*10**5
            else:
                inputFs = None   
                 
        elif re.search( r'noO2/temp_200/', subdir):
            channels = 5
            inputFs = 1*10**5
            print 'Only 3 Piezo Channels Active'
             
        else:
            channels = 8
            inputFs = 1*10**6
            print '6 Piezo Channels Active'
        
        trial = tdp.backpiezoTrial(subdir+'/',dataType, channels, output, fs = inputFs)
        Accel = False
        cP.run('print trial.getAveTimeContour(Accel); print')  
 
#         Accel = True
#         PSDacc = trial.getAveTimeContour(Accel)
        
#         dataType = 'autoCorr'
#         trial = tdp.dataProc(subdir+'/', channels, output,dataType, fs = inputFs)
#         Accel = False
#         autoCorrelation =  trial.getAveTimeContour(Accel)
#         Accel = True
#         autoCorrelationacc = trial.getAveTimeContour(Accel)
        
#         dataType = 'crossCorr'
#         trial = tdp.dataProc(subdir+'/', channels, output,dataType, fs = inputFs)
#         Accel = False
#         crossCorrelation =  trial.getAveTimeContour(Accel)
#         Accel = True
#         crossCorrelationacc = trial.getAveTimeContour(Accel)
        
        
#             
# numberOfChannels = 5
# # lastRun = 20
# trial1 = tdp.dataProc(dirName, dataDir, numberOfChannels, outputDir)
# PSDAccRun = trial1.getAccContourPSD()
#  
# PSDRun = trial1.getAveContourPSD()
#  
# print 'Dataset 1 Done'
# numberOfChannels = 5
# trial2 = tdp.dataProc(dirName2, dataDir2, numberOfChannels, outputDir2)
# PSDAccRun = trial2.getAccContourPSD()
# # 
# PSDRun = trial2.getAveContourPSD()
# # # corrRun = trial.getAutoCorrelation()

