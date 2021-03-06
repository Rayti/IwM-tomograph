import streamlit as st
import numpy as np
import math
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from skimage import color
from skimage import io
from PIL import Image as im
import pydicom
import os
import tempfile
import datetime
from pydicom.dataset import Dataset, FileDataset, FileMetaDataset


def loadImage(path):
    img = color.rgb2gray(io.imread(path))
    return img

def bresenham(p0, p1, img):
    imgLength = len(img[0])
    imgHeight = len(img)
    pts = []
    x0 = p0[0]
    y0 = p0[1]
    x1 = p1[0]
    y1 = p1[1]
    dx = abs(x1-x0)
    dy = abs(y1-y0)
    if x0 < x1:
        sx = 1
    else:
        sx = -1
    if y0 < y1:
        sy = 1
    else:
        sy = -1
    err = dx - dy
    while True:
        pts.append((x0, y0))
        if x0 == x1 and y0 == y1:
            return pts
        e2 = 2*err
        if e2 > -dy:
            err = err - dy
            x0 = x0 + sx
        if e2 < dx:
            err = err + dx
            y0 = y0 + sy
        
def createDicomFile(img, patientName, patientId):
    fileMeta = FileMetaDataset()
    fileMeta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
    fileMeta.MediaStorageSOPInstanceUID = "1.2.3"
    fileMeta.ImplementationClassUID = "1.2.3.4"
    
    fileNameLittleEndian = tempfile.NamedTemporaryFile(suffix='.dcm').name
    fileNameBigEndian = tempfile.NamedTemporaryFile(suffix='.dcm').name
    
    ds = FileDataset(fileNameLittleEndian, {}, file_meta=fileMeta, preamble=b"\0" * 128)
    ds.PatientName = patientName
    ds.PatientID = patientId
    
    ds.is_little_endian = True
    ds.is_implicit_VR = True
    
    dt = datetime.datetime.now()
    ds.ContentDate = dt.strftime('%Y%m%d')
    timeStr = dt.strftime('%H%M%S.%f')
    ds.ContentTime = timeStr
    pd = img * 255.0/img.max()
    #ds.PixelData = pd.tobytes()
    #ds.Rows, ds.Columns = img.shape
    
    dss = pydicom.dcmread("sample.dcm")
    arr = dss.pixel_array
    
    #tmp = np.full((200, 200), 220)
    ds.PixelData = arr
    ds.Rows, ds.Columns = arr.shape
    
    ds.save_as("dicomFile.dcm",  write_like_original=False)
    
    ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRBigEndian
    ds.is_little_endian = False
    ds.is_implicit_VR = False
    #ds.save_as("secondDicomFile.dcm", write_like_original=False)
    
    #arr[arr < 100] = 0
    dss.PixelData = arr
    dss.Rows, dss.Columns = arr.shape
    dss.save_as("sample2.dcm")
    #for i in range(len(dss.pixel_array)):
    #    for j in range(len(dss.pixel_array[0])):
    #        if dss.pixel_array[i][j] > mx :
    #            mx = dss.pixel_array[i][j]
    #            
    #print(mx)
    #print(dss.pixel_array[0])
    #print(img)
    
    
    
