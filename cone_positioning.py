import streamlit as st
import numpy as np
import math
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from skimage import color
from skimage import io
from PIL import Image as im
from core_functions import *


def isWithinImageBoundaries(position, img):
    if position[0] in range(0, len(img[0])) and position[1] in range(0, len(img[1])):
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

def genSinogram(emitter, detectors, spread, skip, img):
    iterations = round(360/skip)
    sinogram = []
    for i in range(iterations):
        sinogram.append([])
        for j in range(len(detectors)):
            sinogram[i].append(scanOneLine(emitter, detectors[j], img))
        emitter, detectors = reposition(emitter, detectors, skip, img)
    sinogram = np.asarray(sinogram)
    return sinogram/sinogram.max()

def reconstructImageC(sinogram, emitter, detectors, skip, imgHeight, imgWidth):
    recImg = np.zeros([imgHeight, imgWidth])
    for sinLine in sinogram:
        reconstructLines(sinLine, emitter, detectors, recImg)
        emitter, detectors = reposition(emitter, detectors, skip, recImg) 
#    for i in range(len(recImg)):
#        for j in range(len(recImg[i])):
#            if recImg[i][j] > 1:
#                recImg[i][j] = 1
    return recImg/recImg.max()

def reconstructLines(sinogramLine, emitter, detectors, recImg):
    for i in range(len(detectors)):
        reconstructOneLine(sinogramLine[i], emitter, detectors[i], recImg)

def reconstructOneLine(value, emitter, detector, recImg):
    positions = bresenham(emitter, detector, recImg)
    for pos in positions:
        if isWithinImageBoundaries(pos, recImg):
            recImg[pos[1]][pos[0]] += value

        
            
