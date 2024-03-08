import numpy as np
from PIL import Image
import os
import shutil
from readlif.reader import LifFile


def merge_z_stack(lif_input_path, brigthes_info):
    """
    Merge a z-stack of images into a single image using maximum intensity projection.

    Args:
        lif_input_path (str): Path to the .lif file containing the z-stack.
        brigthes_info (list): List of dictionaries containing information about each mosaic tile.

    Returns:
        None
    """

    # Get the image from the .lif file
    img = LifFile(lif_input_path).get_image(0)

    tile_ZProjection = []

    # Iterate through the mosaic tiles
    for m_section in brigthes_info:

        # Load slices as numpy arrays for intensity comparison
        z_slice1_array = np.array(img.get_frame(z=m_section['z'], t=0, c=m_section['channel'], m=m_section['m']))
        z_slice2_array = np.array(img.get_frame(z=m_section['z']+1, t=0, c=m_section['channel'], m=m_section['m']))
        z_slice3_array = np.array(img.get_frame(z=m_section['z']+2, t=0, c=m_section['channel'], m=m_section['m']))

        # Combine arrays into a single array for maximum intensity projection
        combined_array = np.maximum.reduce([z_slice1_array, z_slice2_array, z_slice3_array])

        # Convert the result back to an image
        mip_image = Image.fromarray(combined_array)
        tile_ZProjection.append(mip_image)

    # Extract image name from lif_input_path
    img_name = lif_input_path.split('/')[2].split('.')[0]
    output_path = 'out/tiles/'
    output_file = img_name + '/'

    # Create output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output_path = output_path + output_file

    # Check if output directory already exists
    if os.path.exists(output_path):
        print("Folder ", output_path, " already exists")
        overwrite = input("Do you want to overwrite the folder? (y/n) ")
        if overwrite.lower() == 'y':
            shutil.rmtree(output_path)
            os.makedirs(output_path, exist_ok=True)  # Use os.makedirs() to avoid the previous issue
            for i, img in enumerate(tile_ZProjection):
                filename = f"tile_{i:02d}.png"  # This formats i with a leading zero if it's a single digit
                img.save(os.path.join(output_path, filename))
        else:
            print("Tiles not saved")
            return None
    else:
        os.makedirs(output_path, exist_ok=True)  # Use os.makedirs() to avoid the previous issue
        for i, img in enumerate(tile_ZProjection):
            filename = f"tile_{i:02d}.png"  # Use the same formatting here
            img.save(os.path.join(output_path, filename))
    return None