import streamlit as st
import numpy as np
import math
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from skimage import color
from skimage import io
from PIL import Image as im
from core_functions import *
from positioning import *
from cone_positioning import *
    
#skip - skok czyli ilość stopni do obrócenia 'głowicy' z emiterami/detektorami           
def generateSinogram(skip, emitters, detectors, img):
    #ilosc iteracji
    n = round(360/skip)
    
    sinogram = []
    for i in range(n):
        sinogram.append([])
        for j in range(len(emitters)):
            sinogram[i].append(scanOneLine(emitters[j], detectors[j], img))
        repositionEmittersAndDetectors(emitters, detectors, skip ,img)
    sinogram = np.asarray(sinogram)
    return sinogram/sinogram.max()
       
def reconstructLines(sinogramLine, emitters, detectors, recImg):
    for i in range(len(emitters)):
        posToFill = bresenham(emitters[i], detectors[i], recImg)
        for j in range(len(posToFill)):
            if posToFill[j][0] < len(recImg[0]) and posToFill[j][0] >= 0 and posToFill[j][1] < len(recImg) and posToFill[j][1] >= 0:
                xToFill = posToFill[j][0]
                yToFill = posToFill[j][1]
                recImg[yToFill][xToFill] += sinogramLine[i]

def reconstructImage(sinogram, skip, emitters, detectors, img, filtered=False):
    imgLength = len(img[0])
    imgHeight = len(img)
    
    reconstructedImage = np.zeros([imgHeight, imgLength])
    n = round(360/skip)
    for i in range(len(sinogram)):
        reconstructLines(sinogram[i], emitters, detectors, reconstructedImage)
        repositionEmittersAndDetectors(emitters, detectors, skip, img)
    if filtered == True:
        for i in range(len(reconstructedImage)):
            for j in range(len(reconstructedImage[0])):
                if reconstructedImage[i][j] > 1:
                    reconstructedImage[i][j] = 1
    else:
        reconstructedImage /= reconstructedImage.max()
    #for i in range(len(reconstructedImage)):
        #np.convolve(reconstructedImage[i, :], 21, mode='same')
    return reconstructedImage

def generateKernel(size):
    kernel = []
    for k in range(-size//2, size//2):
        if k == 0:
            kernel.append(1)
        else:
            if k % 2 == 0:
                kernel.append(0)
            if k % 2 == 1:
                kernel.append((-4/(math.pi**2))/k**2)
    fig, ax = plt.subplots()
    ax.plot(range(-size//2, size//2), kernel, color="green", lw=2)
    plt.savefig("kernel_plot.png");
    return kernel

def filterLine(sinogramLine, kernel):
    line = np.convolve(sinogramLine, kernel, mode='same')
    return line

def filterSinogram(sinogram, kernel):
    filteredSinogram = np.zeros(sinogram.shape)
    
    for i in range(len(filteredSinogram)):
        filteredSinogram[i] = filterLine(sinogram[i], kernel)
        if i == 0:
            fig, ax = plt.subplots()
            ax.plot(range(len(filteredSinogram[i])), filteredSinogram[i], color="blue", lw=2)
            plt.savefig("filter_line.png");
        
            fig, ax = plt.subplots()
            ax.plot(range(len(sinogram[i])), sinogram[i], color="red", lw=2)
            plt.savefig("line.png");
#    for i in range(len(filteredSinogram)):
#        for j in range(len(filteredSinogram[i])):
#            if filteredSinogram[i][j] < 0:
#                filteredSinogram[i][j] /= 10
    filteredSinogram = (filteredSinogram - filteredSinogram.min())/(filteredSinogram.max() - filteredSinogram.min())
    
    return filteredSinogram#/filteredSinogram.max()
        

##########################MAIN

img = loadImage('./tomograf-zdjecia/Shepp_logan.jpg')
n = 180
skip = 4
spread = 40
kernelSize = 40
#emitters, detectors = generateEmittersAndDetectors(n, spread, img)
#sinogram = generateSinogram(skip, emitters, detectors, img)
#reconstructedImage = reconstructImage(sinogram, skip, emitters, detectors, img)
#kernel = generateKernel(kernelSize)
#filteredSinogram = filterSinogram(sinogram, kernel)
#filteredSinogram /= filteredSinogram.max()
#for i in range(len(filteredSinogram)):
#    for j in range(len(filteredSinogram[i])):
#        if filteredSinogram[i][j] < 0:
#            filteredSinogram[i][j] /= 15
#filteredSinogram = (filteredSinogram - filteredSinogram.min())/(filteredSinogram.max() - #filteredSinogram.min())

#fig, ax = plt.subplots()
#ax.plot(range(len(filteredSinogram[0])), filteredSinogram[0], color="black", lw=2)
#plt.savefig("filter_line_after_normalization.png");

#filteredSinogram /= filteredSinogram.max()
#reconstructedFilteredImage = reconstructImage(filteredSinogram, skip, emitters, detectors, img, filtered=False)




#--------------------------------------------------------------
fig, ax = plt.subplots()
ax.imshow(img)


# Add plot on the image.
#px = [i[0] for i in emitters]
#py = [i[1] for i in emitters]
#bres = []
#for i in range(len(emitters)):
#    bres.append(bresenham(emitters[i], detectors[i], img))
#    
#for i in range(len(bres)):
#    bresX = [i[0] for i in bres[i]]
#    bresY = [i[1] for i in bres[i]]
#    ax.plot(bresX, bresY, color="red", linewidth = 1)


#pxD = [i[0] for i in detectors]
#pyD = [i[1] for i in detectors]
#ax.plot(px,py,color="yellow",lw=3)
#ax.plot(pxD, pyD, color="blue", lw=3)

#CONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONE
emitterCone, detectorsCone = generate(n, spread, img)
pxCone = [i[0] for i in detectorsCone]
pyCone = [i[1] for i in detectorsCone]
pxCone.append(emitterCone[0])
pyCone.append(emitterCone[1])
ax.plot(pxCone, pyCone, 'o', color="green", lw = 2)
sinogramCone = genSinogram(emitterCone, detectorsCone, spread, skip, img)
filteredSinogram = filterSinogram(sinogramCone, generateKernel(kernelSize))
#print(filteredSinogram)
recImgCone = reconstructImageC(sinogramCone, emitterCone, detectorsCone, skip,  len(img), len(img[0]))
#CONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONE


# Save figure.
plt.savefig("img_plot.png",bbox_inches="tight",pad_inches=0.02,dpi=250)
plt.show()

#--------------------------------------------------------------

#st.image(sinogram, width=200)
st.image(sinogramCone, width=200)
st.image(filteredSinogram, width=200)
#st.image(reconstructedImage)
#st.image(reconstructedFilteredImage)
st.image(recImgCone)


st.write("""
    # My first app
    Hello *world!*
    """)

st.image(loadImage('./tomograf-zdjecia/Shepp_logan.jpg'))
