#!/usr/bin/python3
from sys import platform

def c_to_f(temp:float):
    """ Convert temperature from C to F """  
    return ((9.0/5.0)*temp+32.0)

def on_pi():
    """
    Check to see if we're running on the pi
    """
    # If we're on linux
    if platform=='linux':
            #Check if we're on a pi processor (we don't check for the pi name as the user may have renamed it PumpkinPie or the like...)
            import os
            return os.uname()[4][:3]=='arm'
    else:
        print("Code not running on pi")
        return False