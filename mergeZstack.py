import numpy as np
from PIL import Image
import os
import shutil
from readlif.reader import LifFile


def merge_z_stack(lif_input_path, brigthes_info):
    print("Merging images")

    #get the image
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

    print("Images merged")
    #extract image name from img_input
    img_name = lif_input_path.split('/')[2].split('.')[0]
    output_path = 'out/tiles/'
    output_file = img_name + '/'
    
    
    # if save images in new folder, if folder exists, ask user if you want to overwrite
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output_path = output_path + output_file

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
        print("Creating folder ", output_path)
        os.makedirs(output_path, exist_ok=True)  # Use os.makedirs() to avoid the previous issue
        print("Saving tiles...")
        for i, img in enumerate(tile_ZProjection):
            filename = f"tile_{i:02d}.png"  # Use the same formatting here
            img.save(os.path.join(output_path, filename))

    print("Tiles saved")
    return None