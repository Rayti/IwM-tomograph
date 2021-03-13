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

def nextPosition(previousPosition, origin, alpha):
    alpha = alpha * math.pi / 180 #changing grades to radians
    x0 = previousPosition[0]
    y0 = previousPosition[1]
    xOrigin = origin[0]
    yOrigin = origin[1]
    x1 = round(xOrigin + (x0 - xOrigin) * math.cos(alpha) - (y0 - yOrigin) * math.sin(alpha))
    y1 = round(yOrigin + (x0 - xOrigin) * math.sin(alpha) + (y0 - yOrigin) * math.cos(alpha))
    return [x1, y1]

def generate(n, spread, img):
    detectors = []
    origin = [(len(img[0]) - 1)/2, (len(img) - 1)/2]
    alpha = spread / n
    seedPosition = [len(img[0]), 0] #right top image corner
    emitter = nextPosition([len(img[0]) - 1, 0], origin, 360 - 45) #middle top above image
    for i in range(n):
        detectors.append(nextPosition(emitter, origin, 180-(alpha*n)/2+alpha*i))
    return emitter, detectors

def reposition(emitter, detectors, alpha, img):
    origin = [(len(img[0]) - 1)/2, (len(img) - 1)/2]
    emitter = nextPosition(emitter, origin, alpha)
    for i in range(len(detectors)):
        detectors[i] = nextPosition(detectors[i], origin, alpha)
    return emitter, detectors

def scanOneLine(emitter, detector, img):
    scanned = 0
    posToScan = bresenham(emitter, detector, img)
    for i in posToScan:
        if isWithinImageBoundaries(i, img):
            scanned += img[i[1]][i[0]]
    return scanned

#skip - delta grades to rotate each time       
def genSinogram(emitter, detectors, skip, img, nProgress):
    progressBar = st.progress(0)
    if nProgress == 0:#avoiding devision by modulo 0 error
        nProgress = 1
    iterations = round(360/skip)
    sinogram = []
    progressSinogram = np.zeros([round(360/skip), len(detectors)])
    stImg = st.empty()
    for i in range(iterations):
        progressBar.progress(round((100/iterations)*(i+1)))
        sinogram.append([])
        for j in range(len(detectors)):
            sinogram[i].append(scanOneLine(emitter, detectors[j], img))
        emitter, detectors = reposition(emitter, detectors, skip, img)
        #fill progressSinogram
        if (i+1) % nProgress == 0:
            for ik in range(len(sinogram)):
                for jk in range(len(sinogram[0])):
                    progressSinogram[ik][jk] = sinogram[ik][jk]
            progressSinogram /= progressSinogram.max()
            stImg.image(progressSinogram)
    sinogram = np.asarray(sinogram)
    stImg.image(sinogram/sinogram.max())
    return sinogram/sinogram.max()

def reconstructImage(sinogram, emitter, detectors, skip, imgHeight, imgWidth, nProgress):
    progressBar = st.progress(0)
    stImg = st.empty()
    if nProgress == 0: #avoiding devision by modulo 0 error
        nProgress = 1
    recImg = np.zeros([imgHeight, imgWidth])
    i = 0
    for sinLine in sinogram:
        i += 1
        progressBar.progress(round(100/(len(sinogram)/i)))
        reconstructLines(sinLine, emitter, detectors, recImg)
        emitter, detectors = reposition(emitter, detectors, skip, recImg) 
        if i % nProgress == 0:
            progressRecImg = recImg/recImg.max()
            stImg.image(progressRecImg)
    stImg.image(recImg/recImg.max())
    return recImg/recImg.max()

def reconstructLines(sinogramLine, emitter, detectors, recImg):
    for i in range(len(detectors)):
        reconstructOneLine(sinogramLine[i], emitter, detectors[i], recImg)

def reconstructOneLine(value, emitter, detector, recImg):
    positions = bresenham(emitter, detector, recImg)
    for pos in positions:
        if isWithinImageBoundaries(pos, recImg):
            recImg[pos[1]][pos[0]] += value

        
            
