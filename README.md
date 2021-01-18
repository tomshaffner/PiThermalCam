# README #

Documentation of the thermal pi cam project, which connects an MLX90640 thermal camera up to a Raspberry Pi 4.

Setup based primarily off the article at https://makersportal.com/blog/2020/6/8/high-resolution-thermal-camera-with-raspberry-pi-and-mlx90640#thermal-cam, with additions from https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/ and flask pieces based on https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/.

### How do I get set up? ###

1. Install, using apt-get, the following items:
libatlas-base-dev
python-smbus
i2c-tools

2. pip3 install the requirements.txt

3. If you're going to use the opencv implementations in this you'll need to install and build opencv. You can do this via pip, but the manual build approach is the more nuanced approach.

You'll also want to install cmapy, but it's not in the requirements file because a pip install will automatically install opencv via pip. If you're okay with this that's fine; if not you'll want to install using the --no-deps pip install.