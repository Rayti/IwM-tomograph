import streamlit as st
import numpy as np
import math
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from skimage import color
from skimage import io
from PIL import Image as im



def loadImage(path):
    img = color.rgb2gray(io.imread(path))
    return img


#alpha in grades, detectorposition = emitorPosition with alpha + 180
def emitterPosition(previousPosition, origin, alpha, imgHeight, imgLength):
    alpha = alpha * math.pi / 180
    x0 = previousPosition[0]
    y0 = previousPosition[1]
    xOrigin = origin[0]
    yOrigin = origin[1]
    x1 = xOrigin + (x0 - xOrigin) * math.cos(alpha) - (y0 - yOrigin) * math.sin(alpha)
    y1 = yOrigin + (x0 - xOrigin) * math.sin(alpha) + (y0 - yOrigin) * math.cos(alpha)
    x1 = round(x1)
    y1 = round(y1)
    if x1 >= imgLength:
        x1 = x1 - 1
    if y1 >= imgHeight:
        y1 = y1 - 1
    #print("x1 -> ", x1)
    #print("y1 -> ", y1)
    return [x1, y1]

#n - liczbe emiterów/detektorów
#spread - rozpiętość
def generateEmittersAndDetectors(n, spread, img):
    emitters = []
    detectors = []
    origin = []
    origin.append((len(img[0]) - 1)/2)
    origin.append((len(img) - 1)/2)
    alpha = spread / n
    #seedEmitter will not be created - it's abstract point before the real first one, which will be created later with emitterPosition()
    seedEmitter = emitterPosition([(len(img[0]) - 1)/2, 0], origin, 360 - alpha, len(img[0]), len(img))
    #print(seedEmitter)
    for i in range(n):
        if i == 0:
            emitters.append(emitterPosition(seedEmitter, origin, alpha, len(img[0]), len(img)))
            detectors.append(emitterPosition(seedEmitter, origin, alpha + 180, len(img[0]), len(img)))
        else:
            emitters.append(emitterPosition(emitters[-1], origin, alpha, len(img[0]), len(img)))
            detectors.append(emitterPosition(emitters[-1], origin, alpha + 180, len(img[0]), len(img)))
    #odkomentowac aby zobaczyc w pliku jak i gdzie na okregu powstaja detectory i emitery
    #xEmit = [x[0] for x in emitters]
    #yEmit = [x[1] for x in emitters]
    #xDet = [x[0] for x in detectors]
    #yDet = [x[1] for x in detectors]
    #print(xEmit)
    #print(yEmit)
    #plt.plot(xEmit, yEmit)
    #plt.plot(xDet, yDet)
    #plt.savefig("plot.png")
    #print(emitters)
    
    detectors = detectors[::-1]
    return emitters, detectors

def repositionEmittersAndDetectors(emitters, detectors, alpha, img):
    origin = []
    origin.append((len(img[0]) - 1)/2)
    origin.append((len(img) - 1)/2)
    for i in range(len(emitters)):
        emitters[i] = emitterPosition(emitters[i], origin, alpha, len(img[0]), len(img))
        detectors[i] = emitterPosition(detectors[i], origin, alpha, len(img[0]), len(img))
    return emitters, detectors

def bresenham(p0, p1, img):
    imgLength = len(img[0])
    imgHeight = len(img)
    pts = []
    x0 = p0[0]
    y0 = p0[1]
    x1 = p1[0]
    y1 = p1[1]
    dx = abs(x1-x0)
    dy = abs(y1-y0)
    if x0 < x1:
        sx = 1
    else:
        sx = -1
    if y0 < y1:
        sy = 1
    else:
        sy = -1
    err = dx - dy
    while True:
        xAnswer = x0
        yAnswer = y0
        if xAnswer >= imgLength:
            xAnswer = imgLength - 1
        if yAnswer >= imgHeight:
            yAnswer = imgHeight - 1
        pts.append((xAnswer, yAnswer))
        if x0 == x1 and y0 == y1:
            return pts
        e2 = 2*err
        if e2 > -dy:
            err = err - dy
            x0 = x0 + sx
        if e2 < dx:
            err = err + dx
            y0 = y0 + sy

def scanOneLine(emiter, detector, img):
    scanned = 0
    posToScan = bresenham(emiter, detector, img)
    for i in posToScan:
        scanned += img[i[1]][i[0]]
    return scanned
            
#skip - skok czyli ilość stopni do obrócenia 'głowicy' z emiterami/detektorami           
def generateSinogram(skip, emitters, detectors, img):
    imgLength = len(img[0])
    imgHeight = len(img)
    
    #ilosc iteracji
    n = round(360/skip)
    
    sinogram = []
    for i in range(n):
        #print("i -> ", i)
        sinogram.append([])
        for j in range(len(emitters)):
            #print("j -> ", j)
            sinogram[i].append(scanOneLine(emitters[j], detectors[j], img))
        repositionEmittersAndDetectors(emitters, detectors, skip ,img)

    #print("sinogram line -> ", sinogram)
    sinogram = np.asarray(sinogram)
    return sinogram/sinogram.max()
       
def reconstructLines(sinogramLine, emitters, detectors, recImg):
    for i in range(len(emitters)):
        posToFill = bresenham(emitters[i], detectors[i], recImg)
        for j in range(len(posToFill)):
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
        #print("sinogram[i] -> ", sinogram[i])
        #break
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
    return filteredSinogram
        

##########################MAIN

img = loadImage('./tomograf-zdjecia/Shepp_logan.jpg')
n = 200
skip = 3
spread = 160
kernelSize = 40
emitters, detectors = generateEmittersAndDetectors(n, spread, img)
sinogram = generateSinogram(skip, emitters, detectors, img)
reconstructedImage = reconstructImage(sinogram, skip, emitters, detectors, img)
kernel = generateKernel(kernelSize)
filteredSinogram = filterSinogram(sinogram, kernel)
#filteredSinogram /= filteredSinogram.max()
for i in range(len(filteredSinogram)):
    for j in range(len(filteredSinogram[i])):
        if filteredSinogram[i][j] < 0:
            filteredSinogram[i][j] /= 5
filteredSinogram = (filteredSinogram - filteredSinogram.min())/(filteredSinogram.max() - filteredSinogram.min())

fig, ax = plt.subplots()
ax.plot(range(len(filteredSinogram[0])), filteredSinogram[0], color="black", lw=2)
plt.savefig("filter_line_after_normalization.png");

#filteredSinogram /= filteredSinogram.max()
reconstructedFilteredImage = reconstructImage(filteredSinogram, skip, emitters, detectors, img, filtered=False)




#--------------------------------------------------------------
fig, ax = plt.subplots()
ax.imshow(img)


# Add plot on the image.
px = [i[0] for i in emitters]
py = [i[1] for i in emitters]
bres = []
for i in range(len(emitters)):
    bres.append(bresenham(emitters[i], detectors[i], img))
    
for i in range(len(bres)):
    bresX = [i[0] for i in bres[i]]
    bresY = [i[1] for i in bres[i]]
    ax.plot(bresX, bresY, color="red", linewidth = 1)


pxD = [i[0] for i in detectors]
pyD = [i[1] for i in detectors]
ax.plot(px,py,color="yellow",lw=3)
ax.plot(pxD, pyD, color="blue", lw=3)


# Save figure.
plt.savefig("img_plot.png",bbox_inches="tight",pad_inches=0.02,dpi=250)
plt.show()

#--------------------------------------------------------------

st.image(sinogram, width=400)
st.image(filteredSinogram, width=400)
st.image(reconstructedImage)
st.image(reconstructedFilteredImage)


st.write("""
    # My first app
    Hello *world!*
    """)

st.image(loadImage('./tomograf-zdjecia/Shepp_logan.jpg'))
