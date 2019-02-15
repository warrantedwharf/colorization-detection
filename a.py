import cv2
import matplotlib.pyplot as plt
import numpy as np
from glob import glob
from tqdm import tqdm


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
    huedist = np.zeros([200,1], dtype=float) #hue distribution
    satdist = np.zeros([200,1], dtype=float) #sat distribution
    darkdist = np.zeros([200,1], dtype=float) #dark ch distribution
    brightdist = np.zeros([200,1], dtype=float) #bright ch distribution

    #progress calculation
    size = len(images)

    for j in tqdm(images):
        img = cv2.imread(j)
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)#convert to hsv
        

        rdc =  cv2.imread(dpath + j[26:])
        rbc = cv2.imread(bpath + j[26:])
        
        hue_hist = cv2.calcHist([hsv], [0], None, [200],[0,200])#calculating hue histogram
        sat_hist = cv2.calcHist([hsv], [1], None, [200],[0,200])#calculating sat histogram
        dark_hist = cv2.calcHist([rdc],[0],None,[200],[0,200])
        bright_hist = cv2.calcHist([rbc],[0],None,[200],[0,200])

        #addition of pixels
        huedist += hue_hist 
        satdist += sat_hist
        darkdist += dark_hist
        brightdist += bright_hist


        

    #normalize histograms
    huedist = cv2.normalize(huedist, None)
    satdist = cv2.normalize(satdist, None)
    darkdist = cv2.normalize(darkdist, None)
    brightdist = cv2.normalize(brightdist, None)

    return huedist,satdist,darkdist,brightdist



        
#real images

path = 'D:/ocv/colorized/creal10k/*.jpeg' #set path accordingly

dpath = 'D:/ocv/colorized/rdc/'

bpath = 'D:/ocv/colorized/rbc/'

#distribution of real images
hd,sd,dd,bd = hist_dist()

#fake images

path = 'D:/ocv/colorized/ctest10k/*.png' #set path accordingly

dpath = 'D:/ocv/colorized/fdc/'

bpath = 'D:/ocv/colorized/fbc/'

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

plt.subplot(4,3,1)
plt.plot(hd,color='r')
plt.title('Real Hue Dist')

plt.subplot(4,3,2)
plt.plot(fhd,color='b')
plt.title('Fake Hue Dist')

plt.subplot(4,3,3)
plt.plot(abs_hue,color='g')
plt.title('Absolute difference HUE')

plt.subplot(4,3,4)
plt.plot(sd,color='r')
plt.title('Real sat Dist')

plt.subplot(4,3,5)
plt.plot(fsd,color='b')
plt.title('Fake Sat Dist')

plt.subplot(4,3,6)
plt.plot(abs_sat,color='g')
plt.title('Absolute difference SAT')

plt.subplot(4,3,7)
plt.plot(dd,color='r')
plt.title('Real Dark Dist')

plt.subplot(4,3,8)
plt.plot(fdd,color='b')
plt.title('Fake Dark Dist')

plt.subplot(4,3,9)
plt.plot(abs_dd,color='g')
plt.title('Absolute Difference Dark')

plt.subplot(4,3,10)
plt.plot(bd,color='r')
plt.title('Real Bright Dist')

plt.subplot(4,3,11)
plt.plot(fbd,color='b')
plt.title('Fake Bright Dist')

plt.subplot(4,3,12)
plt.plot(abs_bd,color='g')
plt.title('Absolute Difference Bright')

plt.show()