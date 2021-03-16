import streamlit as st
import numpy as np
import math
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from skimage import color
from skimage import io
from PIL import Image as im

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
    #for i in range(len(filteredSinogram)):
        #for j in range(len(filteredSinogram[i])):
            #if filteredSinogram[i][j] < 0:
                #filteredSinogram[i][j] /= 10
    filteredSinogram = (filteredSinogram - filteredSinogram.min())/(filteredSinogram.max() - filteredSinogram.min())
    
    fig, ax = plt.subplots()
    ax.plot(range(len(filteredSinogram[0])), filteredSinogram[0], color="green", lw=2)
    plt.savefig("filter_line_normalized.png");
        
    return filteredSinogram#/filteredSinogram.max()
        
