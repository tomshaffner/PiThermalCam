#!/usr/bin/python3
from sys import platform
import numpy as np

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


def to_rgba(self, x, alpha=None, bytes=False, norm=True):
    """
    Return a normalized rgba array corresponding to *x*.

    In the normal case, *x* is a 1-D or 2-D sequence of scalars, and
    the corresponding ndarray of rgba values will be returned,
    based on the norm and colormap set for this ScalarMappable.

    In either case, if *bytes* is *False* (default), the rgba
    array will be floats in the 0-1 range; if it is *True*,
    the returned rgba array will be uint8 in the 0 to 255 range.

    If norm is False, no normalization of the input data is
    performed, and it is assumed to be in the range (0-1).

    """

    # This is the normal case, mapping a scalar array:
    x = np.ma.asarray(x)
    if norm:
        x = self.norm(x)
    rgba = self.cmap(x, alpha=alpha, bytes=bytes)
    return rgba