# 1. Spatial Smoothing
* Framewise gaussian blurring has been done to smooth the fMRI image. This improves the SNR of the data.  
* Upon experimentation it was found most suitable to perform the gaussian blurring in time domain by convolving with a gaussian kernel, rather than a fft -> multiply -> ifft. 

# 2. Temporal Filtering 
* Filtering of voxel wise time series data to eliminate low frequency noise. Removes undesirable artifacts from signal. 
* fft is applied and low frequency components are removed in the frequency domian. ifft is applied to obtain the desired signal. 

## Dependencies 
1. python 2.7
2. nibabel 2.3.1

To install nibabel just run pip install nibabel


