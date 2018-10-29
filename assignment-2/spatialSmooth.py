import numpy as np
import nibabel as nib
import sys
# from matplotlib import pyplot as plt

arg1 = sys.argv[1]  # input file name
arg2 = np.float64(sys.argv[2])  # k mm (FWHM)
arg3 = sys.argv[3] #output file name

obj1 = nib.loadsave.load(arg1)
resolution = obj1.header['pixdim'][1:4]
rx = 3
ry = 3
rz = 3
del resolution
image1 = nib.loadsave.read_img_data(obj1)
vols = image1.shape[3]

def gaussian(x, y, z, sx, sy, sz):
    return np.exp(-(x**2/(2*sx**2) + y**2/(2*sy**2) + z**2/(2*sz**2)))

def gaussian_kernel(shape, sx, sy, sz, centering):
    kernel = np.ones(shape=shape)
    center_x = int((shape[0]-1)/2)
    center_y = int((shape[1]-1)/2)
    center_z = int((shape[2]-1)/2)
    for x in range(shape[0]):
        for y in range(shape[1]):
            for z in range(shape[2]):    
                if(centering):
                    kernel[x, y, z] = gaussian(rx*(x-center_x), ry*(y-center_y), rz*(z-center_z), sx, sy, sz)
                else:
                    kernel[x, y, z] = gaussian(rx*x, ry*y, rz*z, sx, sy, sz)
    return kernel

def convolution(image, kernel):
    
    if(len(kernel.shape)==2):
        # kernelShape = kernel.shape[0]
        tempx = int((kernel.shape[0]-1)/2)
        tempy = int((kernel.shape[1]-1)/2)
        rows = image.shape[0]
        cols = image.shape[1]
        result = np.copy(image)
        
        for x in range(tempx, rows-tempx, 1):
            for y in range(tempy, cols-tempy, 1):
                result[x, y] = np.sum(np.multiply(image[x-tempx:x+tempx+1, y-tempy:y+tempy+1], kernel))

        return result

    if(len(kernel.shape)==3):
        # kernelShape = kernel.shape[0]
        tempx = int((kernel.shape[0]-1)/2)
        tempy = int((kernel.shape[1]-1)/2)
        tempz = int((kernel.shape[2]-1)/2)
        rows = image.shape[1]
        cols = image.shape[1]
        depth = image.shape[2]
        result = np.copy(image)

        for x in range(tempx, rows-tempx, 1):
            for y in range(tempy, cols-tempy, 1):
                for z in range(tempz, depth-tempz, 1):
                    result[x, y, z] = np.sum(np.multiply(image[x-tempx:x+tempx+1, y-tempy:y+tempy+1, z-tempz:z+tempz+1], kernel))

        return result


#resolution (3, 3, 3)
sigma = arg2/2.35
sy = sigma
sz = sigma
sx = sigma

image2 = np.ones(shape=image1.shape)

"""
fourier domain 
"""
kernel = gaussian_kernel(image1[:, :, :, 0].shape, sx, sy, sz, centering=False)
kernel_fourier = np.fft.fftn(kernel, norm='ortho')
kernel_fourier = kernel_fourier/np.max(kernel_fourier) #scaling 


for i in range(vols):
    avg = np.mean(image1[..., i])
    temp1 = image1[:, :, :, i]
    temp1_fourier = np.fft.fftn(temp1)
    temp2_fourier = np.multiply(kernel_fourier, temp1_fourier)
    temp2 = np.fft.ifftn(temp2_fourier)
    image2[:, :, :, i] = temp2

"""
time domain
"""

# kernel = gaussian_kernel(shape=(7, 7, 7), sx=sx, sy=sy, sz=sz, centering=True)

# for i in range(vols):
#     image2[..., i] = convolution(image1[..., i], kernel)
#     print(vols-i)


correctedHeader=obj1.header.copy()
correctedObject = nib.nifti1.Nifti1Image(image2.astype(int),  np.eye(4))
nib.loadsave.save(correctedObject, arg3)