import cv2
import numpy as np
import json
import os

def extract_sprites_from_spritesheet(image_path):
    # Load the sprite sheet with alpha channel
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError("Failed to load the image.")
    
    # Ensure the image has an alpha channel
    if image.shape[2] < 4:
        raise ValueError("Image does not contain an alpha channel.")
    
    # Extract the alpha channel
    alpha_channel = image[:, :, 3]
    
    # Threshold the alpha channel to create a binary mask
    _, binary_mask = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)
    
    # Find contours of individual sprites
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create output directory based on input file name
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_dir = base_name
    os.makedirs(output_dir, exist_ok=True)
    
    metadata_path = os.path.join(output_dir, "sprites_metadata.json")
    sprite_metadata = []
    
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        
        # Extract the sprite using the bounding box
        sprite = image[y:y+h, x:x+w]
        
        # Resize the sprite to 64x64
        resized_sprite = cv2.resize(sprite, (64, 64), interpolation=cv2.INTER_AREA)
        
        # Save the sprite image
        sprite_filename = os.path.join(output_dir, f"sprite_{i}.png")
        cv2.imwrite(sprite_filename, resized_sprite)
        
        # Store metadata
        sprite_metadata.append({
            "id": i,
            "x": int(x),
            "y": int(y),
            "width": int(w),
            "height": int(h),
            "file": sprite_filename
        })
    
    # Save metadata to a JSON file
    with open(metadata_path, "w") as json_file:
        json.dump(sprite_metadata, json_file, indent=4)
    
    print(f"Metadata and sprites saved in directory: {output_dir}")
    return sprite_metadata

# Example usage
if __name__ == "__main__":
    sprites_metadata = extract_sprites_from_spritesheet("Soldier.png")