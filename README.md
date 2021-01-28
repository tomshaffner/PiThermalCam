# README #

Documentation of the thermal pi cam project, which connects an MLX90640 thermal camera up to a Raspberry Pi. (Built on a Pi 4)

Setup based primarily off the article at https://makersportal.com/blog/2020/6/8/high-resolution-thermal-camera-with-raspberry-pi-and-mlx90640#thermal-cam, with additions from https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/ and flask pieces based on https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/. Many thanks to Joshua Hrisko, Валерий Курышев, and Adrian Rosebrock for their work in these articles.

Full details for this project are available at https://tomshaffner.github.io/PiThermalCam/, including comprehensive hardware/software setup, install, and usage instructions. A cursory overview for development purposes only is included here.

### Manual Install/Setup ###

This section discusses software setup only, and assumes you have hardware set up, the MLX90640 correctly wired up, and the baudrate increased to 400k.

1. Install, using apt-get, the following items:
libatlas-base-dev
python-smbus
i2c-tools

2. Install remaining requirements using either:
a. 
    pip3 install the requirements.txt
or
b. 
    pip3 install the requirements_without_opencv.txt

    Download, build, and install OpenCV locally (painstaking process, but results in more optimized code).

    Install cmapy using --no-deps pip3 flag to avoid installing OpenCV via pip3.


### Usage ###

Run web_server.py to set up a flask server and strean live video.

Run pi_therm_cam.py to display the video feed onscreen.

Check examples folder for sequential running approaches that are easier to track/follow (i.e. not object-oriented). These are less robust, but can be easier to understand/track/edit, particularly for those coming from a scientific background. Again, refer to the link at top for a detailed discussion.