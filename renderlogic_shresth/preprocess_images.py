import os
import shutil
from PIL import Image

def rename_files_in_directory(directory, character, state, direction, flip):
    # Ensure directory exists
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return
    
    # Create new directory name
    parent_dir = os.path.dirname(directory)
    new_directory = os.path.join(parent_dir, f"{os.path.basename(directory)}_renamed")
    os.makedirs(new_directory, exist_ok=True)
    
    # Get all PNG files in the directory
    files = sorted([f for f in os.listdir(directory) if f.lower().endswith('.png')])  # Keep order as per natural sorting
    
    for frame_number, file_name in enumerate(files):
        old_path = os.path.join(directory, file_name)
        
        if os.path.isfile(old_path):  # Ensure it's a file
            new_name = f"{character}_{state}_{direction}_{frame_number+1}.png"
            new_path = os.path.join(new_directory, new_name)
            
            if flip:
                with Image.open(old_path) as img:
                    img = img.transpose(Image.FLIP_LEFT_RIGHT)
                    img.save(new_path)
            else:
                shutil.copy2(old_path, new_path)  # Copy file to new directory with new name
    
    print(f"Renamed files saved in: {new_directory}")

# Get user inputs
directory = input("Enter the directory path containing the files: ")
character = input("Enter the character name: ")
state = input("Enter the state: ")
direction = input("Enter the direction (e.g., ne, nw, s, etc.): ")
flip = input("Flip images? (True/False): ").strip().lower() == 'true'

rename_files_in_directory(directory, character, state, direction, flip)