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



nDetectors = st.sidebar.slider('Amount of detectors', min_value = 1, max_value = 1000, value = 100)
deltaAlpha = st.sidebar.slider('Grade to rotate in each iteration', min_value = 1, max_value = 360, value = 20)
spreadDetectors = st.sidebar.slider('Spread of detectors', min_value = 1, max_value = 360, value = 180)
st.write(spreadDetectors)
selectImg = st.sidebar.selectbox(
    'Choose image from subdirectory',
    ('./tomograf-zdjecia/CT_ScoutView.jpg','./tomograf-zdjecia/SADDLE_PE.JPG', './tomograf-zdjecia/Kwadraty2.jpg', './tomograf-zdjecia/Kropka.jpg'))
nProgress = st.sidebar.slider('Show progress every n roations', min_value = 1, max_value = round(360/deltaAlpha), value = round((360/deltaAlpha)/3))
st.sidebar.write("Selected image")
st.sidebar.image(loadImage(selectImg))

if st.sidebar.button('Execute'):
    img = loadImage(selectImg)
    emitter, detectors = generate(nDetectors, deltaAlpha, img)
    sinogram = genSinogram(emitter, detectors, spreadDetectors, deltaAlpha, img, nProgress)
    st.write("Completed sinogram")
    st.image(sinogram)
    
    reconstructedImage = reconstructImage(sinogram, emitter, detectors, deltaAlpha, len(img), len(img[0]), nProgress)
    st.write("Reconstructed image")
    st.image(reconstructedImage)
    
    
if st.button('add'):
    result = 1 + 2
    st.write('result: %s' % result)

st.write("""
    # My first app
    Hello *world!*
    """)

#st.image(loadImage(path))
