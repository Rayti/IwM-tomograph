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
    
    return emitters, detectors

def repositionEmittersAndDetectors(emitters, detectors, alpha, img):
    origin = []
    origin.append((len(img[0]) - 1)/2)
    origin.append((len(img) - 1)/2)
    for i in range(len(emitters)):
        emitters[i] = emitterPosition(emitters[i], origin, alpha, len(img[0]), len(img))
        detectors[i] = emitterPosition(detectors[i], origin, alpha, len(img[0]), len(img))
    return emitters, detectors

def bresenham(p0, p1):
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
        pts.append((x0,y0))
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
    posToScan = bresenham(emiter, detector)
    for i in posToScan:
        if img[i[1]][i[0]] > scanned:
            scanned = img[i[1]][i[0]]
    return scanned
            
#skip - skok czyli ilość stopni do obrócenia 'głowicy' z emiterami/detektorami           
def generateSinogram(skip, emitters, detectors, img):
    imgLength = len(img[0])
    imgHeight = len(img)
    
    #ilosc iteracji
    n = round(360/skip)
    sumSkip = skip
    
    sinogram = []
    for i in range(n):
        #print("i -> ", i)
        sinogram.append([])
        for j in range(len(emitters)):
            #print("j -> ", j)
            sinogram[i].append(scanOneLine(emitters[j], detectors[j], img))
        repositionEmittersAndDetectors(emitters, detectors, sumSkip ,img)
        sumSkip += skip

    #print("sinogram line -> ", sinogram)
    return sinogram


##########################MAIN

img = loadImage('./tomograf-zdjecia/Kropka.jpg')

emitters, detectors = generateEmittersAndDetectors(90, 180, img)
sinogram = generateSinogram(60, emitters, detectors, img)

arr = np.asarray(sinogram)
#sinogramImg = im.fromarray(np.array(sinogram))
#print("bresenham --> ", emitters[1], "; ", detectors[1])
#print(bresenham(emitters[1], detectors[1]))
st.image(arr)

st.write("""
    # My first app
    Hello *world!*
    """)

st.image(loadImage('./tomograf-zdjecia/Kropka.jpg'))