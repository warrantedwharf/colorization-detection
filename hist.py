#import libraries
import cv2
import matplotlib.pyplot as plt
import numpy as np
from glob import glob
import time

#calculate extreme channel priors module 
def ecp(imgname):
    #dark channel & bright channel generation
    height,width,s = imgname.shape
    dc = np.zeros([height,width], dtype=np.uint8)
    bc = np.zeros([height,width], dtype=np.uint8)
    padval=2
    WHITE=[255,255,255]
    BLACK=[0,0,0]
    padded1=cv2.copyMakeBorder(imgname,padval,padval,padval,padval,cv2.BORDER_CONSTANT,value=WHITE)
    padded2=cv2.copyMakeBorder(imgname,padval,padval,padval,padval,cv2.BORDER_CONSTANT,value=BLACK)

    for i in range(0,height):	
        for j in range(0,width):
            temp1=[]
            temp2=[]
            for k in range(i-padval,i+padval+1):
                for l in range(j-padval,j+padval+1):
                    y=[]
                    z=[]
                    for m in range(3):
                        y.append(padded1[k][l][m])
                        z.append(padded2[k][l][m])
                    temp1.append(min(y))
                    temp2.append(max(z))
            dc[i][j]=min(temp1)
            bc[i][j]=max(temp2)
    return dc,bc

#identify most distinctive bin (Vh)
def f1(hist):
    pos = 0
    vhval = hist[0]
    for i in range(1,200):
        if(hist[i]>vhval):
            vhval = hist[i]
            pos = i
    return pos

#function for histogram distribution
def hist_dist():
    images = glob(path)
    huedist = [0]*1 #hue distribution
    satdist = [0]*1 #sat distribution
    darkdist = [0]*1 #dark ch distribution
    brightdist = [0]*1 #bright ch distribution

    #progress calculation
    size = len(images)
    progress = 0
    i=0

    for j in images:
        start = time.time()
        img = cv2.imread(j)
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)#convert to hsv

        rdc,rbc = ecp(img)
        
        hue_hist = cv2.calcHist([hsv], [0], None, [200],[0,200])#calculating hue histogram
        sat_hist = cv2.calcHist([hsv], [1], None, [200],[0,200])#calculating sat histogram
        dark_hist = cv2.calcHist([rdc],[0],None,[200],[0,200])
        bright_hist = cv2.calcHist([rbc],[0],None,[200],[0,200])

        #addition of pixels
        huedist += hue_hist 
        satdist += sat_hist
        darkdist += dark_hist
        brightdist += bright_hist

        end = start - time.time()
        #progress
        progress+=1/size
        i+=1
        time_rem = (end * (size-i))/3600

        print("Progress: {}%, Images Processed: {}, Time:{} sec, ETC:{} hrs".format(progress*100,i,end,time_rem))
        

    #normalize histograms
    huedist = cv2.normalize(huedist, None)
    satdist = cv2.normalize(satdist, None)
    darkdist = cv2.normalize(darkdist, None)
    brightdist = cv2.normalize(brightdist, None)

    return huedist,satdist,darkdist,brightdist



        
#real images

path = 'D:/Users/Abel/Documents/ocv/colorized/creal10k/*.jpeg' #set path accordingly

#distribution of real images
hd,sd,dd,bd = hist_dist()

#fake images

path = 'D:/Users/Abel/Documents/ocv/colorized/ctest10k/*.png' #set path accordingly

#distribution of fake images
fhd,fsd,fdd,fbd = hist_dist()

#absolute difference of histograms
abs_hue = abs(hd - fhd)
abs_sat = abs(sd - fsd)
abs_dd = abs(dd - fdd)
abs_bd = abs(bd - fbd)

#Vh value of fake-real pair
vh_hue = f1(abs_hue)
vh_sat = f1(abs_sat)
vh_dd = f1(abs_dd)
vh_bd = f1(abs_bd)

print("Vh val| Hue:{}, Sat:{}, Dark:{}, Bright:{}".format(vh_hue,vh_sat,vh_dd,vh_bd))
