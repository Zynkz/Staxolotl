from astropy.io import fits
from astropy.visualization import astropy_mpl_style
import matplotlib.pyplot as plt
from astropy.utils.data import get_pkg_data_filename
import cv2
import numpy as np
import os
import sys
from tqdm import tqdm
import matplotlib.pyplot as plt
from skimage.registration import phase_cross_correlation
from scipy.ndimage import fourier_shift

def load_image(image_name):
    image_file = get_pkg_data_filename(image_name)
    image_data = fits.getdata(image_file, ext=0)
    numpy_data = np.array(image_data)
    return numpy_data

def save_image(numpy_data, image_name):
    file_out = fits.PrimaryHDU(numpy_data)
    file_out1 = fits.HDUList(file_out)
    file_out1.writeto(image_name, overwrite=True)

def point_spread(image):
    K = 4.0
    F = 4.0
    
    # PSF = np.array([[-K/F, -K/F, -K/F],[-K/F, K+1.0, -K/F],[-K/F, -K/F, -K/F]])
    PSF = np.array([[0, -K/F, 0],[-K/F, K+1.0, -K/F],[0, -K/F, 0]])
    # PSF = np.array([[0, -1, 0],[-1, 5, -1],[0, -1, 0]])
    # PSF = np.array([[1,1,1],[1,-8,1],[1,1,1]]) #laplace   ?

    print(PSF)
    print(image)

    height = len(image)
    width = len(image[0])
    output = image
    midpoint = [height//2, width//2]

    # image.flatten()

    for i in range(1, height-1):
        for j in range(1,width-1):

    # for i in range(midpoint[0], height-1):
    #     for j in range(midpoint[1], width-1):
            
            temp = 0.0
            temp += PSF[0][0] * image[i-1][j-1]
            temp += PSF[0][1] * image[i-1][j]
            temp += PSF[0][2] * image[i-1][j+1]
            temp += PSF[1][0] * image[i][j-1]
            temp += PSF[1][1] * image[i][j]
            temp += PSF[1][2] * image[i][j+1]
            temp += PSF[2][0] * image[i+1][j-1]
            temp += PSF[2][1] * image[i+1][j]
            temp += PSF[2][2] * image[i+1][j+1]
            if temp < np.iinfo(np.uint16).min:
                temp = np.iinfo(np.uint16).min
            if temp > np.iinfo(np.uint16).max:
                temp = np.iinfo(np.uint16).max
            output[i][j] = np.uint16(temp)

    return output
    
            






def main():

    original_image = load_image("./moon_test/Moon_00001.fits")
    k = 3.0
    f = 7.0
    # kernel = np.array([[-k/f, -k/f, -k/f],[-k/f, k+1.0, -k/f],[-k/f, -k/f, -k/f]])
    # kernel = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]) #laplace?

    # original_kernel_image = cv2.filter2D(original_image, -1, kernel)
    # save_image(original_kernel_image, "./output/original_kernel_image.fits")

    # mean_image = load_image("./output/moon_1753_1.fits")
    # mean_image = np.fft.fftn(mean_image)

    # kernel_image = cv2.filter2D(mean_image.real, -1, kernel)
    # kernel_image = np.fft.ifftn(kernel_image)
    # kernel_image = np.uint16(kernel_image.real)

    # save_image(kernel_image, "./output/moon_1753_1_kernel.fits")
    
    # laplace_image = cv2.Laplacian(mean_image, -1, cv2.CV_64F)
    # save_image(laplace_image, "./output/moon_1753_1_laplace.fits")

    # final_laplace_image = mean_image + laplace_image
    # save_image(final_laplace_image, "./output/final_laplace_image.fits")
    
    # final_kernel_image = mean_image - kernel_image
    # save_image(final_kernel_image, "./output/final_kernel_image.fits")

    input_image = load_image("./output/moon_1753_1.fits")
    # input_image = load_image("./moon_test/Moon_00001.fits")

    # input_image = np.fft.fftn(input_image)
    psf_image = point_spread(input_image)
    # psf_image = input_image+psf_image
    # psf_image = np.fft.ifftn(psf_image)
    # psf_image = np.uint16(psf_image.real)
    save_image(psf_image, "./output/psf_image.fits")

if __name__=="__main__":
    main()