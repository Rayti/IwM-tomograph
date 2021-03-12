import streamlit as st
import numpy as np
import math
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from skimage import color
from skimage import io
from PIL import Image as im


#alpha in grades, detectorposition = emitorPosition with alpha + 180
def emitterPosition(previousPosition, origin, alpha):
    alpha = alpha * math.pi / 180
    x0 = previousPosition[0]
    y0 = previousPosition[1]
    xOrigin = origin[0]
    yOrigin = origin[1]
    x1 = round(xOrigin + (x0 - xOrigin) * math.cos(alpha) - (y0 - yOrigin) * math.sin(alpha))
    y1 = round(yOrigin + (x0 - xOrigin) * math.sin(alpha) + (y0 - yOrigin) * math.cos(alpha))
    return [x1, y1]


#n - liczbe emiterów/detektorów
#spread - rozpiętość
def generateEmittersAndDetectors(n, spread, img):
    emitters = []
    detectors = []
    origin = [(len(img[0]) - 1)/2, (len(img) - 1)/2]
    alpha = spread / n
    #seedEmitter will not be created - it's abstract point before the real first one, which will be created later and added to list of emitters/detectors
    seedEmitter = emitterPosition([len(img[0]) - 1, 0], origin, 360 - alpha)
    emitters.append(emitterPosition(seedEmitter, origin, alpha))
    detectors.append(emitterPosition(seedEmitter, origin, alpha + 180))
    for i in range(n - 1):
        emitters.append(emitterPosition(emitters[-1], origin, alpha))
        detectors.append(emitterPosition(detectors[-1], origin, alpha))
    detectors = detectors[::-1]
    return emitters, detectors

def repositionEmittersAndDetectors(emitters, detectors, alpha, img):
    origin = [(len(img[0]) - 1)/2, (len(img) - 1)/2]
    for i in range(len(emitters)):
        emitters[i] = emitterPosition(emitters[i], origin, alpha)
        detectors[i] = emitterPosition(detectors[i], origin, alpha)
    return emitters, detectors
