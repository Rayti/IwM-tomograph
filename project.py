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
from dicom_file_creator import *
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

filterFlag = st.sidebar.checkbox("With filtering")

dicomFileFlag = st.sidebar.checkbox("Create DICOM file")
dicomFileName = "sample.dcm"
patientId = "123456"
patientFullName = "Teuzebiusz Buraczek"
inspectionDate = "2021/03/16"
if dicomFileFlag == True:
    dicomFileName = st.sidebar.text_input(label = 'Output file name:', value = "sample.dcm")
    patientId = st.sidebar.text_input(label = 'Patient ID:', value = "123456")
    patientFullName = st.sidebar.text_input(label = 'Patient full name:', value = "Teuzebiusz Buraczek")
    inspectionDate = st.sidebar.text_input(label = 'Inspection date:', value = "2021/03/16")
    
    
st.image(loadImage(chosenPath))

if st.sidebar.button('Test'):
    testPositioning(nDetectors, spreadDetectors, 0, loadImage(chosenPath))
    
if st.sidebar.button('Execute'):
    img = loadImage(chosenPath)
    st.write("Sinogram")
    sinogram = genSinogram(nDetectors, spreadDetectors, deltaAlpha, img, nProgress)
    if filterFlag == True:
        kernel = generateKernel(nDetectors)#(nDetectors % 30 + 21)
        sinogram = filterSinogram(sinogram, kernel)
        st.write("Filtered sinogram")
        st.image((sinogram - sinogram.min())/(sinogram.max() - sinogram.min()))
    st.write("Reconstructed image")
    reconstructedImage = reconstructImage(nDetectors, spreadDetectors, deltaAlpha, sinogram, len(img), len(img[0]), nProgress)
    if dicomFileFlag == True:
        createDicomFile(reconstructedImage, dicomFileName, patientId, patientFullName, inspectionDate)
        st.write("Dicom file ", dicomFileName, " created")

