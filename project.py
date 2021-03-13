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



nDetectors = st.sidebar.slider('Amount of detectors', min_value = 1, max_value = 1000)
deltaAlpha = st.sidebar.slider('Grade to rotate in each iteration', min_value = 1, max_value = 360)
spreadDetectors = st.sidebar.slider('Spread of detectors', min_value = 1, max_value = 360)
selectImg = st.sidebar.selectbox(
    'Choose image from subdirectory',
    ('./tomograf-zdjecia/CT_ScoutView.jpg','None'))
if st.sidebar.button('Create sinogram'):
    if st.sidebar.button('Reconstruct image'):
        pass
##########################MAIN
path = './tomograf-zdjecia/CT_ScoutView.jpg'
#path = './tomograf-zdjecia/SADDLE_PE.JPG'
img = loadImage(path)
n = 25
skip = 60
spread = 120
kernelSize = 20

#--------------------------------------------------------------
fig, ax = plt.subplots()
ax.imshow(img)

#CONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONE
emitterCone, detectorsCone = generate(n, spread, img)
pxCone = [i[0] for i in detectorsCone]
pyCone = [i[1] for i in detectorsCone]
pxCone.append(emitterCone[0])
pyCone.append(emitterCone[1])
ax.plot(pxCone, pyCone, 'o', color="green", lw = 2)
sinogramCone = genSinogram(emitterCone, detectorsCone, spread, skip, img)
#filteredSinogram = filterSinogram(sinogramCone, generateKernel(kernelSize))
#print(filteredSinogram)
recImgCone = reconstructImageC(sinogramCone, emitterCone, detectorsCone, skip,  len(img), len(img[0]))
#CONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONECONE


# Save figure.
plt.savefig("img_plot.png",bbox_inches="tight",pad_inches=0.02,dpi=250)
plt.show()

#--------------------------------------------------------------

st.image(sinogramCone, width=200)
#st.image(filteredSinogram, width=200)
#st.image(reconstructedImage)
#st.image(reconstructedFilteredImage)
st.image(recImgCone)

if st.button('add'):
    result = 1 + 2
    st.write('result: %s' % result)

st.write("""
    # My first app
    Hello *world!*
    """)

st.image(loadImage(path))
