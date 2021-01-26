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
[![Image of House from Thermal Camera](/images/Passivhaus_thermogram_gedaemmt_ungedaemmt.png#center)](/PiThermalCam/images/Passivhaus_thermogram_gedaemmt_ungedaemmt.png)
*[Passivhaus Institut, CC BY-SA 3.0](http://creativecommons.org/licenses/by-sa/3.0/), via Wikimedia Commons*

Initially I researched buying or renting such a camera, but the buying options tend to start at [$200 for the basic smartphone version](https://www.flir.com/products/flir-one-gen-3/), and go up to nearly $1,000. My local Lowe's has such cameras for rent as well but they cost $50 for 24 hours!

I've long been a Raspberry Pi fan so when I saw that rental price I decided to see what options were available for the Pi. I quickly found the MLX90640 camera which costs only $60; at this price I figured I'd get a cool gadget to play with, be able to evaluate my house for leaks, and when I'm done I can use it as a security camera.

I would of course also need a raspberry pi and accompany equipment but I had some of that and would be able to reuse it all for other projects as well. This was also a great excuse to finally upgrade from the Pi 3B+ I had to a [Pi 4](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/).

Of note: The resolution on this camera is much lower so we'll never get pictures quite like the above, but a mere few years ago even the [best cheaper camera](https://www.adafruit.com/product/3538) had only an 8x8 resolution, which is nearly unusable for projects like this. Jumping up to 24x32 resolution of the MLX90640 is a 12-fold increase for about the same price! It seems we've finally reached the point where cheap homemade thermal cameras are worth buying.

The below guide is meant to be a start-to-finish overview of the parts, setup, install, and use of this project for any who want to do likewise or build on it further. I don't cover everything needed to work with a Raspberry Pi itself as there are plenty of other guides for that out there, but I try to touch on any and all pieces related to this project directly, at least to get it up and running.

This guide is pretty comprehensive, but if you just want to get up and running, the pieces related to setup and the OpenCV running types are all you need to get to a fully working camera fairly fast.

I also touch on a few pieces needed for development here, but if you're going to develop further I'd suggest looking at the original source articles as well; they cover the details of the code in more detail than I do here. I've also tried to leave comments in the code to make quite clear the sources of things and other information necessary to track what's going on and/or speed the learning curve for development.

#### Contents
{:.no_toc}
* This line is replaced at runtime by a Table of Contents of headers, excluding those headers followed by {:.no_toc} 
{:toc}

## Background

There were several similar projects already online, and I ended up taking pieces of two as my baseline, mixing and matching, and adding features like web streaming from a third source. The results of that work are placed here for others to use directly or as a baseline for further develoment. The code is also available in the Github Repo corresponding to this page (link at top). The license is also included there and is an AGPL-3.0 License, so if you make changes and publish, you'll need to publish the code with it.

Thanks are owed to those three other projects: namely, Joshua Hrisko's article at Maker Portal, [High Resolution Thermal Camera with Raspberry Pi and MLX90640](https://makersportal.com/blog/2020/6/8/high-resolution-thermal-camera-with-raspberry-pi-and-mlx90640),  Валерий Курышев's article under the name Walker2000 at Habr, [Making a DIY thermal camera based on a Raspberry Pi](https://habr.com/en/post/441050/), and Adrian Rosebrock's article [OpenCV – Stream video to web browser/HTML page](https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/). Their work was a BIG step forward as a starting point.

_[Back to Table of Contents]_(#contents)
## Parts Required

{:.center}
[![Raspberry Pi 4](/images/Raspberry_Pi_4_Model_B_-_Side.jpg#center)](/PiThermalCam/images/Raspberry_Pi_4_Model_B_-_Side.jpg)
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

**Other Things you might need:**
- Portable battery with output ~ 3 Amps
- Screen for the Raspberry Pi

If you're going to be walking around your house, or outside it, you'll want some way to see the camera output live. As such, you'll probably need a portable battery for the device and, if you're not going to stream the video over your WIFI (or your pi will go outside of internet range), you'll want a screen to attach to the Pi.

I went with the Wifi option so I can't speak to screens, but I'd imagine any of the many Pi-specific screens would be fine for this.

On the battery, the Pi 4 draws around 3 Amps so you'd want any backup battery you have which can feed a USB-C connection with 3 Amps. I had a battery I use for my phone while traveling that worked great. You could try one with less power than this; just be aware that even if it runs it might be a bit slower.

_[Back to Table of Contents]_(#contents)
## Hardware Setup

{:.center}
[![Wiring Setup](/images/mlx90640_rpi_wiring_diagram_w_table.png#center)](/PiThermalCam/images/mlx90640_rpi_wiring_diagram_w_table.png)
*[Image by Joshua Hrisko / Maker Portal, copied with permission and thanks](https://www.raspberrypi.org/products/raspberry-pi-universal-power-supply/)*

Most of the physical setup is straightforward. The one piece specific to this project is wiring the camera to the Pi itself, and luckly for us, Josh at Maker Portal has made the perfect picture (above) for this and kindly agreed to let me put it here too.

The image shows where the camera connects to the Pi using the appropriate power and I2C pins. In my particular case I had a fan on the ground pin shown in this so I needed to move the ground wire to another ground on the Pi, but you can find another ground as needed in the [GPIO pinout diagrams](https://www.raspberrypi.org/documentation/usage/gpio/) available in many places online.

Below is a picture of my device in final form. You can see the case I used (but would not recommend; better to get one a tad more open and with a variable speed fan) and the fact that I initially bought a Stemma connector with male ends meant I had to solder those to other wires to connect to the Pi. If you buy the right pieces the first time yours will look cleaner than this.

I found taping the camera to the case an easy way to make using the device simpler to work with.

{:.center}
[![Assembled Device](/images/assembled device.jpg#center)](/PiThermalCam/images/assembled device.jpg)
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
[![Baudrate Change](/images/baudrate change.gif#center)](/PiThermalCam/images/baudrate change.gif)
*Section of /boot/config.txt after baudrate change.*

Save the file and reboot the device when you're done.

Note: In the first article I referenced, baudrates much higher than 400k were apparently tested; as high as 1M. I tested some higher rates but got many more errors at these levels. Running at higher rates also increases the risk of overheating as the maximum supported speed is [apparently 400k](https://raspberrypi.stackexchange.com/questions/108896/what-is-rpis-i2c-maximum-speed#:~:text=The%20maximum%20supported%20speed%20is%20400%20Kb%2Fs.). When I switched to the OpenCV approach (discussed below), 400k was fast enough to be usable. Since I want to reuse my Pi for other projects or as a security camera long term I stuck with the 400k. If you want the Matplotlib approach to work faster, as it did for the writer of that first article, this is likely what you'd need to change; just make sure you have good heat management of your Pi in doing so. My choice to stick with only 400k is likely why that approach is so slow for me, and is thus why the OpenCV approach is the one I mainly use.

 **Connection Verification**

Once the above steps are done and your device is connected you can check to ensure the camera is visible to your pi. Run the command `sudo i2cdetect -y 1` and you should see a result like the below, indicating the camera is visible at the 0x33 address.

{:.center}
[![I2C Camera Detected](/images/i2c detected.gif#center)](/PiThermalCam/images/i2c detected.gif)
*The Raspberry PI registers the camera present at address 33.*

Of note: The basic datasheet is available at Digikey for the [110 Degree Camera Version](https://media.digikey.com/pdf/Data%20Sheets/Adafruit%20PDFs/4469_Web.pdf) and the [55 Degree Version](https://media.digikey.com/pdf/Data%20Sheets/Adafruit%20PDFs/4407_Web.pdf). In both cases though the underlying camera device itself has the [same datasheet](https://www.melexis.com/-/media/files/documents/datasheets/mlx90640-datasheet-melexis.pdf), which shows that register 33 is the correct address.

**IDE Setup for Development**

If you're not going to run simply from the icons or script, you'll likely will want an IDE in order to look at and work with the python code. The Raspberry Pi comes with several now; if you installed the Raspbian version with recommended software you can find them in the Programming section of the menu. In my case though, I love Visual Studio Code and it's now supported on the Pi!! Straightforward install instructions are available at [PiMyLifeUp](https://pimylifeup.com/raspberry-pi-visual-studio-code/). Also, if you want a faster development experience you can install VS Code on your local machine, enable and set up SSH on the Pi (tutorials on this easy to find), and then use the remote development extension from your local VSCode. This was actually the best dev experience I found; the only down side is that running in this way will, in some approaches, throw errors because you don't have a display. As such I did 90% of my development via remote SSH and the remaining 10%, where I needed to have live video on the Pi itself, either directly in the terminal on the Pi or in VSCode on the Pi.

None of this is required, but if you find yourself looking to develop this project further, I found this setup to be the best.

_[Back to Table of Contents]_(#contents)
## Library Installation

After the prereq setup, clone the Git repo to your Pi. Clone it into your default (pi) folder to mirror my setup and avoid needing extra adjustments. This can be done by opening a terminal, making sure you're in the pi folder, and typing `git clone https://github.com/tomshaffner/PiThermalCam.git`.

There are three approaches for running the camear. All three are python 3 scripts so if you're comfortable with running python code manually or via an IDE you can just execute them. Details outlined below.

For convenience I also created a desktop icon for each approach; those three icons are in the templates folder and can be copied to your Raspbian desktop. Depending on how they downloaded you may need to make them executable, and they only work if you've installed this library in pi/pithermalcam/; otherwise you'll have to update the links.

_[Back to Table of Contents]_(#contents)
## Usage - The Three Approaches

There are three approaches or methods used in this library.

**Matplotlib:** The first, using Matplotlib, is based off the previously mentioned [article by Joshua Hrisko](https://makersportal.com/blog/2020/6/8/high-resolution-thermal-camera-with-raspberry-pi-and-mlx90640). The picture colormapping and interpolation used in this approach is quite good, but it requires the baudrate to be well over the recommended limit to function as a reasonable rate. I was lucky to get a picture a second at the 400k baudrate. I would recommend starting with this approach to perform tests on your camera to make sure it's working, but once you've verified that it's probably better to move on to the other methods.

**OpenCV:** The second approach uses OpenCV and runs MUCH faster. As I'll discuss below though, I found the colormaps and interpolation of Matplotlib superior, and so I ended up importing those pieces of the Matplotlib into this approach.

**OpenCV Web Server:** The first two approaches run locally and display video output on the Pi directly. If you have a screen for the Pi or you're remoting into it via Remote Desktop or VNC this works fine. If you're walking around your house trying to use Remote Desktop on your phone to see the video output though, this can be a pain. As such I took the second approach above and rebuilt it into a Flask webserver version. If you start the webserver you'll see an IP Address printed out, and you can load that IP via a web browser on any computer in the network to see and control the video. For me, this was the more reliable/robust solution in practice.

All three versions are discussed in more detail below.

### Matplotlib Version

The Matplotlib version can be found in the examples folder under the name matplotlib_therm_cam.py. It has several running modes which can be switched via the number at the bottom of the file, as visible here:
{:.center}
[![Matplotlib Modes](/images/matplotlib_modes.png#center)](/PiThermalCam/images/matplotlib_modes.png)
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
[![Cycling Colormaps](/images/cycling colormaps.gif#center)](/PiThermalCam/images/cycling colormaps.gif)
*Different colormaps make it easier to see important areas*

Note: It's hard to see in the compressed gif here, but the colormap in use is shown in the white text at the top.

The contrast in the image also makes a big difference. E.g. as I move out of the picture in this clip, the smaller temperature differences in the image become much more visible, making the impact of the windows much clearer. Again, different colormaps can help highlight areas of interest here too.

{:.center}
[![Impact of Temperature Range on image](/images/turning_to_windows_only.gif#center)](/PiThermalCam/images/turning_to_windows_only.gif)
*As I leave the image, my bodyheat being removed makes the temperature difference between the windows and wall more visible*

#### Interpolation Algorithms
Also, the process of blowing the image up larger requires zoom/interpolation algorithms of various sorts. E.g. here is a picture of me with the Matplotlib approach before interpolation (i.e. just the raw data as an image):

{:.center}
[![Matplotlib Raw Data Wave](/images/Matplotlib Simple Wave.gif#center)](/PiThermalCam/images/Matplotlib Simple Wave.gif)
*The raw temperature data as an image.*

Now change the color scheme and interpolate for a cleaner/clearer picture:

{:.center}
[![Matplotlib Wave](/images/Matplotlib Wave.gif#center)](/PiThermalCam/images/Matplotlib Wave.gif)
*The data interpolated. Note the clarity of the border between my body and the surroundings.*

Apart from having evidence that my hands aren't just feeling cold but actually ARE cold, this image highlights particularly how good the Matplotlib approach (which uses the SciPy library for interpolation) sets the coloring in a way that makes edges clear. The white line surrounding the red of my body makes the boundary much more visible.

OpenCV, in contrast, has a number of interpolations algorithms, but most of them don't function as well with boundaries like this, and the default colormaps weren't as useful. As a result I used the cmapy library to import a handful of Matplotlib colormaps (the ones chosen are visible in the cycling colormap gif above), and now we can also cycle interpolation algorithms. Here I cycle through all of them, using the same colormap as the above Matplotlib image:

{:.center}
[![Interpolation Cycling](/images/cycling interpolation.gif#center)](/PiThermalCam/images/cycling interpolation.gif)
*Cycling through the various interpolation algorithms. SciPy is the algorithm used by the Matplotlib approach.*

The interpolation algorithm used is shown in the white text at the top of the image. Of note, cycling in this way allows us to us simplistic algorithms at the start that are showing pretty much just the raw data (useful in some cases to see what's actually going on before interpolation). Also, the last two interpolation algorithms used are based in part on the Matplotlib approach. The first of them, Scipy, uses exactly the same Scipy-based algorithm the Matplotlib approach used. As you can see in this gif though, using it can be a bit slower or glitchy. To gain the clearer quality of the Scipy approach but the speed of OpenCV the Scipy/CV2 approach at the end uses Scipy to scale up partially, and then OpenCV to scale the rest of the way. This seems to work almost as well as Scipy alone, but without as much of a speed hit.

####  Other Options
Finally, a few other simple options were added.

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

The thinking here is simple: S for Save, T for Temp, F for Filter, C for Colormap, I for Interpolation, and in those last to cases the key just to the left to go back.

#### Viewing remotely on the Pi

If, like me, you don't have a screen for your Raspberry Pi, you'll likely be remoting into the Pi for the two options discussed above. Both show live video on the screen and you'll want to see that as you move around. I mentioned remoting in via SSH for VS Code development earlier, but for viewing the video I used two different approaches: the first was VNC Viewer, which comes with the Raspberry Pi and can be [enabled in Raspbian](https://www.raspberrypi.org/documentation/remote-access/vnc/). This is traditionally how I've connected to my Pi.

On the advice of some online forums however, I also tested the Remote Desktop program included in Microsoft Windows. As the forums had suggested, I found this connection to be a bit more stable and reliable when trying to view live video on the Pi and simultaneously moving around the wifi network. Connecting is a simple as opening remote desktop (often pre-installed on Windows and available in the Windows store and for Android and I believe Mac devices) and typing in the IP address and username of your Pi.

These two options were enough to cover my need for this approach, and I'd recommend others who are doing this consider these options.

If, however, this approach seems at times cumbersome or more error prone, the web server version might be for you:

### OpenCV Version - Web Server

After testing the other two options I came to the conclusion that a better approach for using the camera via the internet would be to stream the video live to a webpage where multiple other computers or phones could all easily pull it up in a browser. Fortunately there was a similar project online in the guise of a [motion-detecting camera project](https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/) which I could use as a baseline for this. As such, the OpenCV code is connected in this piece to a basic Flask server which streams the video live to any computer on the network.

In the process of making this conversion, the OpenCV code was also refactored into a cleaner object-oriented class to be cleaner and better encapsulated. If others wish to develop this project further or use the camera functionality in another project I'd suggest starting with this class for a cleaner, simpler, and self-contained entry point.

Furthermore, the flask webpage that connects to this was set up to enable all the functionality of the various keyboard commands discussed in the OpenCV section via buttons on the webpage. This allows multiple browser windows or machines to all connect to the video stream at the same time and any can control the colormap, interpolation method, temperature units, save snapshots, etc.

To initiate this, either click the "Run Flask Thermal Camera" icon, if you set it up, or initiate the web server in python 3 with `python3 web_server.py`. When it begins it will show the local IP address to log onto:

{:.center}
[![The Flask-server starting up](/images/flask ip address.png#center)](/PiThermalCam/images/flask ip address.png)
*The web server code displays the address to connect to before starting the Flask server.*

In this case the user simply opens a browser and goes to 192.168.86.22:8000 in order to pull up the resulting webpage with the live feed:

{:.center}
[![The Flask-based Live Webpage](/images/flask_webpage.png#center)](/PiThermalCam/images/flask_webpage.png#center)
*The flask-based server allows web browsers to view and control the live video feed.*

The IP address for this can also be fixed by setting your router to reserve an IP address for your Pi.

Of note: This address will only be accessible from inside the same network. If you wish to set this up for external access research how to make a flask server accessible online.

#### Image Saving Note

Several of these features include the option to save snapshots of the video feed. The save location is determined by the Config file included in the project. It defaults to the location /home/pi/pithermalcam/run_data/. If this needs to be changed it can be updated in the config file directly.

_[Back to Table of Contents]_(#contents)
## Results

Having put all this together, the big outstanding question is, how does it work? Is it useful enough to identify insulation issues?

It is again worth noting that a higher resolution (i.e. much more expensive) camera would make this much easier. The lower resolution means it's harder to figure out what a hot or cold spot is at times, and in my use I found it was both helpful and, now and then, necessary to change the color map and interpolation scheme as I was using the camera to figure out what was going on.

This is another instance in which the 110 Degree camera viewing angle is also harder to work with; if the camera is pointed at a wall, the viewing range is so wide that it's sometimes hard to tell what is what. In a number of cases it was necessary to get very close to something to figure out what was going on. Sometimes it was also useful to hold the camera still and have someone put their hand on a physical object to determine what something was. (e.g. this red section is that angle of the wall there I think, can you put your hand on it to make sure?)

The 55 Degree camera would, again, likely be much better for this. Having the same number of sensors over a smaller viewing range would give a more nuanced view of what's happening, and would also allow the camera to be more useful at a greater distance.

This ultimately just means that the 110 Degree camera is a bit more work though, the end result can still be quite useful. As it need be used only once for the thermal evaluation though the extra work isn't a huge issue. And, as I said earlier, for longer term security camera usage the 110 Degree camera is likely much better as it can cover a much wider area when watching for the presence of a warm body.

**Initial Results**
To begin with, some basic pictures were taken of the workstation. Below are real images with a corresponding thermal image to compare for a few of these. Click an image to enlarge.

Here the heat from the screen and laptop is visible fairly clearly.
{:.center}
[![Screen and Laptop](/images/screen_and_laptop.jpg#center)](/PiThermalCam/images/screen_and_laptop.jpg#center)
*Image of a screen and laptop, normal and thermal.*

Here a ceiling light and windows in the background show the heat of the former and the coolness of the latter.
{:.center}
[![Light and Windows](/images/lamp_and_windows.jpg#center)](/PiThermalCam/images/lamp_and_windows.jpg#center)
*A light and windows showing heat and cold respectively.*

To play around with the camera a bit, a number of pictures were taken around a running sink, where the water temperature could be varied. Here's the sink via a normal camera:
{:.center}
[![Sink with running water](/images/sink.jpg#center)](/PiThermalCam/images/sink.jpg#center)
*A sink with running water.*

And here's the sink with the water at cold and hot settings:
{:.center}
[![Thermal Sink](/images/thermal_sink.jpg#center)](/PiThermalCam/images/thermal_sink.jpg#center)
*Sink with cold and hot running water respectively.*

Then I took my hand and placed it in the image under the water. In the right image I ran the cold water over the palm of my hand (it also ran down my little finger) and then took a thermal picture; the cold from the water makes the heat from the center of my hand invisible, or even colder than the background. In the left image I then covered my entire hand in cold water and held it behind a stream of hot water; the end result shows the stream visible and my arm down to a bit above the wrist. Beyond that my hand is completely invisible  where the cold water had covered it:
{:.center}
[![Invisible hand](/images/invisible_hand.jpg#center)](/PiThermalCam/images/invisible_hand.jpg#center)
*A hand covered in cold water, and a hand with cold water covering the palm only.*

Seeing this was interesting, and kind of cast in a different light all those movie or TV shows where someone is facing a thermal camera in some heist.

**Evaluating the House for Insulation**
The next question was, what heat problems are there in the house? I covered a lot more than just the below, but here are some highlights.

First, to evaluate the impact the curtains in my living room, I opened one of them; the cold of the door is clearly visible in the opened area:
{:.center}
[![Curtain](/images/curtain.jpg#center)](/PiThermalCam/images/curtain.jpg#center)
*The effect of curtains visualized.*

Note: The angle of these two pictures isn't exactly the same.

Next I went into the basement and took a number of pictures. Of particular interest here, the soil stack (black pipe carrying waste water out of the ceiling and into the wall) was the hottest item in this picture! I checked after and it turned out someone had taken a hot shower not too long before.
{:.center}
[![Soil Pipe Coming out of Ceiling](/images/pipe_part_one.jpg#center)](/PiThermalCam/images/pipe_part_one.jpg#center)
*Waste pipe coming out of the ceiling.*

Note: Again, the thermal picture and real picture are taken from slightly different angles here.

That waste pipe continues through the wall and into another basement room, and in that room the heat from that pipe is again the hottest thing around:
{:.center}
[![Soil Pipe Continuing](/images/pipe_part_two.jpg#center)](/PiThermalCam/images/pipe_part_two.jpg#center)
*Waste pipe continuing.*

I hope to do further testing of this pipe when it hasn't been used recently to see how much heat loss there is otherwise. It's still an open question whether this heat is just from the recent shower or if that pipe is always warm, indicating heat from the apartment above is being lost through it, in which case it might be worth insulating the pipe.

In the second room there's also insulation in the ceiling preventing heat loss through the floor of the apartment above. Evaluating sections of that insulation highlighted one section where the insulation between two particularly close joists is actually simply missing:
{:.center}
[![Insulation issues](/images/Insulation_Issues.jpg#center)](/PiThermalCam/images/Insulation_Issues.jpg#center)
*A section of insulation missing underneath a floor, and a hole in that insulation.*

Of note, not only is there greater heat in between those joists, but a small area of insulation in another section is also leaking heat, indicating it's either bunched wrong or there's a thin place that could use some patching. The entire ceiling here could use an evaluating to find other sections of insulation that are missing or leaking heat.

In the garage, there was some debate about whether the garage door itself was the major point of heat loss or if the cinderblock walls were just as bad. In particular, the cinderblock wall has a crack just to the left of the door, and it was thought that insulating the door itself might be a waste if the wall leaked just as much:
{:.center}
[![Garage Door](/images/garage_door.jpg#center)](/PiThermalCam/images/garage_door.jpg#center)
*Heat loss via the garage door.*

Here we can see that's not the case; the wall might be losing heat, but the door is losing it MUCH faster. If that crack makes a difference it's too small even to see here.

Note: The temperature differential shown is only about 14 Degrees F. The temperatures in the text are relative so the absolute value is almost certainly wrong, but the difference between them should be ballpark correct and represents the differential between the hottest and coldest parts of the picture. Note that the walls immediately around the garage door ARE cooler than the hottest part of the picture (dark red in the ceiling), but those walls are still warmer than the door itself. As such, the theory about the wall losing heat is likely correct, but the greater heat loss through the door would indicate that either a new door or insulation for it would, indeed, help keep the space warmer.


While looking at that garage picture I was a bit surprised at how hot the ceiling was. Particularly interesting, if the camera turned up a bit, a beam of heat could be seen running down the ceiling (left pic below). At first I thought maybe this was the chain and motor for the garage, but if I took a picture when the garage door hadn't been opened for a day the beam of heat was still there. Furthermore, if I turned the camera up to cover the entire ceiling, the beam of heat ran all along it, even the sections with no chain or motor. Turned high enough to exclude the door itself, the beam of heat in the middle of the ceiling, surrounded by cooler areas on either side, became obvious (right picture below):
{:.center}
[![Ceiling above the garage door](/images/garage_ceiling.jpg#center)](/PiThermalCam/images/garage_ceiling.jpg#center)
*The ceiling above the garage door, showing poorly insulated*

This was one of the most useful insights from the entire project. The camera is seeing heat leaking through the center of the garage ceiling, while the ceiling looks completely blank and unchanged to the naked eye. Something is going on above the surface of the ceiling that is not visible.

In trying to figure out what might be causing this, first, an access panel nearby gives a bit of visibility in the direction of this ceiling and it seems there are two boards that cover the outside sections of the ceiling, but leave the middle section open. Second, it's believed, after asking around among those who were present during the last remodeling, that the heating duct for the apartment above runs directly through this section. Furthermore, at the time of installation this heating duct was installed without being insulated.

As such, it seems likely that some portion of the heat from this particular heating duct is, instead of being vented into the apartment above through the grate, leaking into the garage below. From there is goes right out the poorly insulated garage door, making for an overall heat loss for the entire area.

There's still a debate about whether the best solution for this is to insulate the duct itself or to insulate the garage door, continuing to lose heat from above into the garage but potentially making the garage a more comfortable space to work in during the winter months.

In either case though, the camera has already been deeply useful in figuring out what's going on and what to do about it.


There were other examples of the camera helping find holes or issues in the current insulation. What's shown here is already enough, however, to demonstrate the usefulness and efficacy of the MLX90640 for this purpose.

**Further use thoughts**
What's not shown here are pictures taken from the outside of the house of heat coming out. Some basic testing was done for this, but on the days in question this testing was limited due in part to concerns about water on the device (it was raining), and because the efficacy of those images was limited. The device itself worked fine from outside, and in a few cases identified much more clearly which windows are currently leaking much more heat than others, and which windows already seem to be high enough quality to not be an issue.

From outside however, the distances from the objects being considered become greater, and as a result the problems of having a lower resolution higher viewing angle camera become more apparent. This is one area where the 55 Degree viewing angle camera would likely be much better.

Also, the wifi in this particular house extends only so far from the building itself. As such, the method used here of streaming the video over wifi became more and more unstable the further from the building the camera was. With a better network connection or a screen attached to the Pi and the video being displayed locally on the screen (rather than via the web server approach) this method would be much easier. Pictures of this type will likely be quite useful as well in identifying other areas of heat loss for the house.

For purposes of this demo however, the above were considered sufficient to showcase the efficacy of the camera for this purpose.

_[Back to Table of Contents]_(#contents)
## Conclusion

While the MLX90640 will never provide pictures or video of the level of fidelity that some much more expensive professional cameras provide, what's shown here is more than enough to demonstrate the efficacy and usefulness of the camera both for entertainment purposes, as a security camera, and for a thermal evaluation of a house. The version of the camera with a narrower viewing angle (55 Degrees instead of 110) would likely be better for the thermal evaluation purpose but be of less value as a security camera.

Regardless though, it's clear that the market has now reached the point where affordable thermal cameras can be effectively used to evaluate the insulation quality of a house. This article, and the accompanying open source library on Github, are provided for others to get started quickly and easily in doing their own work, or to use as a springboard for further development of their own.

_[Back to Table of Contents]_(#contents)
## Further Development

There are a few next steps for development that have not (to date) been undertaken. Pull requests that complete these would be welcome:

1. Add double-click save option in local version: The web-version of the OpenCV code has been set up to enable saving not only via the 's' key, but also via double-clicking the image itself. This would be a particularly useful function on the local OpenCV version as well, as it would enable a touchscreen double-tap picture saving. Initial attempts to replicate the approach used in the web version didn't work in the local version, but it would be worth completing these.
2. Test OpenCV Pip Install: The above approach was used via the manual installation of OpenCV, but this approach is extremely cumbersome. Testing of the pip installation approach, both to verify it works and to compare the speed, would be extremely useful. If this did work the library would be switched to use it as the default install method, which would be far simpler and faster.
3. Convert library to pip-installable package: Related to 2), if pip install for all dependencies could be possible, the library could be easily converted to a package that could be hung on PyPI. This would enable those would bought the camera to wire it up, install the apt-get dependencies, and then install this library directly from PiPI and be up and running in minutes. A few steps would likely be necessary for this in addition to completing number 2 above:
  - Convert library to package (requirements.txt is already set up with this conversion in mind, once the pip-installed version of OpenCV is verified to work)
  - Set up scripts that copy icons to desktop and ensure they're executable
  - Update paths (in config file and icons) to reflect pip installation location
  - Determine if other methods are necessary for running Matlab, OpenCV local, and OpenCV Web version
4. Set up security camera mode: The web server version of the library can currently be used as a basic security camera version, but another mode could be added to do this more effectively. In particular, the article used to set up the web server version could be mirrored to check and see where movement is occurring in the frame and where the background is remaining unchanged. This could also then be set up to raise a warning of some sort when movement is detected.

Of note on this fourth point, the normal use of the camera indicates some measure of noise that's greater than a typical (non-thermal) camera experiences, so the approach used in the original article on this topic would likely need to be enhanced to allow for greater noise levels without triggering. Similarly, the fact that temperatures are shown in a relative way might impact how movement works. And finally, temperature fluctuations of the general environment throughout the day would need to be accounted for to avoid beams of sun or the simple onset of a wind or night being viewed as motion.

_[Back to Table of Contents]_(#contents)
## Issue Reporting

Where issues, problems, or concerns come up, they can be reported in the [Github repository that corresponds to this page](https://github.com/tomshaffner/PiThermalCam). Bugs or problems can be entered as [Issues](https://github.com/tomshaffner/PiThermalCam/issues), and general questions or discussion topics can be created in the [Discussions](https://github.com/tomshaffner/PiThermalCam/discussions) section. A fast response from the author is not guaranteed, but I will do my best to support/respond as time allows.