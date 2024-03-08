from PIL import Image
import os


def stitch_images(images_path, overlap_percentage=0.1):
    """
    Stitch multiple images together to create a single panoramic image.

    Args:
        images_path (str): The path to the directory containing the images.
        overlap_percentage (float, optional): The percentage of overlap between adjacent images. Defaults to 0.1.

    Returns:
        None
    """
    # Correctly get the images sorted by filename
    filenames = sorted([f for f in os.listdir(images_path) if f.endswith('.png')], key=lambda x: int(x.split('_')[1].split('.')[0]))
    images = [Image.open(os.path.join(images_path, f)) for f in filenames]

    # Assuming all images have the same size
    width, height = images[0].size

    # Calculate overlap in pixels
    overlap_width = int(width * overlap_percentage)
    overlap_height = int(height * overlap_percentage)

    # Adjust dimensions for stitching, taking into account the overlap
    adj_width = width - overlap_width
    adj_height = height - overlap_height

    # Calculate the dimensions of the final image
    final_width = adj_width * 5 + overlap_width
    final_height = adj_height * 4 + overlap_height

    # Create the final image
    final_image = Image.new('RGBA', (final_width, final_height), (255, 255, 255, 0))

    # Iterate through the images and paste them in their correct positions
    for i, img in enumerate(images):
        # Calculate row and column for the current image
        col = i // 4
        row = i % 4

        # Calculate the position
        x_position = col * adj_width
        y_position = row * adj_height

        # Paste the image into the final image
        final_image.paste(img, (x_position, y_position), img if img.mode == 'RGBA' else None)

    # Create the output directory if it doesn't exist
    output_path = 'out/full_image/'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Save the final image
    img_name = images_path.split('/')[-1]
    final_image.convert('L').save(output_path + f"full_{img_name}.png")

    return None