import numpy as np
import sys
import os
import nibabel as nib

arg1 = sys.argv[1] #input file
arg2 = np.float64(sys.argv[2]) #TR
arg3 = np.float64(sys.argv[3]) #target time
arg4 = sys.argv[4] #slicetimefile
arg5 = sys.argv[5] #output

temp = open(arg4, 'r')
seq = []
for z in temp:
    seq.append(np.float64(z[:-1]))
    if(np.float64(z[:-2])>arg2):
        temp = open(arg5+'.txt', 'w')
        temp.write("FAILURE")
        temp.close()
        exit()

def interpolate(givenX, givenY, changeX):
	changeY = []
	if(changeX[0]<givenX[0]):
		changeY.append(givenY[0]) #nearest neighbour for extremes
		for i in range(len(givenX)-1):
			slope = (givenY[i+1]-givenY[i])/(givenX[i+1]-givenX[i])*1.0
			temp = slope*(changeX[i+1]-givenX[i]) + givenY[i]
			changeY.append(temp)
		changeY[-1] = givenY[-1]
		return np.array(changeY).astype(np.float64)
	else:
		changeY.append(givenY[0])
		for i in range(1, len(givenX)-1, 1):
			slope = (givenY[i+1]-givenY[i])/(givenX[i+1]-givenX[i])*1.0
			temp = slope*(changeX[i]-givenX[i]) + givenY[i]
			changeY.append(temp)
		changeY.append(givenY[-1])
		return np.array(changeY).astype(np.float64)

obj = nib.loadsave.load(arg1)
image = nib.loadsave.read_img_data(obj)
vox_x = image.shape[0]
vox_y = image.shape[1]
vox_z = image.shape[2]
vols = image.shape[3]
vol_times = (np.arange(vols)*arg2).astype(np.float64)

correctedImage = np.ones(shape = image.shape)

for x in range(vox_x):
    for y in range(vox_y):
        for z in range(vox_z):
            timeSeries = image[x, y, z, :].astype(np.float64)
            ztime = seq[z]
            acqtimes = (vol_times+ztime).astype(np.float64)
            targetTimes = (vol_times+arg3).astype(np.float64)
            temp = interpolate(acqtimes, timeSeries, targetTimes)
            correctedImage[x, y, z, :] = np.reshape(temp, newshape=(1, 1, 1, vols)).astype(np.float64)

temp = open(arg5+'.txt', 'w')
temp.write("SUCCESS")
temp.close()
# np.save('wtf.npy', correctedImage)
correctedHeader=obj.header.copy()
correctedObject = nib.nifti1.Nifti1Image(correctedImage,  np.eye(4))
nib.loadsave.save(correctedObject, arg5+'.nii.gz')
