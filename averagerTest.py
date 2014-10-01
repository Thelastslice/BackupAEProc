import numpy as np
from math import floor

def avgPSD(x,n):
        PSD = list()
        blockLength = int(floor(len(x)/n))
#         blockFreq = fftfreq(blockLength,1.0/self.fs)
#         df = blockFreq[1] - blockFreq[0]
        for i in range(n):
            xBlock = x[i*blockLength:(i+1)*blockLength] 
            print xBlock
            PSD.append([xBlock])
            
#         PSD = self.getPSD(self.x)        
        PSD = np.asarray(PSD)
        print PSD.shape
        temp = np.mean(PSD, axis=0)   
        return temp[0]
    
def getPSD(x):
    pass


x=np.arange(0,45000,1)
n=5
fuck = avgPSD(x,n)
print fuck


# for i in range(5):
    
