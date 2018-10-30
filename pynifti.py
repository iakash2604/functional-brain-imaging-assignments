import numpy as np
import sys
import nibabel

a = "path/to/file"

temp = nibabel.loadsave.load(a)
image = nibabel.loadsave.read_img_data(temp)

"""
image is the 4D fMRI data. (x, y, z, t). 
"""

