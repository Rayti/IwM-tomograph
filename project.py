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
nProgress = st.sidebar.slider('Show progress every n iterations', min_value = 1, max_value = round(360/deltaAlpha), value = 1)

executionFlag = st.sidebar.radio("Reconstruction:", ("Normal", "Filtered", "Both"))

dicomFileFlag = st.sidebar.checkbox("Create DICOM file")
dicomFileName = "sample.dcm"
patientId = "123456"
patientFullName = "Teuzebiusz Buraczek"
inspectionDate = "2021/03/16"
comment = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin suscipit finibus cursus. "
if dicomFileFlag == True:
    dicomFileName = st.sidebar.text_input(label = 'Output file name:', value = "sample.dcm")
    patientId = st.sidebar.text_input(label = 'Patient ID:', value = "123456")
    patientFullName = st.sidebar.text_input(label = 'Patient full name:', value = "Teuzebiusz Buraczek")
    inspectionDate = st.sidebar.text_input(label = 'Inspection date:', value = "2021/03/16")
    comment = st.sidebar.text_area(label = 'Comment:', value = comment)
    
    
st.image(loadImage(chosenPath))
  
if st.sidebar.button('Execute'):
    img = loadImage(chosenPath)
    st.header("Sinogram")
    sinogram = genSinogram(nDetectors, spreadDetectors, deltaAlpha, img, nProgress)
    if executionFlag in ("Normal", "Both"):
        st.header("Reconstructed image (normal):")
        reconstructedImage = reconstructImage(nDetectors, spreadDetectors, deltaAlpha, sinogram, len(img), len(img[0]), nProgress)
        st.write("RMSE: ", getRMSE(img, reconstructedImage))
        if dicomFileFlag == True:
            createDicomFile(reconstructedImage, dicomFileName, patientId, patientFullName, inspectionDate, comment)
            st.write("Dicom file ", dicomFileName, " created")
    if executionFlag in ("Filtered", "Both"):
        kernel = generateKernel(22)
        filteredSinogram = filterSinogram(sinogram, kernel)
        st.header("Filtered sinogram")
        st.image((filteredSinogram - filteredSinogram.min())/(filteredSinogram.max() - filteredSinogram.min()))
        
        st.header("Reconstructed image (filtered):")
        reconstructedFilteredImage = reconstructImage(nDetectors, spreadDetectors, deltaAlpha, filteredSinogram, len(img), len(img[0]), nProgress)
        st.write("RMSE: ", getRMSE(img, reconstructedFilteredImage))
        if dicomFileFlag == True:
            createDicomFile(reconstructedFilteredImage, "filtered_" + dicomFileName, patientId, patientFullName, inspectionDate, comment)
            st.write("Dicom file ", "filtered_" + dicomFileName, " created")

st.sidebar.text(" ")
st.sidebar.text(" ")
st.sidebar.text(" ")
st.sidebar.text(" ")
st.sidebar.text("FOR TESTING PURPOSES")
if st.sidebar.button('Create file with detectors positions plotted'):
    testPositioning(nDetectors, spreadDetectors, 0, loadImage(chosenPath))
  

