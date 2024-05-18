# References
# Sam Siewert - sharpen.c
# ChatGPT 3.5 - Graphic User Interface

import os

import tkinter as tk
from tkinter import filedialog

import numpy as np
import cv2

from astropy.io import fits
from astropy.visualization import astropy_mpl_style
from astropy.utils.data import get_pkg_data_filename

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from skimage.registration import phase_cross_correlation
from scipy.ndimage import fourier_shift

from tqdm import tqdm

class Staxolotl:
    def __init__(self, parent):
        self.parent = parent
        self.image_paths = []
        self.current_index = 0
        self.points = []
        self.canvas = None
        self.dots = []
        self.clip_list = []
        self.ap = []
        self.key_image_path = None
        self.output_image = []
        self.ap_radius = tk.IntVar()
        self.ap_radius.set(50)
        self.downscale_factor = 0.2

        # Initialize and configure the main window
        self.parent.title("Staxolotl")

        # Open Folder button
        self.open_button = tk.Button(parent, text="Open Folder", command=self.open_folder)
        self.open_button.grid(row=0, column=0, padx=20, pady=10)

        # Sigma Clip button
        self.sigma_button = tk.Button(parent, text="Sigma Clip", command=self.sigma_clip)
        self.sigma_button.grid(row=1, column=0, padx=20, pady=10)

        # Mean Stack button
        self.mean_button = tk.Button(parent, text="Mean Stack", command=self.mean_stack)
        self.mean_button.grid(row=2, column=0, padx=20, pady=10)

        # Sharpen button
        self.sharpen_button = tk.Button(parent, text="Sharpen", command=self.point_spread)
        self.sharpen_button.grid(row=3, column=0, padx=20, pady=10)

        # AP checkbox
        self.ap_label = tk.Label(parent, text = "AP Radius", font=("TkDefaultFont", 10, "underline"))
        self.ap_label.grid(row=4, column=0, sticky='w', padx=10, pady=10)
        self.ap_checkbox0 = tk.Radiobutton(parent, text = "50", variable=self.ap_radius, value=50)
        self.ap_checkbox0.grid(row=5,column=0, sticky='w', padx=10, pady=10)
        self.ap_checkbox1 = tk.Radiobutton(parent, text = "100", variable=self.ap_radius, value=100)
        self.ap_checkbox1.grid(row=6,column=0, sticky='w', padx=10, pady=10)
        self.ap_checkbox2 = tk.Radiobutton(parent, text = "200", variable=self.ap_radius, value=200)
        self.ap_checkbox2.grid(row=7,column=0, sticky='w', padx=10, pady=10)

        # Popout Display button
        self.sharpen_button = tk.Button(parent, text="Full Image View", command=self.show_full_image)
        self.sharpen_button.grid(row=8, column=0, padx=20, pady=10)

        # Previous and Next arrows
        self.prev_arrow = tk.Label(parent, text="◄", font=("Arial", 14), cursor="hand2")
        self.prev_arrow.grid(row=12, column=1, padx=0, pady=15)
        self.prev_arrow.bind("<Button-1>", lambda event: self.show_previous_image())

        # Slider bar
        self.slider = tk.Scale(parent, from_=0, to=1, length = 550, orient=tk.HORIZONTAL, command=self.slider_changed)
        self.slider.grid(row=12, column=2, columnspan=5, rowspan=1, padx=10, pady=10)

        self.next_arrow = tk.Label(parent, text="►", font=("Arial", 14), cursor="hand2")
        self.next_arrow.grid(row=12, column=11, padx=0, pady=15)
        self.next_arrow.bind("<Button-1>", lambda event: self.show_next_image())

        # Frame to contain FITS image viewer
        self.frame = tk.Frame(parent)
        self.frame.grid(row=1, column=1, columnspan=11, rowspan=11, padx=5, pady=5)

    # Loads a fits Image
    def load_image(self, image_name):
        image_file = get_pkg_data_filename(image_name)
        image_data = fits.getdata(image_file, ext=0)
        numpy_data = np.array(image_data)
        return numpy_data

    #Saves a Fits Image
    def save_image(self, numpy_data):
        file_path = filedialog.asksaveasfilename(defaultextension = ".fits")
        if file_path:
            file_out = fits.PrimaryHDU(numpy_data)
            file_out1 = fits.HDUList(file_out)
            file_out1.writeto(file_path, overwrite=True)
        return file_path

    # Opens a folder for working directory - GPT3.5
    def open_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.image_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.fits')]
            if self.image_paths:
                self.current_index = 0
                self.show_image()
        self.slider.config(from_=0, to=len(self.image_paths)-1)

    # Updates slider position - GPT3.5
    def slider_changed(self, value):
        index = int(float(value))
        self.current_index = index
        self.show_image()

    # Displays an image to the viewer - GPT3.5
    def show_image(self):
        plt.close('all')
        plt.figure()
        hdul = fits.open(self.image_paths[self.current_index])
        image_data = hdul[0].data
        
        # Downscale the image for display
        downscaled_image = cv2.resize(image_data, None, fx=self.downscale_factor, fy=self.downscale_factor)

        # Display downscaled image
        plt.imshow(downscaled_image, cmap='gray', origin='lower')

        # Tighten the axis limits to remove white borders
        plt.gca().set_aspect('equal', adjustable='box')
        plt.gca().autoscale(enable=True, axis='both', tight=True)

        # Turn off axis
        plt.axis('off')

        filename = os.path.basename(self.image_paths[self.current_index])
        plt.title(filename)

        if self.canvas:  # Check if canvas exists
            self.canvas.get_tk_widget().destroy()  # Destroy the existing canvas

        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Bind mouse click event to function
        self.canvas.mpl_connect('button_press_event', self.on_click)

        # Update slider value
        self.slider.set(self.current_index)

        # Change Key Image
        self.key_image_path = self.image_paths[self.current_index]

    # Popout display for better viewing features - GPT3.5
    def show_full_image(self):
        if self.image_paths == []:
            self.popup_error("No images in working directory")
            return
        plt.close('all')  # Close any previous figures
        hdul = fits.open(self.image_paths[self.current_index])
        image_data = hdul[0].data

        plt.imshow(image_data, cmap='gray', origin='lower')  # Display image
        plt.axis('off')  # Turn off axis
        plt.show()

    def on_click(self, event):
        self.show_image()
        # Save the coordinates of the click relative to the image
        if event.xdata is not None and event.ydata is not None:
            self.points.append((int(event.xdata/self.downscale_factor), int(event.ydata/self.downscale_factor)))
            print("Alignment Point at:", event.xdata/self.downscale_factor, event.ydata/self.downscale_factor)
            self.ap = [int(event.xdata/self.downscale_factor), int(event.ydata/self.downscale_factor)]

            # Clear previously plotted dots
            self.clear_dots()

            # Add a point marker on the image
            dot = plt.scatter(event.xdata, event.ydata, color='red', marker='o', s=10)  # 'o' marker, size 20, color red
            self.dots.append(dot)
            self.canvas.draw_idle()  # Redraw canvas to display the marker

    # removes alignment point while only a single point is compatible but multiple are intended
    def clear_dots(self):
        # Remove previously plotted dots
        for dot in self.dots:
            dot.remove()
        self.dots = []

    # Button for scrolling images - GPT3.5
    def show_previous_image(self):
        if self.image_paths:
            self.current_index = (self.current_index - 1) % len(self.image_paths)
            self.points.clear()  # Clear points when switching images
            self.show_image()

    # Button for scrolling images - GPT3.5
    def show_next_image(self):
        if self.image_paths:
            self.current_index = (self.current_index + 1) % len(self.image_paths)
            self.points.clear()  # Clear points when switching images
            self.show_image()

    # Removes images from an image set that out outside the standard deviation
    def sigma_clip(self):

        if self.image_paths == []:
            self.popup_error("No images in working directory")
            return

        average_blur = 0.0
        stddev_blur = 0.0
        n = len(self.image_paths)
        self.clip_list = []

        print("Calculating Average Sharpness")
        for images in tqdm(self.image_paths):
            input_image = self.load_image(images)
            average_blur += (cv2.Laplacian(input_image, cv2.CV_64F).var()/n)
        print("average blur: " + str(average_blur) + "\n")

        print("Calculating standard deviation of Sharpness")
        for images in tqdm(self.image_paths):
            input_image = self.load_image(images)
            stddev_blur += (abs(average_blur - cv2.Laplacian(input_image, cv2.CV_64F).var())/n)
        print("standard deviation: " + str(stddev_blur) + "\n")

        print("Removing images outside standard deviation")
        for images in tqdm(self.image_paths):
            input_image = self.load_image(images)
            blur = cv2.Laplacian(input_image, cv2.CV_64F).var()
            
            if (abs(blur - average_blur) < stddev_blur):
                self.clip_list.append(images)

        print(str(n)+" images reduced to " + str(len(self.clip_list)) + " images due to sigma clipping")
        self.image_paths = self.clip_list
        self.current_index = 0
        self.slider.config(from_=0, to=len(self.image_paths)-1)
        self.show_image()

    # Takes the average pixel value across all images
    def mean_stack(self):
        if self.image_paths == []:
            self.popup_error("No images in working directory")
            return
        elif self.ap == []:
            self.popup_error("Requires alignment point\nThis can be done by cliping on the current image")
            return
        key_image = self.load_image(self.key_image_path)
        mean_image = np.array([[0.0 for x in range(len(key_image[0]))] for y in range(len(key_image))])
        num = len(self.clip_list)
        for images in tqdm(self.image_paths):
            next_image = self.image_alignment(key_image, self.load_image(images))
            mean_image = mean_image + next_image/num
        if self.ap_radius !=0:
            mean_image = np.fft.ifftn(mean_image)
        self.output_image = np.uint16(mean_image.real)
        self.key_image_path = self.save_image(self.output_image)
        self.image_paths.clear()
        self.image_paths = [self.key_image_path]
        self.current_index = 0
        self.show_image()

    # Aligns on image with the reference image. Used during stacking
    def image_alignment(self, key_image, align_image):
        size = int(self.ap_radius.get())
        if self.ap == []:
            self.ap = [len(key_image)//2, len(key_image[0])//2]
            # print("len(key_image) == " + str(len(key_image)) + "\n")

        key_subimg = np.array([row[(self.ap[0]-size):(self.ap[0]+size)] for row in key_image[(self.ap[1]-size):(self.ap[1]+size)]])
        align_subimg = np.array([row[(self.ap[0]-size):(self.ap[0]+size)] for row in align_image[(self.ap[1]-size):(self.ap[1]+size)]])

        shift, error, diffphase = phase_cross_correlation(key_subimg, align_subimg)
        aligned_image = fourier_shift(np.fft.fftn(align_image), shift)

        return aligned_image

    # Sharpens the images using a sharpening filter - translated from sharpen.c
    def point_spread(self):

        if self.image_paths == []:
            self.popup_error("No images in working directory")
            return
        

        PSF = np.array([0, -1, 0,-1, 5, -1,0, -1, 0])

        image = self.load_image(self.key_image_path)
        output = image

        height = len(image)
        width = len(image[0])

        image_type = type(output[0][0])
        bounds = np.iinfo(image_type)

        image = image.flatten()

        print("Sharpening: " + str(self.key_image_path) + "\n")

        for i in tqdm(range(1, height-1)):
            for j in range(1,width-1):

                temp = 0.0
                temp += PSF[0] * image[((i-1)*width)+j-1]
                temp += PSF[1] * image[((i-1)*width)+j]
                temp += PSF[2] * image[((i-1)*width)+j+1]
                temp += PSF[3] * image[((i)*width)+j-1]
                temp += PSF[4] * image[((i)*width)+j]
                temp += PSF[5] * image[((i)*width)+j+1]
                temp += PSF[6] * image[((i+1)*width)+j-1]
                temp += PSF[7] * image[((i+1)*width)+j]
                temp += PSF[8] * image[((i+1)*width)+j+1]

                if temp < bounds.min:
                    temp = bounds.min
                if temp > bounds.max:
                    temp = bounds.max
                output[i][j] = image_type(temp)

        image = image.reshape(height, width)
        self.key_image_path = self.save_image(output)
        self.image_paths = [self.key_image_path]
        self.current_index = 0
        self.show_image()

    # Not yet implemented - GPT3.5
    def confirm_window(self, message):
        message = str(message)
        popup = tk.Toplevel(self.parent)
        popup.title("Confirmation")

        # Calculate the position of the popup window relative to the application window
        popup_width = 300
        popup_height = 75
        app_x = self.parent.winfo_rootx()  # X-coordinate of the application window
        app_y = self.parent.winfo_rooty()  # Y-coordinate of the application window
        app_width = self.parent.winfo_width()  # Width of the application window
        app_height = self.parent.winfo_height()  # Height of the application window
        popup_x = app_x + (app_width - popup_width) // 2  # X-coordinate of the popup window
        popup_y = app_y + (app_height - popup_height) // 2  # Y-coordinate of the popup window

        # Set the geometry of the popup window to center it relative to the application window
        popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")

        label = tk.Label(popup, text=error_message)
        label.pack()
        confirm_button = tk.Button(popup, text="OK", command=popup.destroy)
        confirm_button.pack()
        cancel_button = tk.Button(popup, text="OK", command=popup.destroy)
        cancel_button.pack()

    # Error message for when features can be used given the currently selected options - GPT3.5
    def popup_error(self, error):
        error_message = str(error)
        popup = tk.Toplevel(self.parent)
        popup.title("Error")

        # Calculate the position of the popup window relative to the application window
        popup_width = 300
        popup_height = 75
        app_x = self.parent.winfo_rootx()  # X-coordinate of the application window
        app_y = self.parent.winfo_rooty()  # Y-coordinate of the application window
        app_width = self.parent.winfo_width()  # Width of the application window
        app_height = self.parent.winfo_height()  # Height of the application window
        popup_x = app_x + (app_width - popup_width) // 2  # X-coordinate of the popup window
        popup_y = app_y + (app_height - popup_height) // 2  # Y-coordinate of the popup window

        # Set the geometry of the popup window to center it relative to the application window
        popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")

        label = tk.Label(popup, text=error_message)
        label.pack()
        ok_button = tk.Button(popup, text="OK", command=popup.destroy)
        ok_button.pack()

# Create the main window
root = tk.Tk()


# Create FITSViewer instance
app = Staxolotl(root)

# Run the Tkinter event loop
root.mainloop()

