import numpy as np
from PIL import Image
import os

def fit_dnd_map(tv_size, table_grid_size, image_grid_size, original_image_path, saved_image_path):

    namepieces = ['PitPub','Vol4','Vol5','Vol6']
    gridsizes = [(23,20),(22,33),(30,30),(22,30)]

    for i in range(0, np.size(namepieces)):
        if namepieces[i] in original_image_path:
            print(i)
            image_grid_size = gridsizes[i]
            print(image_grid_size)
            
    # Extract parameters
    tv_width_px, tv_height_px = tv_size
    tv_grid_width, tv_grid_height = table_grid_size
    input_grid_width, input_grid_height = image_grid_size
    
    # TV dimensions in mm (using the given pixel density)
    tv_width_mm = tv_width_px / 3.2
    tv_height_mm = tv_height_px / 3.2

    # Calculate individual cell size
    cell_width_mm = tv_width_mm / tv_grid_width
    cell_height_mm = tv_height_mm / tv_grid_height
    cell_width_px = int(cell_width_mm * 3.2)
    cell_height_px = int(cell_height_mm * 3.2)

    # Load the D&D image
    dnd_map = Image.open(original_image_path)

    # Resize the image to match the desired grid size
    resized_dnd_map = dnd_map.resize((cell_width_px * input_grid_width, cell_height_px * input_grid_height))

    # Rotate the image if necessary
    resized_dnd_map = resized_dnd_map.rotate(90, resample=Image.BICUBIC, expand=True)

    # Create a new black image with the dimensions of the TV
    tv_image = Image.new('RGB', (tv_width_px, tv_height_px))

    # Calculate the position to place the D&D map
    x = (tv_image.width - resized_dnd_map.width) // 2
    y = (tv_image.height - resized_dnd_map.height) // 2

    # Paste the D&D map onto the TV image
    tv_image.paste(resized_dnd_map, (x, y))

    # Save the new image
    tv_image.save(saved_image_path)

# Folder containing the original PNG files
original_folder = '/home/vasilii/OneDrive/PC2/Documents/DnD/Say Map!/Spelljammer/Session 32/Raw/'

#original_folder = '/home/vasilii/OneDrive/PC2/Documents/DnD/Say Map!/Spelljammer/'

# Folder containing the script (where the saved files will be placed)
saved_folder = './'

# Iterate through all files in the original folder
for filename in os.listdir(original_folder):
    print(filename)
    if filename.endswith('.jpg'):
        original_filepath = os.path.join(original_folder, filename)
        saved_filepath = os.path.join(saved_folder, filename)

        # Apply the fit_dnd_map function to the file
        fit_dnd_map((4096, 2160), (39, 22), (22, 30), original_filepath, saved_filepath)

