from readlif.reader import LifFile
import numpy as np
from PIL import Image
import os



def get_brightestZ(img_input,channel):
    #get the image
    img = img_input.get_image(0)

    # Initialize img structure to hold the brightest z-stack (with the 2 next following) information for each mosaic tile
    brightest_info = [{'m':None,'z': None,'channel':None, 'intensity': -1} for _ in range(img.dims.m)]

    # Iterate through the mosaic tiles
    for m in range(img.dims.m):
        # Then, iterate through the z-stacks for each mosaic tile
        for z in range(img.dims.z-2):
            # Get the z-slice for this mosaic tile
            z_slice1 = img.get_frame(z=z, t=0, c=channel, m=m)  # Assuming the first time point and first channel
            z_slice2 = img.get_frame(z=z+1, t=0, c=channel, m=m)
            z_slice3 = img.get_frame(z=z+2, t=0, c=channel, m=m)
            # Calculate the brightness/intensity of this z-slice
            intensity = (np.mean(z_slice1)+np.mean(z_slice2)+np.mean(z_slice3))/3
            
            # Update if this is the brightest z-stack for this mosaic tile so far
            if intensity > brightest_info[m]['intensity']:
                brightest_info[m]['channel'] = channel
                brightest_info[m]['m'] = m
                brightest_info[m]['z'] = z
                brightest_info[m]['intensity'] = round(intensity,4)

    print('brightesZ evauated')
    return brightest_info


def merge_images(img_input, brigthes_info):
    print("Merging images")
    #get the image
    img = img_input.get_image(0)

    tile_ZProejction = []

    # Iterate through the mosaic tiles
    for m_section in brigthes_info:
        z_slice1 = img.get_frame(z=m_section['z']  , t=0, c=m_section['channel'], m=m_section['m'])
        z_slice2 = img.get_frame(z=m_section['z']+1, t=0, c=m_section['channel'], m=m_section['m'])
        z_slice3 = img.get_frame(z=m_section['z']+2, t=0, c=m_section['channel'], m=m_section['m'])

        max_width = max(z_slice1.width, z_slice2.width, z_slice3.width)
        max_height = max(z_slice1.height, z_slice2.height, z_slice3.height)

        new_image = Image.new('RGBA', (max_width, max_height), (255, 255, 255, 0))

        new_image.paste(z_slice1, (0, 0), z_slice1 if z_slice1.mode == 'RGBA' else None)
        new_image.paste(z_slice2, (0, 0), z_slice2 if z_slice2.mode == 'RGBA' else None)
        new_image.paste(z_slice3, (0, 0), z_slice3 if z_slice3.mode == 'RGBA' else None)

        tile_ZProejction.append(new_image)

    print("Images merged")
    #extract image name from img_input
    img_name = img_input.filename.split('/')[-1].split('.')[0]
    output_path = 'out/tiles/'
    output_file = img_name + '/'
    
    
    # if save images in new folder, if folder exists, ask user if you want to overwrite
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output_path = output_path + output_file

    if os.path.exists(output_path):
        print("Folder ",output_path, " already exists")
        overwrite = input("Do you want to overwrite the folder? (y/n)")
        if overwrite.lower() == 'y':
            for i, img in enumerate(tile_ZProejction):
                img.save(output_path + f"tile_{i}.png")
        else:
            print("Tiles not saved")
            return None
    else:
        print("Creating folder ",output_path)
        os.mkdir(output_path)
        print("Saving tiles...")
        for i, img in enumerate(tile_ZProejction):
            img.save(output_path + f"tile_{i}.png")

    print("Tiles saved")
    return None


def stitch_images(images_path, overlap_percentage=0.1):
    print("Stitching images")
    # Assuming the images are named 'tile_0.png', 'tile_1.png', ..., 'tile_19.png'
    # Load the first image to get the dimensions
    first_image_path = os.path.join(images_path, 'tile_0.png')
    first_image = Image.open(first_image_path)
    width, height = first_image.size

    # Calculate the overlap in pixels
    overlap_width = int(width * overlap_percentage)
    overlap_height = int(height * overlap_percentage)

    # Adjust the dimensions for stitching
    adj_width = width - overlap_width
    adj_height = height - overlap_height

    # Calculate the dimensions of the final image
    final_width = adj_width * 5 + overlap_width
    final_height = adj_height * 4 + overlap_height

    # Create a new image with the appropriate dimensions
    final_image = Image.new('RGB', (final_width, final_height))

    # Iterate over the image indices to place each image in its designated spot
    for i in range(20):  # Assuming 20 images numbered 0 to 19
        image_file_name = f'tile_{i}.png'
        image_file_path = os.path.join(images_path, image_file_name)
        img = Image.open(image_file_path)

        # Calculate row and column for the current image
        col = i % 5
        row = i // 5

        # Calculate the position
        x_position = col * adj_width
        y_position = row * adj_height

        # Paste the image into the final image
        final_image.paste(img, (x_position, y_position))


    img_name = images_path.split('/')[2]
    output_path = 'out/full_image/'
    output_file = img_name + '/'

    
    # if save images in new folder, if folder exists, ask user if you want to overwrite
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output_path = output_path + output_file

    if os.path.exists(output_path):
        print("Folder ",output_path, " already exists")
        overwrite = input("Do you want to overwrite the folder? (y/n)")
        if overwrite.lower() == 'y':
            img.save(output_path + f"full_{img_name}.png")
        else:
            print("Full image not saved")
            return None
    else:
        print("Creating folder ",output_path)
        os.mkdir(output_path)
        print("Saving images")
        img.save(output_path + f"full_{img_name}.png")

    print("Full image saved")
    return None




if __name__ == "__main__":
    #read file
    img = LifFile('../src/20231230_ID514_silence_IC_neuercfos.lif')
    channel = 0 #channel to use
    #get the brightest z-stack for each mosaic tile
    k = get_brightestZ(img,channel)
    #print(k)
    #merge the brightest z-stack for each mosaic tile
    merge_images(img,k)
    stitch_images('out/tiles/20231230_ID514_silence_IC_neuercfos/')
