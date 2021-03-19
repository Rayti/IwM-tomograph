import streamlit as st
import numpy as np
import math
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from skimage import color
from skimage import io
from PIL import Image as im
from core_functions import *
import streamlit as st


def isWithinImageBoundaries(position, img):
    if position[0] in range(0, len(img[0])) and position[1] in range(0, len(img)):
        return True
    else:
        return False

def getPosition(seedPosition, origin, alpha):
    alpha = alpha * math.pi / 180
    x0 = seedPosition[0]
    y0 = seedPosition[1]
    xOrigin = origin[0]
    yOrigin = origin[1]
    x1 = round(xOrigin + (x0 - xOrigin) * math.cos(alpha) - (y0 - yOrigin) * math.sin(alpha))
    y1 = round(yOrigin + (x0 - xOrigin) * math.sin(alpha) + (y0 - yOrigin) * math.cos(alpha))
    return [x1, y1]

def setUpPositions(n, spread, alpha, img):
    detectors = []
    origin = [(len(img[0])-1)/2, (len(img) - 1)/2]
    seedPosition = [len(img[0]) -1 , 0] #right top image corner
    emitter = getPosition(seedPosition, origin, alpha)
    spreadAlpha = spread / n
    for i in range(n):
        detectors.append(getPosition(emitter, origin, 180 - spread/2 + spreadAlpha/2  + spreadAlpha * i  ))
    return emitter, detectors
    

def scanOneLine(emitter, detector, img):
    scanned = 0
    posToScan = bresenham(emitter, detector)
    for i in posToScan:
        if isWithinImageBoundaries(i, img):
            scanned += img[i[1]][i[0]]
    return scanned



def genSinogram(n, spread, alpha, img, nProgress):
    progressBar = st.progress(0)
    if nProgress == 0:#avoiding division by modulo 0 error
        nProgress = 1
    iterations = round(360/alpha)
    sinogram = []
    progressSinogram = np.zeros([round(360/alpha), n])
    stImg = st.empty()
    for i in range(iterations):
        emitter, detectors = setUpPositions(n, spread, alpha * i, img)
        progressBar.progress(round((100/iterations)*(i+1)))
        sinogram.append([])
        for j in range(len(detectors)):
            sinogram[i].append(scanOneLine(emitter, detectors[j], img))
        #fill progressSinogram
        if (i+1) % nProgress == 0:
            for ik in range(len(sinogram)):
                for jk in range(len(sinogram[0])):
                    progressSinogram[ik][jk] = sinogram[ik][jk]
            progressSinogram /= progressSinogram.max()
            stImg.image(progressSinogram)
    sinogram = np.asarray(sinogram)
    stImg.image(sinogram/sinogram.max())
    return sinogram


def reconstructImage(n, spread, alpha, sinogram, imgHeight, imgWidth, nProgress):
    progressBar = st.progress(0)
    stImg = st.empty()
    if nProgress == 0: #avoiding devision by modulo 0 error
        nProgress = 1
    recImg = np.zeros([imgHeight, imgWidth])
    countMatrix = np.zeros([imgHeight, imgWidth])
    i = 0
    for sinLine in sinogram:
        i += 1
        progressBar.progress(round(100/(len(sinogram)/i)))
        emitter, detectors = setUpPositions(n, spread, alpha * (i - 1), recImg)
        reconstructLines(sinLine, emitter, detectors, recImg, countMatrix)
        if i % nProgress == 0:
            progressRecImg = recImg.copy()
            for ipro in range(len(countMatrix)):
                for jpro in range(len(countMatrix[0])):
                    if countMatrix[ipro][jpro] != 0:
                        progressRecImg[ipro][jpro] /= countMatrix[ipro][jpro]
            stImg.image((progressRecImg - progressRecImg.min())/(progressRecImg.max() - progressRecImg.min()))
           
    for i in range(len(countMatrix)):
        for j in range(len(countMatrix[0])):
            if countMatrix[i][j] != 0:
                recImg[i][j] /= countMatrix[i][j]
    bottom = np.percentile(recImg, 2)
    top = np.percentile(recImg,98)
    for i in range(len(recImg)):
        for j in range(len(recImg[0])):
            if recImg[i][j] <= bottom:
                recImg[i][j] = bottom
            if recImg[i][j] >= top:
                recImg[i][j] = top
    
    recImg = (recImg - recImg.min())/(recImg.max() - recImg.min())
    
    stImg.image(recImg)
    return recImg

def reconstructLines(sinogramLine, emitter, detectors, recImg, countMatrix):
    for i in range(len(detectors)):
        reconstructOneLine(sinogramLine[i], emitter, detectors[i], recImg, countMatrix)

def reconstructOneLine(value, emitter, detector, recImg, countMatrix):
    positions = bresenham(emitter, detector)
    for pos in positions:
        if isWithinImageBoundaries(pos, recImg):
            recImg[pos[1]][pos[0]] += value
            countMatrix[pos[1]][pos[0]] +=1

    
def testPositioning(n, spread, alpha, img):
    fig, ax = plt.subplots()
    origin = [(len(img[0]) - 1)/2, (len(img) - 1)/2]
    print("imgHeight -> ", len(img))
    print("imgLength -> ", len(img[0]))
    ax.plot(origin[0], origin[1], 'o', color="black")
    emitter, detectors = setUpPositions(n, spread, alpha, img)
    ax.plot(emitter[0], emitter[1], 'o', color="red")
    for i in detectors:
        ax.plot(i[0], i[1], 'o', color="blue")
    ax.set_xlim([-200, len(img[0]) + 200])
    ax.set_ylim([-200, len(img) + 200])
    ax.axis('equal')
    plt.grid()
    plt.savefig("emitter_positions");
    
