import streamlit as st
import numpy as np
import math
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from skimage import color
from skimage import io

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
    return kernel

def filterLine(sinogramLine, kernel):
    line = np.convolve(sinogramLine, kernel, mode='same')
    return line

def filterSinogram(sinogram, kernel):
    filteredSinogram = np.zeros(sinogram.shape)
    for i in range(len(filteredSinogram)):
        filteredSinogram[i] = filterLine(sinogram[i], kernel)
    return filteredSinogram
        
