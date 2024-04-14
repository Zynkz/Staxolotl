# References
# https://www.geeksforgeeks.org/how-to-iterate-through-images-in-a-folder-python/

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

# def stack(key_image, next_image):
#     width = len(key_image[0])
#     height = len(key_image)
#     size = width * height
#     for itr in range(size):
#         i = itr//width
#         j = itr%width
#         key_image[i][j] = key_image[i][j] + next_image[i][j]#//n
#     return key_image

# class Image_data:
#     data_type = None
#     key_image = None
#     image_list = None


#     def __init__(self, folder_dir, key_image_name):
#         image_list = os.listdir(folder_dir)
#         key_image = load_image(folder_dir+key_image_name)
#         data_type = type(key_image[0][0])


def load_image(image_name):
    image_file = get_pkg_data_filename(image_name)
    image_data = fits.getdata(image_file, ext=0)
    numpy_data = np.array(image_data)
    return numpy_data

def save_image(numpy_data, image_name):
    file_out = fits.PrimaryHDU(numpy_data)
    file_out1 = fits.HDUList(file_out)
    file_out1.writeto(image_name, overwrite=True)

def mean_stack(folder_dir, key_image):
    mean_image = np.array([[0 for x in range(len(key_image[0]))] for y in range(len(key_image))])
    image_list = os.listdir(folder_dir)
    num = len(image_list)
    for images in tqdm(os.listdir(folder_dir)):
        next_image = load_image(folder_dir+images)
        # next_image = image_alignment(key_image, next_image)
        next_image = image_alignment_upsample(key_image, next_image)
        mean_image = mean_image + next_image/num
    # return_image = np.fft.ifftn(mean_image)
    # print(type(return_image[0][0]))
    mean_image = np.fft.ifftn(mean_image)
    # print(type(mean_image.real))
    return np.uint16(mean_image.real)

def convolve(key_image, next_image):
    for itr from 0 to len(key_image):
        




def image_alignment(key_image, align_image):
    # key_subimg = np.array(key_image[3350:3750, 2150:2450])
    # align_subimg = np.array(align_image[3350:3750, 2150:2450])

    # key_subimg = np.array([row[3350:3750] for row in key_image[1200:1600]])
    # align_subimg = np.array([row[3350:3750] for row in align_image[1200:1600]])

    key_subimg = np.array([row[700:800] for row in key_image[700:800]])
    align_subimg = np.array([row[700:800] for row in align_image[700:800]])

    # save_image(key_subimg, "./output/key_subimg.fits")
    # save_image(align_subimg, "./output/align_subimg.fits")

    # shift, error, diffphase = phase_cross_correlation(key_subimg, align_subimg)
    # aligned_image = fourier_shift(np.fft.fftn(align_image), shift)

    shift, error, diffphase = phase_cross_correlation(key_subimg, align_subimg)
    aligned_image = fourier_shift(np.fft.fftn(align_image), shift)

    return aligned_image

def image_alignment_upsample(key_image, align_image):
    # key_subimg = np.array(key_image[3350:3750, 2150:2450])
    # align_subimg = np.array(align_image[3350:3750, 2150:2450])

    key_subimg = np.array([row[3350:3750] for row in key_image[1200:1600]])
    align_subimg = np.array([row[3350:3750] for row in align_image[1200:1600]])

    # save_image(key_subimg, "./output/key_subimg.fits")
    # save_image(align_subimg, "./output/align_subimg.fits")

    shift, error, diffphase = phase_cross_correlation(key_subimg, align_subimg, upsample_factor=100)
    # print(shift)
    aligned_image = fourier_shift(np.fft.fftn(align_image), shift)
    save_image(aligned_image.real, "./output/fourier.fits")
    # _upsampled_dft(aligned_image, )


    return aligned_image

def MTF():
    return True

def main():
    #plt.style.use(astropy_mpl_style)

    folder_dir = sys.argv[1]
    key_image = load_image(folder_dir+"Moon_00001.fits")
    
    image_list = os.listdir(folder_dir)
    image_type = type(key_image[0][0])
    print(image_type)

    print("\nMean Image:")
    mean_image = mean_stack(folder_dir, key_image)
    # stddev_image = np.sqrt(mean_image)
    # average_sd = np.sum(stddev_image)/(len(stddev_image)*len(stddev_image[0]))
    # print(average_sd)

    # output_image = np.array([[np.uint16(0) for x in range(len(key_image[0]))] for y in range(len(key_image))])

    # for images in tqdm(os.listdir(folder_dir)):
    #     next_image = load_image(folder_dir+images)
    #     next_sd = np.sum(np.sqrt(next_image))/(len(stddev_image)*len(stddev_image[0]))
    #     # print(next_sd)
    #     if next_sd < average_sd:
    #         output_image = output_image + next_image//len(image_list)

    # dst = np.fft(output_image)

    save_image(mean_image, "./output/test.fits")

if __name__=="__main__":
    main()
