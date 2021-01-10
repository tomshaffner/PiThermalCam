# -*- coding: utf-8 -*-
#!/usr/bin/python3
##################################
# MLX90640 Thermal Camera w Raspberry Pi
##################################
import time,board,busio
import numpy as np
import adafruit_mlx90640
import datetime as dt
import cv2
import imutils
import logging, configparser
import cmapy
from numpy.lib.type_check import imag
from utils import *

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


class ThermalCam:
    # See https://gitlab.com/cvejarano-oss/cmapy/-/blob/master/docs/colorize_all_examples.md to develop list
    _colormap_list=['jet','bwr','seismic','coolwarm','PiYG_r','tab10','tab20','gnuplot2','brg']

    def __init__(self,use_f:bool = True, filter_image:bool = False, resize_image:bool = True, image_width:int=1200, image_height:int=900, output_folder:str = output_folder):
        self.use_f=use_f
        self.filter_image=filter_image
        self.resize_image=resize_image
        self.image_width=image_width
        self.image_height=image_height

        self._raw_image = np.zeros((24*32,))
        self._colormap_index = 0
        self._setup_therm_cam()
        self._t0 = time.time()
        return self.update_image_frame()

    def __del__(self):
        logger.debug("ThermalCam Object deleted.")

    def _setup_therm_cam(self):
        """Initialize the thermal camera"""
        # Setup camera
        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=800000) # setup I2C
        self.mlx = adafruit_mlx90640.MLX90640(self.i2c) # begin MLX90640 with I2C comm
        self.mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_8_HZ  # set refresh rate
        time.sleep(0.1)

    def _get_image(self):
        """Get one pull of the raw image data, converting temp units if necessary"""
        # Get image
        self.mlx.getFrame(self._raw_image) # read mlx90640
        self._temp_min = np.min(self._raw_image)
        self._temp_max = np.max(self._raw_image)
        if self.use_f:
            self._temp_min=c_to_f(self._temp_min)
            self._temp_max=c_to_f(self._temp_max)
        self._image=self._temps_to_rescaled_uints(self._raw_image,self._temp_min,self._temp_max)

    def _process_image(self):
        """Process the raw temp data to a colored image. Filter if necessary"""
        # Image processing
        self._image = cv2.applyColorMap(self._image, cmapy.cmap(self._colormap_list[self._colormap_index]))
        self._image = cv2.resize(self._image, (800,600), interpolation = cv2.INTER_CUBIC) #INTER_LANCZOS4) #INTER_LINEAR)
        self._image = cv2.flip(self._image, 1)
        if self.filter_image:
            self._image = cv2.erode(self._image, None, iterations=2)
            self._image = cv2.dilate(self._image, None, iterations=2)

    def _set_image_attributes(self):
        """Set image size and text content"""
        if self.use_f:
            text = f'Tmin={self._temp_min:+.1f}F Tmax={self._temp_max:+.1f}F FPS={1/(time.time() - self._t0):.2f} Filtered:{self.filter_image} Colormap:{self._colormap_list[self._colormap_index]}'
        else:
            text = f'Tmin={self._temp_min:+.1f}C Tmax={self._temp_max:+.1f}C FPS={1/(time.time() - self._t0):.2f} Filtered:{self.filter_image} Colormap:{self._colormap_list[self._colormap_index]}'
        cv2.putText(self.image, text, (10, 18), cv2.FONT_HERSHEY_SIMPLEX, .6, (255, 255, 255), 2)
        cv2.namedWindow('Thermal Image', cv2.WINDOW_NORMAL)
        if self.resize_image:
            cv2.resizeWindow('Thermal Image', self.image_width,self.image_height)
        cv2.imshow('Thermal Image', self.image)


    def change_colormap(self, forward:bool = True):
        """Cycle colormap. Forward by default, backwards if param set to false."""
        if forward:
            self._colormap_index+=1
            if self._colormap_index==len(self._colormap_list):
                self._colormap_index=0
        else:
            self._colormap_index-=1
            if self._colormap_index<0:
                self._colormap_index=len(self._colormap_list)-1

    def update_image_frame(self):
        """Pull raw data, process it to an image, and update image attributes"""
        self._get_image()
        self._process_image()
        self._set_image_attributes()
        return self._image

    def read_image_frame(self):
        return self._image

    def save_image(self):
        fname = self._output_folder + 'pic_' + dt.datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.jpg'
        cv2.imwrite(fname, self._image)
        print('Thermal Image ', fname)

    # function to convert temperatures to pixels on image
    def _temps_to_rescaled_uints(f,Tmin,Tmax):
        norm = np.uint8((f - Tmin)*255/(Tmax-Tmin))
        norm.shape = (24,32)
        return norm
        

class Motion_Detector:
    # Class based on post at https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/
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

    def detect(self, image, threshholdVal=25):
        # compute the absolute difference between the background model and the image passed in, then threshold the delta image
        delta = cv2.absdiff(self.bg.astype("uint8"), image)
        thresh = cv2.threshold(delta, threshholdVal, 255, cv2.THRESH_BINARY)[1]
        # perform a series of erosions and dilations to remove small blobs
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)

        # find contours in the thresholded image and initialize the minimum and maximum bounding box regions for motion
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        (minX, minY) = (np.inf, np.inf)
        (maxX, maxY) = (-np.inf, -np.inf)

        # if no contours were found, return None
        if len(cnts) == 0:
            return None
        # otherwise, loop over the contours
        for c in cnts:
            # compute the bounding box of the contour and use it to update the minimum and maximum bounding box regions
            (x, y, w, h) = cv2.boundingRect(c)
            (minX, minY) = (min(minX, x), min(minY, y))
            (maxX, maxY) = (max(maxX, x + w), max(maxY, y + h))
        # otherwise, return a tuple of the thresholded image along with bounding box
        return (thresh, (minX, minY, maxX, maxY))
