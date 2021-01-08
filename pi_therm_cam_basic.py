##################################
# MLX90640 Test with Raspberry Pi
##################################
#
import time,board,busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt
import logging, configparser

# Manual Params
DEBUG_MODE=True

# Set up Logger
if DEBUG_MODE:
    logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(name)s:%(lineno)d] %(message)s',level=logging.DEBUG)
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
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ # set refresh rate

def c_to_f(temp:float):
    """ Convert temperature from C to F """
    logger.debug(f'Converting {temp} Celcius to Fahrenheit')    
    return ((9.0/5.0)*temp+32.0)

# print out the average temperature from the MLX90640
def print_mean_temp():
    """
    Get mean temp of entire field of view. Return both temp C and temp F.
    """
    frame = np.zeros((24*32,)) # setup array for storing all 768 temperatures
    while True:
        try:
            mlx.getFrame(frame) # read MLX temperatures into frame var
            break
        except ValueError:
            continue # if error, just read again
    
    temp_c = np.mean(frame)
    temp_f=c_to_f(temp_c)
    print('Average MLX90640 Temperature: {0:2.1f}C ({1:2.1f}F)'.format(temp_c,temp_f))
    return temp_c, temp_f

def simple_camera_read():
    mlx_shape = (24,32)

    # setup the figure for plotting
    plt.ion() # enables interactive plotting
    fig,ax = plt.subplots(figsize=(12,7))
    therm1 = ax.imshow(np.zeros(mlx_shape),vmin=0,vmax=60) #start plot with zeros
    cbar = fig.colorbar(therm1) # setup colorbar for temps
    cbar.set_label('Temperature [$^{\circ}$C]',fontsize=14) # colorbar label

    frame = np.zeros((24*32,)) # setup array for storing all 768 temperatures
    t_array = []
    while True:
        t1 = time.monotonic()
        try:
            mlx.getFrame(frame) # read MLX temperatures into frame var
            data_array = (np.reshape(frame,mlx_shape)) # reshape to 24x32
            therm1.set_data(np.fliplr(data_array)) # flip left to right
            therm1.set_clim(vmin=np.min(data_array),vmax=np.max(data_array)) # set bounds
            cbar.on_mappable_changed(therm1) # update colorbar range
            plt.pause(0.001) # required
            fig.savefig(output_folder + 'mlx90640_test_fliplr.png',dpi=300,facecolor='#FCFCFC', bbox_inches='tight') # comment out to speed up
            t_array.append(time.monotonic()-t1)
            print('Sample Rate: {0:2.1f}fps'.format(len(t_array)/np.sum(t_array)))
        except ValueError:
            continue # if error, just read again

if __name__ == "__main__":
    # print_mean_temp()
    simple_camera_read()