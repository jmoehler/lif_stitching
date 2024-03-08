from brightestZ import get_brightestZ
from mergeZstack import merge_z_stack
from stitching import stitch_images
import os

def lif_processer(lif_input_path, channel):
    """
    Process the lif files in the specified directory. Main handler for the pipeline.

    Args:
        lif_input_path (str): The path to the directory containing the lif files.
        channel (int): The channel number to process.

    Returns:
        None
    """
    print('-----------------------------------')
    print("Hellloooooo there this is the lif_processer. I will process the lif files for you. Lean back and relax. I will keep you updated :)")
    print('If you have any questions/ problems,  please contact me at: jmm123@posteo.de')
    print('-----------------------------------')
    print()
    #check the number of .lif files in the directory
    num_files = len([f for f in os.listdir('./src') if f.endswith('.lif')])

    #add counter for the number of files processed
    counter = 0

    print(f"Number of files to process: {num_files}")
    print("lets get started...")

    # add list of processed files to keep track of the files processed and avoid reprocessing
    processed_files = []

    # Iterate over all files in the './src' directory
    for file in os.listdir('./src'):
        # Check if the file has a '.lif' extension
        if file.endswith('.lif'):
            # Extract the image name from the lif_input_path
            img_name = file.split('.')[0]
            # Check if the file has already been processed
            if img_name in processed_files:
                print(f"{img_name} has already been processed, it will be skipped.")
                continue    
            else:
                # Add the file to the list of processed files
                processed_files.append(img_name)
                counter += 1
                print(f"Processing file {counter} of {num_files}: {img_name}")

            # Construct the image path
            img = './src/' + file
            
            # Get the brightest z-stack for each mosaic tile
            brigthes_info = get_brightestZ(img, channel)
            
            # Merge the brightest z-stack for each mosaic tile
            merge_z_stack(img, brigthes_info)
            
            # Stitch the images for the current mosaic tile
            stitch_images('out/tiles/' + img_name + '/')
    print("All files have been processed. You can find the results in the 'out' directory. Have a nice day!")

