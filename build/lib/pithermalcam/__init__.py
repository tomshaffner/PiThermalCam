
# Imports here to enable access to these functions from the library import without having to import those files.
# Effectively using this init in the same manner as a C header file. If there's a more pythonic way to do this, it should change to that.
from pithermalcam.pi_therm_cam import pithermalcam
from pithermalcam import web_server

def test_camera_connected():
    """Check for an average temperature value to ensure the camera is connected and working."""
    thermcam = pithermalcam() # Instantiate class
    temp_c, temp_f = None
    temp_c, temp_f = thermcam.get_mean_temp

    if temp_c is None:
        raise ValueError("No value for temperature found; check your camera connection and try again.")
    else:
        print("Camera seems to be connected and returning a value:")
        print('Average MLX90640 Temperature: {0:2.1f}C ({1:2.1f}F)'.format(temp_c,temp_f))


def display_camera_live():
    """Display the camera live onscreen"""
    thermcam = pithermalcam() # Instantiate class
    thermcam.display_camera_onscreen()

def stream_camera_online():
    """Start a flask server streaming the camera live"""
    # This is a clunky way to do this, the better approach would likely to be restructuring web_server.py with the Flask Blueprint approach
    # If the code were restructure for this, the code would be much more complex and opaque for running directly though
    web_server.start_server()
