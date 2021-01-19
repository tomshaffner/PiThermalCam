{:.center}
# MLX90640 Thermal Camera with Raspberry Pi 4
{:.no_toc}

{:.center}
_January, 2021_

# Note: This page is still under construction. Check back later for the final version.
{:.no_toc}

## Introduction
{:.no_toc}

It's winter, and my heating bill has gone up. I've also noticed a draft in certain areas of my house, so I decided it was time to fulfill my long-awaited dream of getting a thermal camera. These have generated some buzz of late as potential Covid temperature detectors, but I was more interested in seeing where there's an insulation problem in my house that I might fix, or to be able to detect leaks in pipes. Also, fun to play with!

Cameras such as these can produce images like this one, showing where heat is leaving a building:

{:.center}
![Image of House from Thermal Camera](/images/Passivhaus_thermogram_gedaemmt_ungedaemmt.png#center)
*[Passivhaus Institut, CC BY-SA 3.0](http://creativecommons.org/licenses/by-sa/3.0/), via Wikimedia Commons*

Initially I researched buying or renting such a camera, but the buying options tend to start at [$200 for the basic smartphone version](https://www.flir.com/products/flir-one-gen-3/), and go up to nearly $1,000. My local Lowe's has such cameras for rent as well but they cost $50 for 24 hours!

I've long been a Raspberry Pi fan so when I saw that rental price I decided to see what options were available for the Pi. I quickly found the MLX90640 camera which costs only $60; at this price I figured I'd get a cool gadget to play with, be able to evaluate my house for leaks, and when I'm done I can use it as a security camera.

I would of course also need a raspberry pi and accompany equipment but I had some of that and would be able to reuse it all for other projects as well. This was also a great excuse to finally upgrade from the Pi 3B+ I had to a [Pi 4](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/).

Of note: The resolution on this camera is much lower so we'll never get pictures quite like the above, but a mere few years ago even the [best cheaper camera](https://www.adafruit.com/product/3538) had only an 8x8 resolution, which is nearly unusable for projects like this. Jumping up to 24x32 resolution of the MLX90640 is a 12-fold increase for about the same price! It seems we've finally reached the point where cheap homemade thermal cameras are worth buying.

The below guide is meant to be a start-to-finish overview of the parts, setup, install, and use of this project for any who want to do likewise or build on it further. I don't cover everything needed to work with a Raspberry Pi itself as there are plenty of other guides for that out there, but I try to touch on any and all pieces related to this project directly.

**Contents**
* This line is replaced at runtime by a Table of Contents of headers, excluding those headers followed by {:.no_toc} 
{:toc}

## Background

There were several similar projects already online, and I ended up taking pieces of two as my baseline, mixing and matching, and adding features like web streaming from a third source. The results of that work are placed here for others to use directly or as a baseline for further develoment. The code is also available in the Github Repo corresponding to this page (link at top). The license is also included there and is an AGPL-3.0 License, so if you make changes and publish, you'll need to publish the code with it.

Thanks are owed to those three other projects: namely, Joshua Hrisko's article at Maker Portal, [High Resolution Thermal Camera with Raspberry Pi and MLX90640](https://makersportal.com/blog/2020/6/8/high-resolution-thermal-camera-with-raspberry-pi-and-mlx90640),  Валерий Курышев's article under the name Walker2000 at Habr, [Making a DIY thermal camera based on a Raspberry Pi](https://habr.com/en/post/441050/), and Adrian Rosebrock's article [OpenCV – Stream video to web browser/HTML page](https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/). Their work was a BIG step forward as a starting point.

## Parts Required

{:.center}
![Raspberry Pi 4](/images/Raspberry_Pi_4_Model_B_-_Side.jpg#center)
*[By Miiicihiaieil  Hieinizilieir / Wikimedia Commons, CC BY-SA 4.0](https://commons.wikimedia.org/w/index.php?curid=80140656)*

Most of the parts lists I see are incomplete or link to pages with excessive costs (e.g. the Pi was invented specifically to be cheaper, so the basic version should never be > $35 before shipping). Below is a complete list of parts needed if you're starting from scratch. The Pi-specific items can be reused for other projects; the camera is really the only item specific to this project.

Prices are approximate as of Jan. 2021:
- $60 + Shipping - [MLX90640 Thermal Camera](https://www.adafruit.com/product/4469)
  - Note: The Thermal Camera comes in two flavors; one that's 110 Degrees wide, one that's 55. For purposes of this project the 55 would have been MUCH better but unfortunately it was sold out, so I had to make do with the with 110. This makes my thermal evaluation harder but the camera will likely be better for security camera use longer term. I haven't had the chance to try it but I believe this code should work with the 55 Degree camear too.
- $1 + Shipping - [STEMMA QT / Qwii with Female Sockets](https://www.adafruit.com/product/4397) - This, or some other wiring solution, is needed to connect the camera to the Pi.
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
*[Image by Joshua Hrisko / Maker Portal, copied with permission and thanks](https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/)*

Most of the physical setup is straightforward. The one piece specific to this project is wiring the camera to the Pi itself, and luckly for us, Josh at Maker Portal has made the perfect picture (above) for this and kindly agreed to let me put it here too.

The image shows where the camera connects to the Pi using the appropriate power and I2C pins. In my particular case I had a fan on the ground pin shown in this so I needed to move the ground wire to another ground on the Pi, but you can find another ground as needed in the [GPIO pinout diagrams](https://www.raspberrypi.org/documentation/usage/gpio/) available in many places online.

Below is a picture of my device in final form. You can see the case I used (but would not recommend; better to get one a tad more open and with a variable speed fan) and the fact that I initially bought a Stemma connector with male ends meant I had to solder those to other wires to connect to the Pi. If you buy the right pieces the first time yours will look cleaner than this.

I found taping the camera to the case an easy way to make using the device simpler to work with.

{:.center}
![Assembled Device](/images/assembled device.jpg#center)
*Final Device Assembled*

## Prerequisite Software Installation

There are two approaches to the video in this package. The first uses Matplotlib and is based on [Joshua Hrisko's article](https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/) mentioned above. It works fine but in my case ran incredibly slow (though it had superior processing algorithms; more on this later). It was almost unusable without substantial speed improvements, so I switched to:

The second approach uses an OpenCV approach based on the [article by Валерий Курышев](https://habr.com/en/post/441050/), which ran MUCH faster for me, and thus I focused subsequent work on importing the algorithms from Josh's article into the OpenCV method.

You can install simply the listed requirements in steps 1 and 2 below and that will be sufficient to use the Matplotlib approach as is. If you wish to use the faster (higher FPS in the final video) and more robust approach though, you'll need to go through the longer and more complex process of installing OpenCV as well.

### Installation Steps
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

 **5. Enable I2C and Increase Pi Baudrate**
Finally you'll need to enable I2C on your Raspberry Pi and increase the baudrate. I2C can be enabled simply in the Pi Configuration via GUI or via typing `sudo raspi-config` and enabling it there.

To increase your baudrate, type `sudo nano /boot/config.txt` and find the line with `dtparam=i2c_arm=on`. Add `i2c_arm_baudrate=400000` to the end of it, so the end result should look like:

{:.center}
![Baudrate Change](/images/baudrate change.gif#center)
*Section of /boot/config.txt after baudrate change.*

Save the file and reboot the device when you're done.

Note: In the first article I referenced, baudrates much higher than 400k were apparently tested; as high as 1M. I tested some higher rates but got many more errors at these levels. Running at higher rates also increases the risk of overheating as the maximum supported speed is [apparently 400k](https://raspberrypi.stackexchange.com/questions/108896/what-is-rpis-i2c-maximum-speed#:~:text=The%20maximum%20supported%20speed%20is%20400%20Kb%2Fs.). When I switched to the OpenCV approach (discussed below), 400k was fast enough to be usable. Since I want to reuse my Pi for other projects or as a security camera long term I stuck with the 400k. If you want the Matplotlib approach to work faster, as it did for the writer of that first article, this is likely what you'd need to change; just make sure you have good heat management of your Pi in doing so. My choice to stick with only 400k is likely why that approach is so slow for me, and is thus why the OpenCV approach is the one I mainly use.

 **Connection Verification**

Once the above steps are done and your device is connected you can check to ensure the camera is visible to your pi. Run the command `sudo i2cdetect -y 1` and you should see a result like the below, indicating the camera is visible at the 0x33 address.

{:.center}
![I2C Camera Detected](/images/i2c detected.gif#center)
*The Raspberry PI registers the camera present at address 33.*

Of note: The basic datasheet is available at Digikey for the [110 Degree Camera Version](https://media.digikey.com/pdf/Data%20Sheets/Adafruit%20PDFs/4469_Web.pdf) and the [55 Degree Version](https://media.digikey.com/pdf/Data%20Sheets/Adafruit%20PDFs/4407_Web.pdf). In both cases though the underlying camera device itself has the [same datasheet](https://www.melexis.com/-/media/files/documents/datasheets/mlx90640-datasheet-melexis.pdf), which shows that register 33 is the correct address.

**IDE Setup for Development**

If you're not going to run simply from the icons or script, you'll likely will want an IDE in order to look at and work with the python code. The Raspberry Pi comes with several now; if you installed the Raspbian version with recommended software you can find them in the Programming section of the menu. In my case though, I love Visual Studio Code and it's now supported on the Pi!! Straightforward install instructions are available at [PiMyLifeUp](https://pimylifeup.com/raspberry-pi-visual-studio-code/). Also, if you want a faster development experience you can install VS Code on your local machine, enable and set up SSH on the Pi (tutorials on this easy to find), and then use the remote development extension from your local VSCode. This was actually the best dev experience I found; the only down side is that running in this way will, in some approaches, throw errors because you don't have a display. As such I did 90% of my development via remote SSH and the remaining 10%, where I needed to have live video on the Pi itself, either directly in the terminal on the Pi or in VSCode on the Pi.

None of this is required, but if you find yourself looking to develop this project further, I found this setup to be the best.

## Library Installation

After the prereq setup, clone the Git repo to your Pi. Clone it into your default (pi) folder to mirror my setup and avoid needing extra adjustments. This can be done by opening a terminal, making sure you're in the pi folder, and typing `git clone https://github.com/tomshaffner/PiThermalCam.git`.

There are three approaches for running the camear. All three are python 3 scripts so if you're comfortable with running python code manually or via an IDE you can just execute them. Details outlined below.

For convenience I also created a desktop icon for each approach; those three icons are in the templates folder and can be copied to your Raspbian desktop. Depending on how they downloaded you may need to make them executable, and they only work if you've installed this library in pi/pithermalcam/; otherwise you'll have to update the links.

## The Three Approaches

There are three approaches or methods used in this library.

**Matplotlib:** The first, using Matplotlib, is based off the previously mentioned [article by Joshua Hrisko](https://makersportal.com/blog/2020/6/8/high-resolution-thermal-camera-with-raspberry-pi-and-mlx90640). The picture colormapping and interpolation used in this approach is quite good, but it requires the baudrate to be well over the recommended limit to function as a reasonable rate. I was lucky to get a picture a second at the 400k baudrate. I would recommend starting with this approach to perform tests on your camera to make sure it's working, but once you've verified that it's probably better to move on to the other methods.

**OpenCV:** The second approach uses OpenCV and runs MUCH faster. As I'll discuss below though, I found the colormaps and interpolation of Matplotlib superior, and so I ended up importing those pieces of the Matplotlib into this approach.

**OpenCV Web Server:** The first two approaches run locally and display video output on the Pi directly. If you have a screen for the Pi or you're remoting into it via Remote Desktop or VNC this works fine. If you're walking around your house trying to use Remote Desktop on your phone to see the video output though, this can be a pain. As such I took the second approach above and rebuilt it into a Flask webserver version. If you start the webserver you'll see an IP Address printed out, and you can load that IP via a web browser on any computer in the network to see and control the video. For me, this was the more reliable/robust solution in practice.

All three versions are discussed in more detail below.

### Matplotlib Version

The Matplotlib version can be found in the examples folder under the name matplotlib_therm_cam.py. It has several running modes which can be switched via the number at the bottom of the file, as visible here:
{:.center}
![Matplotlib Modes](/images/matplotlib_modes.gif#center)
*The running modes available for the Matplotlib Approach*

Run this by executing the icon or going into the folder in the terminal and typing `python3` followed by the filename. The mode from the number chosen will execute.

Mode 1 in the picture is the simples just to make sure you're getting readings from your camera. Mode 2 then takes a basic picture (saved to the run_data folder) showing the raw data without any interpolation. Mode 3 is mode 2 in video form. Modes 4 and 5 correlate to modes 2 and 3, except with interpolation built in.

In the video modes, the video will continue unless/until an error occurs, the terminal window is closed, or the code in the terminal is halted.

### OpenCV Version - Local

The OpenCV Local version can be found in the examples folder under the name opencv_therm_cam.py. It has two running modes which can be switched via the number at the bottom of the file, but the default is the video mode which is likely all you need if everything is installed correctly.

Run this by executing the icon or going into the folder in the terminal and typing `python3` followed by the filename.

In the normal mode, the video will start running.

In using the camera I quickly found that it was useful to be able to change a number of features as the camera was running. Let's discusse these here:

#### Colormaps
The colormap used can sometimes make a big differences in what is easily visible or not. In this clip, for example, you can see both my body heat on the side and two cold windows in the backgroung. I cycle the colormap in this, showing how much it can make a difference in how easy/hard it is to see differences.

{:.center}
![Cycling Colormaps](/images/cycling colormaps.gif#center)
*Different colormaps make it easier to see important areas*

Note: It's hard to see in the compressed gif here, but the colormap used is displayed in the white text at the top.

The contrast in the image also makes a big difference. E.g. as I move out of the picture in this clip, the smaller temperature differences in the image become much more visible, making the impact of the windows much clearer. Again, different colormaps can help highlight areas of interest here too.

{:.center}
![Impact of Temperature Range on image](/images/turning_to_windows_only.gif#center)
*As I leave the image, my bodyheat being removed makes the temperature difference between the windows and wall more visible*

Also, the process of blowing the image up larger requires zoom/interpolation algorithms of various sorts. As an example, here is a picture of me with the Matplotlib approach before interpolation (i.e. just the raw data as an image):

{:.center}
![Matplotlib Raw Data Wave](/images/Matplotlib Simple Wave.gif#center)
*The raw temperature data as an image.*

Now change the color scheme and interpolate for a much cleaner picture:

{:.center}
![Matplotlib Wave](/images/Matplotlib Wave.gif#center)
*Note the clarity of the border between my body and the surroundings.*

Apart from having evidence that my hands aren't just feeling cold but actually ARE cold, this image highlights particularly how good the Matplotlib approach (which uses the SciPy library for interpolation) sets the coloring to detect edges. The white line surrounding the red of my body makes the boundary much clearer.

#### Interpolation Algorithms
OpenCV, in contrast, has a number of interpolations algorithms, but most of them don't function as well with boundaries like this, and the default colormaps weren't as useful. As a result I used the cmapy library to import a handful of Matplotlib colormaps (the once I chose you saw cycled above), and now we can also cycle interpolation algorithms. Here is a cycling of all of them, using the same colormap as the above Matplotlib image:

{:.center}
![Interpolation Cycling](/images/cycling interpolation.gif#center)
*Cycling through the various interpolation algorithms. SciPy is the algorithm used by the Matplotlib approach.*

The interpolation algorithm used is shown in the white text at the top of the image. Of note, cycling in this way allows us to us simplistic algorithms that are pretty much the basic raw data (useful in some cases to see what's actually going on before interpolation). Also, the last two interpolation algorithms used are based in part on the Matplotlib approach. The first of them, Scipy, uses exactly the same Scipy-based algorithm the Matplotlib approach used. As you can see in this gif though, using it can be a bit slower and prone to errors like the color glitch here. To gain the clearer quality of the Scipy approach but the speed of OpenCV the Scipy/CV2 approach at the end uses Scipy to scale up partially, and then OpenCV to scale the rest of the way.

#### Other Options
Finally, a few other simple options wer added.

- The temperature units shown in the text of the image (which are relative by the way, not absolute) can be toggled between Fahrenheit and Celsius.
- Simple filtering can be turned on. I tested a number of filtering algorithms but not many make much difference; the best I could find I left here, but the impact is minimal.
- Snapshot saving - When moving around the house evaluating, it's useful to be able to take pictures from the video, so snapshots can be saved.
- Finally, exiting can be annoying if the terminal is behind the video, as you need to move the video to reach the terminal, so Esc is set to shut the script down.

All of these options can be controlled while the video is running using the following keys:

Esc - Exit and Close.
S - Save a Snapshot of the Current Frame
X - Cycle the Colormap Backwards
C - Cycle the Colormap forward
F - Toggle Filtering On/Off
T - Toggle Temperature Units between C/F
U - Go back to the previous Interpolation Algorithm
I - Change the Interpolation Algorithm Used

### OpenCV Version - Web Server

## Usage



For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).
