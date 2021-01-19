{:.center}
# MLX90640 Thermal Camera with Raspberry Pi 4
{:.no_toc}

{:.center}
_January, 2021_

# Note: This page is still under construction. Check back later for the final version.
{:.no_toc}

## Introduction
{:.no_toc}

It's winter, and my heating bill has gone up. I've also noticed a draft in certain areas of my house, so I decided it was time to fulfill my long-awaited dream of getting a thermal camera. These have generated some buzz of late as potential Covid temperature detectors, but I was more interested in seeing where there's an insulation problem in my house that I might fix. Also, fun to play with!

Cameras such as these can produce images like this one, showing where heat is leaving a building:

{:.center}
![Image of House from Thermal Camera](/images/Passivhaus_thermogram_gedaemmt_ungedaemmt.png#center)
*[Passivhaus Institut, CC BY-SA 3.0](http://creativecommons.org/licenses/by-sa/3.0/), via Wikimedia Commons*

Initially I researched buying or renting such a camera, but the buying options tend to start at [$200 for the basic smartphone version](https://www.flir.com/products/flir-one-gen-3/), and go up to nearly $1,000. My local Lowe's has such cameras for rent as well but they cost $50 for 24 hours!

I've long been a Raspberry Pi fan so when I saw that rental price I decided to see what options were available for the Pi. I quickly found the MLX90640 camera which costs only $60; at this price I figured I'd get a cool gadget to play with, be able to evaluate my house for leaks, and when I'm done I might use it as a security camera.

I would of course also need a pi and accompany equipment but I had some of that and would be able to reuse it all for other projects as well. This was also a great excuse to finally upgrade from the Pi 3B+ I had to a [Pi 4](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/).

Of note: The resolution on this camera is much lower so we'll never get pictures quite like the above, but a mere few years ago even the [best cheaper camera](https://www.adafruit.com/product/3538) had only an 8x8 resolution, which is nearly unusable for projects like this. Jumping up to 24x32 resolution of the MLX90640 is a 12-fold increase for about the same price! It seems we've finally reached the point where cheap homemade versions of the camera are worth buying.

The below guide is meant to be a start-to-finish overview of the parts, setup, install, and use of this project for any who want to do likewise or build on it further.

**Contents**
* This line is replaced at runtime by a Table of Contents of headers, excluding those headers followed by {:.no_toc} 
{:toc}

## Background

There were several such projects already online, and I ended up taking pieces of two as my baseline, mixing and matching, and adding features like web streaming from a third page. The results of that work are placed here for others to use directly or as a baseline for further develoment. The code is also available in the Github Repo corresponding to this page (link at top). The license is also included there and is an AGPL-3.0 License.

Thanks are owed to those three other projects: namely, Joshua Hrisko's article at Maker Portal, [High Resolution Thermal Camera with Raspberry Pi and MLX90640](https://makersportal.com/blog/2020/6/8/high-resolution-thermal-camera-with-raspberry-pi-and-mlx90640),  Валерий Курышев's article under the name Walker2000 at Habr, [Making a DIY thermal camera based on a Raspberry Pi](https://habr.com/en/post/441050/), and Adrian Rosebrock's article [OpenCV – Stream video to web browser/HTML page](https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/). Their work was a BIG step forward as a starting point.

## Parts Required

{:.center}
![Raspberry Pi 4](/images/Raspberry_Pi_4_Model_B_-_Side.jpg#center)
*[By Miiicihiaieil  Hieinizilieir / Wikimedia Commons, CC BY-SA 4.0](https://commons.wikimedia.org/w/index.php?curid=80140656)*

Most of the parts lists I see are incomplete or link to pages with excessive costs (e.g. the Pi was invented to be accessible, so the basic version should never be > $35 before shipping). Below is a complete list of parts needed if you're starting from scratch. The Pi-specific items can be reused for other projects; the camera is really the only item specific to this project.

Prices are approximate as of Jan. 2021:
- $60 + Shipping - [MLX90640 Thermal Camera](https://www.adafruit.com/product/4469)
  - Note: The Thermal Camera comes in two flavors; one that's 110 Degrees wide, one that's 55. For purposes of this project the 55 would have been MUCH better but unfortunately it was sold out, so I had to make do with the with 110. This makes my thermal evaluation harder but the camera will likely be better for security camera use longer term. I haven't had the chance to try it but I believe this code should work with the 55 Degree version without alteration too.
- $1 + Shipping - [STEMMA QT / Qwii with Female Sockets](https://www.adafruit.com/product/4397) - This, or some other wiring solution, is needed to connect the camera easily to the Pi.
- $35 + Shipping - [Raspberry Pi 4](https://www.adafruit.com/product/4292)
  - Note: This same project could likely be performed with other Raspberry Pi versions as well, e.g. a Pi 3 or the like. Some adjustments might be necessary though, and for purposes here the Pi 4 with 2 GB RAM is the one being used.
- $10-$30 - Raspberry Pi SD Card with Raspbian Installed - You can buy cards with Raspbian pre-loaded or get larger or faster cards from a variety of sources, so long as they follow the [right guidelines](https://www.raspberrypi.org/documentation/installation/sd-cards.md).
  - Note: If buying a card >=64GB make sure you check the [instructions for exFAT formatting](https://www.raspberrypi.org/documentation/installation/sdxc_formatting.md). 
- ~$12 - Raspberry Pi Power Supply - You can get cheaper ones online, but they don't always have sufficient power output (Amps). For a quality one check [here](https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/)
- Optional - Cooling Case with Fan - There are a variety of these to buy. You might well be fine without it, but the Pi 4 runs hot enough that I decided I wanted one simply to not need to worry about the CPU temp. Of note, if you have a Pi 4, looking for a case/fan in which the fan has 3 wires, not 2, so that you can connect it up to the Raspbian fan control which turns it on/off automatically as needed. The 2-wire versions will need adjustment or will be always on.

#### Other Things you might need:
- Portable battery with output ~ 3 Amps
- Screen for the Raspberry Pi

If you're going to be walking around your house, or outside it, you'll want some way to see the camera output live. As such, you'll probably need a portable battery for the device and, if you're not going to stream the video over your WIFI (or your pi will go outside of internet range), you'll want a screen to attach to the Pi.

I went with the Wifi option so I can't speak to screens, but I'd imagine any of the many Pi-specific screens would be fine for this.

On the battery, the Pi 4 draws around 3 Amps so you'd want any backup battery you have which can feed a USB-C connection with 3 Amps. I had a battery I use for my phone while traveling that worked great. You could try one with less power than this; just be aware that even if it runs it might be a bit slower.

## Hardware Setup

{:.center}
![Wiring Setup](/images/mlx90640_rpi_wiring_diagram_w_table.png#center)
*[By Joshua Hrisko / Maker Portal, copied permission and thanks](https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/)*

Most of the physical setup is straightforward. The one piece specific to this project is wiring the camera to the Pi itself, and luckly for us, Josh at Maker Portal has made the perfect picture (above) for this and kindly agreed to let me put it here too.

The image shows where the camera connects to the Pi using the appropriate power and I2C pins. In my particular case I had a fan on the ground pin shown in this so I needed to move the ground wire to another ground on the Pi, but you can find another ground as needed in the [GPIO pinout diagrams](https://www.raspberrypi.org/documentation/usage/gpio/) available in many places online.

## Software Installation

There are two approaches to the video in this package. The first uses Matplotlib and is based on [Joshua Hrisko's article](https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/) mentioned above. It works fine but in my case ran incredibly slow (though it had superior processing algorithms; more on this later). It was almost unusable without substantial speed improvements, so I switched to:

The second approach uses an OpenCV approach based on the [article by Валерий Курышев](https://habr.com/en/post/441050/), which ran MUCH faster for me, and thus I focused subsequent work on importing the algorithms from Josh's article into the OpenCV method.

You can install simply the listed requirements in steps 1 and 2 below and that will be sufficient to use the Matplotlib approach as is. If you wish to use the faster (higher FPS in the final video) and more robust approach though, you'll need to go through the longer and more complex process of installing OpenCV as well.

#### Installation Steps
**1. apt-get Installs**

First, a number of these can be installed using apt-get, in particular these three:
libatlas-base-dev
python-smbus
i2c-tools

**2. Pip Installs**

Most of the remaining packages are listed in the requirements.txt file and can be installed via pip using the command `pip3 install -r requirements.txt`.

**3. OpenCV Install**

OpenCV is a very large and comprehensive video processing library. It works faster partly because it runs mostly in C++. There are thus two ways to install it.
1. Attempt a pip install
  - There are premade versions of the library that can be installed using pip. This changes often so it's worth searching for yourself, but at the time of this writing [this article](https://www.jeremymorgan.com/tutorials/raspberry-pi/how-to-install-opencv-raspberry-pi/) or [this article](https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/) discuss the pip method to do this. This is much faster/simpler but from what I've read it also is less optimized and in develpment I wanted every ounce of speed so I did the more complex install below. If you just want a simple setup give it a go; from what I've read it likely isn't a huge speed difference. If you do this, the whole system install is slightly simpler and fine if you don't expect to use multiple OpenCV versions; the virtual environment install is a bit cleaner if you might have multiple versions.
2. Compile/Install OpenCV Locally
  - This results in a more robust and optimized install and is what I used, but it also requires a MUCH longer and more cumbersome install process: one with many steps and which, at one point, takes an hour for the build to finish. Fortunately there are many sites that walk through the steps to do this. As this changes often it's again worth searching the web for more updated install instructions for OpenCV on a Raspberry Pi, but at the time of this writing [this article](https://qengineering.eu/install-opencv-4.4-on-raspberry-pi-4.html) or [this article](https://learnopencv.com/install-opencv-4-on-raspberry-pi/) work (check for newer OpenCV version even in those though). Again, I installed directly, skipping the virtual environment, but either approach should be fine for this project.

**4. Cmapy Install**

A final small step: you'll need to install the cmapy python library. It has opencv as a dependency though, and so requires one shift.
 - If you're using the pip install approach for OpenCV you can just install cmapy via pip3 no problem.
 - If you're compiling OpenCV however you'll need to install cmapy using the --no-deps flag to prevent it trying to also install the pip version of OpenCV. To do this, simply run `pip3 install cmapy --no-deps`

## Setting Up Run

First, clone the Git repo locally. Clone it into your default (pi) folder for best functioning. This can be done by opening a terminal, making sure you're in the pi folder, and typing `git clone https://github.com/tomshaffner/PiThermalCam.git`.

There are three approaches for running. All three are python 3 scripts so if you're comfortable with running python code manually or via an IDE you can just execute them. Details outlined below.

For convenience I also created a desktop icon for each approach; those icons are in the templates folder and can be copied to your Raspbian desktop. Depending on how they downloaded You may need to make them executable, and they only work if you've installed this library in pi/pithermalcam/; otherwise you'll have to update the links.

### Matplotlib Version

### OpenCV Version - Local

### OpenCV Version - Web Server

## Usage



For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).
