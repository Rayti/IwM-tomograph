#Authors:
#Miłosz Karłowicz
#Daniel Kotyński
import streamlit as st
import numpy as np
import math
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from skimage import color
from skimage import io
from PIL import Image as im
from core_functions import *
from cone_positioning import *
from filtering import *
from glob import glob
import pydicom


st.title("Tomograph simulation")
files = glob("./tomograf-zdjecia/*")
files = [f[19:] for f in files]
nDetectors = st.sidebar.slider('Amount of detectors', min_value = 1, max_value = 1000, value = 100)
deltaAlpha = st.sidebar.slider('Grades to rotate in each iteration', min_value = 1, max_value = 45, value = 10)
spreadDetectors = st.sidebar.slider('Spread of detectors', min_value = 1, max_value = 360, value = 180)
selectImg = st.sidebar.selectbox('Choose image from subdirectory', files)
chosenPath = "./tomograf-zdjecia/" + selectImg
nProgress = st.sidebar.slider('Show progress every n rotations', min_value = 1, max_value = round(360/deltaAlpha), value = 1)
dicomFileFlag = st.sidebar.checkbox("Create DICOM file")
filterFlag = st.sidebar.checkbox("With filtering")
st.image(loadImage(chosenPath))

if st.sidebar.button('Test'):
    testPositioning(loadImage(chosenPath))

if st.sidebar.button('Execute'):
    img = loadImage(chosenPath)
    emitter, detectors = generate(nDetectors, spreadDetectors, img)
    st.write("Sinogram")
    sinogram = genSinogram(emitter, detectors, deltaAlpha, img, nProgress)
    if filterFlag == True:
        kernel = generateKernel(nDetectors)
        sinogram = filterSinogram(sinogram, kernel)
        st.write("Filtered sinogram")
        st.image(sinogram)
    st.write("Reconstructed image")
    emitter, detectors = generate(nDetectors, spreadDetectors, img)
    reconstructedImage = reconstructImage(sinogram, emitter, detectors, deltaAlpha, len(img), len(img[0]), nProgress)
    if dicomFileFlag == True:
        createDicomFile(reconstructedImage, "Patient", "1.2.34.5")
