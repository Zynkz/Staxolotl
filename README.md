# Staxolotl
## Release Notes
### Version 1.0.0
- First release of Staxolotl
  - Staxolotl was created to help hobbyist astrophotographers improve the quality of their images
  - Compatible with the FITS image format
  - Allows you to open all images within a folder
  - Image set can be reduced to a smaller size by using sigma clipping
    - grades the sharpness of each image
    - Take images within one standard deviation from the mean sharpness
  - Reference image is defined as the current image in the display
    - An alignment point can be place on the images
    - A radius can be selected which will be  the reference frame for alignment
    - Alignment is done with a Fourier transform and cross phase correlation
  - Images can be stacked using mean stacking
    - Takes the average pixel intensity
  - Image sharpening is being done with a point spread function and a sharpening filter
- Known issues
  - Switching images in the image viewer will cause the alignment point to disappear but the data point is still recorded
  - When saving an image, it will automatically change the working directory to the saved image but if you don't save the image, it won't restore the old working directory
