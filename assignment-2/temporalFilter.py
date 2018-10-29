import numpy as np
import nibabel as nib
import sys

arg1 = sys.argv[1]  # input file name
arg2 = np.float64(sys.argv[2])  # TR time
arg3 = np.float64(sys.argv[3])  # Cutoff time, C
arg4 = sys.argv[4]  # output file name

def createGaussianTimeVector(t, sigma, tr):
	timeVector = []
	for i in range(t):
		time = i*tr
		timeVector.append(np.exp(-time**2/(2*sigma**2)))
	return np.array(timeVector)


obj1 = nib.loadsave.load(arg1)
image1 = nib.loadsave.read_img_data(obj1)
image2 = np.ones(shape = image1.shape)

sigma = arg3/2


x = image1.shape[0]
y = image1.shape[1]
z = image1.shape[2]
vols = image1.shape[3]
timeVector = np.fft.fft(createGaussianTimeVector(vols, sigma, arg2), norm='ortho')
timeVector = timeVector/np.max(timeVector)

for i in range(x):
	for j in range(y):
		for k in range(z):
			timeSeries = image1[i, j, k, :]
			dc = np.mean(timeSeries)
			# temp = np.fft.fft(timeSeries-dc) 
			temp = np.fft.fft(timeSeries)		#subtracting dc from timeseries doesnt make a difference
			temp_lowfreq = np.multiply(temp, timeVector)
			temp_highfreq = temp - temp_lowfreq
			# temp[1:vols] = 0
			temp = np.fft.ifft(temp_highfreq)
			image2[i, j, k, :] = temp + dc

correctedHeader=obj1.header.copy()
correctedObject = nib.nifti1.Nifti1Image(image2,  np.eye(4))
nib.loadsave.save(correctedObject, arg4)


