import numpy as np
from readlif.reader import LifFile


def get_brightestZ(lif_input_path, channel):
    """
    This function calculates the three brightest neighboring z-stacks for each mosaic tile in an image.

    Parameters:
    lif_input_path (str): The path to the .lif file containing the image.
    channel (int): The channel number to consider for calculating brightness.

    Returns:
    list: A list of dictionaries containing the brightest z-stack information for each mosaic tile.
          Each dictionary contains the mosaic tile index, z-stack index, channel number, and intensity.
    """
    
    # Get the image from the .lif file
    img = LifFile(lif_input_path).get_image(0)

    # Initialize a data structure to hold the brightest z-stack information for each mosaic tile
    brightest_info = [{'m': None, 'z': None, 'channel': None, 'intensity': -1} for _ in range(img.dims.m)]

    # Iterate through the mosaic tiles
    for m in range(img.dims.m):
        # Iterate through the z-stacks for each mosaic tile
        for z in range(img.dims.z - 2):
            # Get the z-slices for this mosaic tile
            z_slice1 = img.get_frame(z=z, t=0, c=channel, m=m)  # Assuming the first time point and first channel
            z_slice2 = img.get_frame(z=z + 1, t=0, c=channel, m=m)
            z_slice3 = img.get_frame(z=z + 2, t=0, c=channel, m=m)

            # Calculate the brightness/intensity of this z-stack
            intensity = (np.mean(z_slice1) + np.mean(z_slice2) + np.mean(z_slice3)) / 3

            # Update if this is the brightest z-stack for this mosaic tile so far
            if intensity > brightest_info[m]['intensity']:
                brightest_info[m]['channel'] = channel
                brightest_info[m]['m'] = m
                brightest_info[m]['z'] = z
                brightest_info[m]['intensity'] = round(intensity, 4)

    return brightest_info
