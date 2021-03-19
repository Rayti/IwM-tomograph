import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import ExplicitVRLittleEndian
import pydicom._storage_sopclass_uids
import numpy as np

def createDicomFile(img, filename, patientId, patientName, inspectionDate, comment):

    for i in range(len(img)):
        for j in range(len(img[0])):
            img[i][j] = round(img[i][j]*255)
    
    image2d = img.astype(np.uint16)
    meta = pydicom.Dataset()
    meta.MediaStorageSOPClassUID = pydicom._storage_sopclass_uids.MRImageStorage
    meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian  
    ds = Dataset()
    ds.file_meta = meta
    ds.is_little_endian = True
    ds.is_implicit_VR = False
    ds.SOPClassUID = pydicom._storage_sopclass_uids.MRImageStorage
    ds.PatientName = patientName
    ds.PatientID = patientId
    ds.ContentDate = inspectionDate
    ds.Modality = "MR"
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.FrameOfReferenceUID = pydicom.uid.generate_uid()
    ds.BitsStored = 16
    ds.BitsAllocated = 16
    ds.SamplesPerPixel = 1
    ds.HighBit = 15
    ds.ImagesInAcquisition = "1"
    ds.Rows = image2d.shape[0]
    ds.Columns = image2d.shape[1]
    ds.InstanceNumber = 1
    ds.ImagePositionPatient = r"0\0\1"
    ds.ImageOrientationPatient = r"1\0\0\0\-1\0"
    ds.ImageType = r"ORIGINAL\PRIMARY\AXIAL"
    ds.RescaleIntercept = "0"
    ds.RescaleSlope = "1"
    ds.PixelSpacing = r"1\1"
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelRepresentation = 1
    ds.StudyDescription = comment
    pydicom.dataset.validate_file_meta(ds.file_meta, enforce_standard=True)
    ds.PixelData = image2d.tobytes()

    ds.save_as( filename, write_like_original=False)
