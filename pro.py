import os

def rename_archer_files(directory):
    """ Renames all PNG files starting with 'Archer' to lowercase in the given directory. """
    
    # Ensure the directory exists
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return
    
    # Loop through files in the directory
    for filename in os.listdir(directory):
        if filename.lower().endswith(".png") and filename.startswith("Knight"):
            old_path = os.path.join(directory, filename)
            new_filename = filename.lower()  # Convert to lowercase
            new_path = os.path.join(directory, new_filename)
            
            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} → {new_filename}")

# Example usage
directory = r"C:\Users\praty\Desktop\COdeWars V5\coderoyale\data\images\troops\Red"  # Change this to your actual folder path
rename_archer_files(directory)
