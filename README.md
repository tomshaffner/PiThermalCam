# README #

Documentation of the pithermalcam project and accompanying [PyPI package](https://pypi.org/project/pithermalcam/), which connects an MLX90640 thermal camera up to a Raspberry Pi. (Built on a Pi 4)

Setup based primarily off the articles [by Joshua Hrisko at MakerPortal](https://makersportal.com/blog/2020/6/8/high-resolution-thermal-camera-with-raspberry-pi-and-mlx90640) and by [Валерий Курышев’s under the name Walker2000 at Habr](https://habr.com/en/post/441050/) and flask pieces based on the work of [Adrian Rosebrock at pyimagesearch](https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/). Many thanks these people for their great work.

Full details for this project are available at https://tomshaffner.github.io/PiThermalCam/, including comprehensive hardware/software setup, install, usage instructions, and examples of potential results. A cursory overview for development purposes only is included here.

### Manual Install/Setup ###

This section discusses software setup only, and assumes you have hardware set up, the MLX90640 correctly wired up, I2C turned on, and the I2C baudrate increased to 400k. Refer to the above full details link for detailed instructions on both the hardware and software installs.

The below install is for manual operation of the library. For the Pip install from PyPi skip the below and simply execute `pip3 install pithermalcam`.

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

    Download, build, and install OpenCV locally (painstaking process, but results in more optimized code.).

    Install cmapy using --no-deps pip3 flag to avoid installing OpenCV via pip3.


### Usage ###

#### Pip Library Install ####

If you install the library via Pip you can follow the usage shown in the examples folder to see usage instructions.

#### Clone library locally ####
If you wish to clone the library, execute this clone command:

`git clone -b master --single-branch https://github.com/tomshaffner/PiThermalCam.git`

This clones the code without cloning the pictures for the accompanying article (which take up excessive space).

To operate from here:

1. Copy the icons to your desktop and make executable.

or

2. Run the files directly in python3:

Run pithermalcam/web_server.py to set up a flask server and stream live video over the local network.

Run pithermalcam/pi_therm_cam.py to display the video feed onscreen.

Check sequential_versions folder for sequential running approaches that are easier to track/follow (i.e. sequential running rather than object-oriented classes). These are less robust, but can be easier to understand/track/edit, particularly for those coming from a scientific background. Again, refer to the link at top for a detailed discussion.
