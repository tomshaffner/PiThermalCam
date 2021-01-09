# -*- coding: utf-8 -*-
#!/usr/bin/python3
##################################
# MLX90640 Thermal Camera w Raspberry Pi
##################################

import time,board,busio
import numpy as np
import adafruit_mlx90640
import datetime as dt
import matplotlib.pyplot as plt
import cv2
import logging, configparser
import cmapy
import traceback

from numpy.lib.type_check import imag
from utils import *

profiling = False # Flag to turn profiling on
if profiling:
    import cProfile, pstats

# Manual Params
DEBUG_MODE=False

# Set up Logger
if DEBUG_MODE:
    logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(name)s:%(lineno)d] %(message)s',level=logging.DEBUG)
    logging.getLogger('matplotlib.font_manager').disabled = True # Disable warnings from matplotlib font manager when in debug mode
else:
    logging.basicConfig(filename='pithermcam.log',filemode='a',format='%(asctime)s %(levelname)-8s [%(filename)s:%(name)s:%(lineno)d] %(message)s',level=logging.WARNING,datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger(__name__)

# Parse Config file
config = configparser.ConfigParser(inline_comment_prefixes='#')
config.read('/home/pi/pithermalcam/config.ini')
logger.debug(f'Config file sections found: {config.sections()}')

## Read Global variables from config file
# Note: Raw parsing used to avoid having to escape % characters in time strings
logger.debug("Reading config file and initializing variables...")
output_folder = config.get(section='FILEPATHS',option='output_folder',raw=True)
filename_date_format = config.get(section='FILEPATHS',option='filename_date_format',raw=True) # NOTE: This will be used in Windows so no disallowed character like ":"

# Setup camera
i2c = busio.I2C(board.SCL, board.SDA, frequency=800000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_8_HZ  # set refresh rate
time.sleep(0.1)

# function to convert temperatures to pixels on image
def temps_to_rescaled_uints(f,Tmin,Tmax):
	norm = np.uint8((f - Tmin)*255/(Tmax-Tmin))
	norm.shape = (24,32)
	return norm

def take_pic(pic_name='simple_pic.png',use_f = False):
    """Take single pic"""  
    image = np.zeros((24*32,))

    # Get image
    mlx.getFrame(image) # read mlx90640
    temp_min = np.min(image)
    temp_max = np.max(image)
    image=temps_to_rescaled_uints(image,temp_min,temp_max)    

    # Image processing
    img = cv2.applyColorMap(image, cv2.COLORMAP_JET)
    img = cv2.resize(img, (320,240), interpolation = cv2.INTER_CUBIC)
    img = cv2.flip(img, 1)

    text = 'Tmin = {:+.1f} Tmax = {:+.1f} '.format(temp_min/100, temp_max/100)
    cv2.putText(img, text, (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)
    cv2.imshow('Output', img)

    fname = output_folder + 'pic_' + dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.jpg'
    cv2.imwrite(fname, img)
    print('Saving image ', fname)

def camera_read(use_f:bool = False, filter_image:bool = False):
    image = np.zeros((24*32,))
    t0 = time.time()
    colormap_index = 0
    # See https://gitlab.com/cvejarano-oss/cmapy/-/blob/master/docs/colorize_all_examples.md to develop list
    colormap_list=['jet','bwr','seismic','coolwarm','PiYG_r','tab10','tab20','gnuplot2','brg']
    try:
        while True:          
            # Get image
            mlx.getFrame(image) # read mlx90640
            temp_min = np.min(image)
            temp_max = np.max(image)
            img=temps_to_rescaled_uints(image,20,40)    

            # Image processing
            img = cv2.applyColorMap(img, cmapy.cmap(colormap_list[colormap_index]))
            img = cv2.resize(img, (800,600), interpolation = cv2.INTER_CUBIC) #INTER_LANCZOS4) #INTER_LINEAR)
            img = cv2.flip(img, 1)
            if filter_image:
                img = cv2.erode(img, None, iterations=2)
                img = cv2.dilate(img, None, iterations=2)
            if use_f:
                temp_min=c_to_f(temp_min)
                temp_max=c_to_f(temp_max)
                text = f'Tmin={temp_min:+.1f}F Tmax={temp_max:+.1f}F FPS={1/(time.time() - t0):.2f} Filtered:{filter_image} Colormap:{colormap_list[colormap_index]}'
            else:
                text = f'Tmin={temp_min:+.1f}C Tmax={temp_max:+.1f}C FPS={1/(time.time() - t0):.2f} Filtered:{filter_image} Colormap:{colormap_list[colormap_index]}'
            cv2.putText(img, text, (10, 18), cv2.FONT_HERSHEY_SIMPLEX, .6, (255, 255, 255), 2)
            cv2.namedWindow('Thermal Image', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Thermal Image', 1200,900)
            cv2.imshow('Thermal Image', img)

            # if 's' is pressed - saving of picture
            key = cv2.waitKey(1) & 0xFF
            if key == ord("s"): # If s is chosen, save an image to filec
                fname = output_folder + 'pic_' + dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.jpg'
                cv2.imwrite(fname, img)
                print('Thermal Image ', fname)
            if key == ord("c"): # If c is chosen cycle the colormap used
                colormap_index+=1
                if colormap_index==len(colormap_list):
                    colormap_index=0
            if key == ord("f"): # If f is chosen cycle the image filtering
                filter_image = not filter_image
                print(f"Filter On: {filter_image}")
            if key == ord("u"): # If t is chosen cycle the units used for temperature
                use_f = not use_f
                print(f"Using Fahrenheit: {use_f}")
                    
            t0 = time.time()
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        print("Code Stopped by User")
    except Exception as e:
        print(traceback.format_exc())
        pass

    cv2.destroyAllWindows()

class Motion_Detection_Camera:
    # Class based on post from https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/
    def __init__(self, accumWeight=0.5):
        # store the accumulated weight factor
        self.accumWeight = accumWeight
        # initialize the background model
        self.bg = None

    def update(self, image):
        # if the background model is None, initialize it
        if self.bg is None:
            self.bg = image.copy().astype("float")
            return
        # update the background model by accumulating the weighted
        # average
        cv2.accumulateWeighted(image, self.bg, self.accumWeight)

    def detect(self, image, tVal=25):
        # compute the absolute difference between the background model and the image passed in, then threshold the delta image
        delta = cv2.absdiff(self.bg.astype("uint8"), image)
        thresh = cv2.threshold(delta, tVal, 255, cv2.THRESH_BINARY)[1]
        # perform a series of erosions and dilations to remove small blobs
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)


if __name__ == "__main__":
    # take_pic()
    camera_read()