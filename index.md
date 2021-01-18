# MLX90640 Thermal Camera with Raspberry Pi 4
{:.no_toc}
January, 2021

# Note: This page is still under construction. Check back later for the final version.
{:.no_toc}

## Introduction
{:.no_toc}

It's winter, and my heating bill has gone up. I've also noticed a draft in certain areas of my house, so I decided it was time to fulfill my long-awaited dream of getting a thermal camera. These have generated some buzz of late as potential Covid temperature detectors, but I was more interested in seeing where there's an insulation problem in my house that I might fix. Also, fun to play with!

Cameras such as these can produce images like this one, showing where heat is leaving a building:

![Image of House from Thermal Camera](/images/Passivhaus_thermogram_gedaemmt_ungedaemmt.png)
*[Passivhaus Institut, CC BY-SA 3.0](http://creativecommons.org/licenses/by-sa/3.0/), via Wikimedia Commons*

Initially I researched buying or renting such a camera, but the buying options tend to start at [$200 for the basic smartphone version](https://www.flir.com/products/flir-one-gen-3/), and go up to nearly $1,000. My local Lowe's has such cameras for rent as well but they cost $50 for 24 hours!

I've long been a Raspberry Pi fan so when I saw that rental price I decided to see what options were available for the Pi. I quickly found the MLX90640 camera which costs only $60; at this price I figured I'd get a cool gadget to play with, be able to evaluate my house for leaks, and when I'm done I might use it as a security camera. I would of course also need a pi and accompany equipment but I had some of that and would be able to reuse it all for other projects as well. This was also a great excuse to finally upgrade from the Pi 3B+ I had to a [Pi 4](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/).

Of note: The resolution on this camera is much lower so we'll never get pictures quite like the above, but a mere few years ago even the [best cheaper camera](https://www.adafruit.com/product/3538) had only an 8x8 resolution, which is nearly unusable for projects like this. Jumping up to 24x32 resolution of the MLX90640 is a 12-fold increase for about the same price! It seems we've finally reached the point where cheap homemade versions of the camera are worth buying.

The below guide is meant to be a start-to-finish overview of the parts, setup, install, and use of this project for any who want to do likewise or build on it further.

* This line is replaced at runtime by a Table of Contents of headers, excluding the top header
{:toc}

## Background/Acknowledgements

There were several such projects already online, and I ended up taking pieces of two as my baseline, mixing and matching, and adding features like web streaming from a third page. The results of that work are placed here for others to use directly or as a baseline for further develoment. The code is also available in the Github Repo corresponding to this page (link at top). The license is also included there and is an AGPL-3.0 License.

Thanks are owed to those three other projects: namely, Joshua Hrisko's article at Maker Portal, [High Resolution Thermal Camera with Raspberry Pi and MLX90640](https://makersportal.com/blog/2020/6/8/high-resolution-thermal-camera-with-raspberry-pi-and-mlx90640),  Валерий Курышев's article under the name Walker2000 at Habr, [Making a DIY thermal camera based on a Raspberry Pi](https://habr.com/en/post/441050/), and Adrian Rosebrock's article [OpenCV – Stream video to web browser/HTML page](https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/). Their work was a BIG step forward as a starting point.

## Parts Required

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
- Portable battery with amp output ~ 3 Amps
- Screen for the Raspberry Pi

If you're going to be walking around your house, or outside it, you'll want some way to see the camera output live. As such, you'll probably need a portable battery for the device and, if you're not going to stream the video over your WIFI (or your pi will go outside of internet range), you'll want a screen to attach to the Pi.

I went with the Wifi option so I can't speak to screens, but I'd imagine any of the many Pi-specific screens would be fine for this.

On the battery, the Pi 4 draws around 3 Amps so you'd want any backup battery you have which can feed a USB-C connection with 3 Amps. You could try one with less power than this if it's not too low everything would probably work, it would just be slower.

## Physical Setup

## Software Installation

## Setting Up Run

### Matplotlib Version

### OpenCV Version - Local

### OpenCV Version - Web Server

## Usage



For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).
