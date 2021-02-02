
# Imports here to enable access to these functions from the library import without having to import those files.
# Effectively using this init in the same manner as a C header file. If there's a more pythonic way to do this, it should change to that.
from pithermalcam.pi_therm_cam import pithermalcam
from pithermalcam import web_server


def test_camera():
    """Check for an average temperature value to ensure the camera is connected and working."""
    try:
        thermcam = pithermalcam()  # Instantiate class
        temp_c = None
        temp_f = None
        temp_c, temp_f = thermcam.get_mean_temp()

        print("Camera seems to be connected and returning a value:")
        print('Average MLX90640 Temperature: {0:2.1f}C ({1:2.1f}F)'.format(temp_c,temp_f))
        print('To verify it\'s working, change the average temperature')
        print('(e.g. by hold your hand over the camera) and run again to verify that the average temperature has changed.')
    except ValueError as e:
        if str(e) == 'No I2C device at address: 0x33':
            print("ERROR: Camera not found. There seems to be no device connected to I2C address 0x33.")
    except Exception as e:
        print("Camera didn't seem to work properly. Returned the following error:")
        raise(e)


def display_camera_live(output_folder:str = '/home/pi/pithermalcam/run_data/'):
    """Display the camera live onscreen"""
    thermcam = pithermalcam(output_folder=output_folder)  # Instantiate class
    thermcam.display_camera_onscreen()


def stream_camera_online(output_folder:str = '/home/pi/pithermalcam/run_data/'):
    """Start a flask server streaming the camera live"""
    # This is a clunky way to do this, the better approach would likely to be restructuring web_server.py with the Flask Blueprint approach
    # If the code were restructure for this, the code would be much more complex and opaque for running directly though
    web_server.start_server(output_folder=output_folder)

# Add attributes to existing pithermalcam object
setattr(pithermalcam, 'stream_camera_online', stream_camera_online)
