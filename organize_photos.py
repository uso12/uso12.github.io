import os
import shutil
import json
from PIL import Image, ImageOps  # Added ImageOps

# --- CONFIGURATION ---
TARGET_DIRECTORIES = ['photos-reduce', 'photos-1_5_resolution']
IMAGE_DATA_FILE = "images.json"

# New Configuration for Imports
IMPORT_SOURCE_DIR = 'new-full-added'
IMPORT_ARCHIVE_DIR = os.path.join(IMPORT_SOURCE_DIR, 'old')
THUMB_DEST_DIR = 'photos-reduce'
FULL_DEST_DIR = 'photos-1_5_resolution'
MAX_THUMB_SIZE_MB = 2

def load_file_mappings(json_file):
    """Loads JSON and flattens base/additional into one list per category"""
    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found.")
        return {}
        
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    mapping = {}
    for category, content in data.items():
        combined_files = content.get('base', []) + content.get('additional', [])
        mapping[category] = combined_files
        
    return mapping

def process_new_imports():
    """
    1. Reads images from 'new-full-added'
    2. Fixes rotation (EXIF)
    3. Resizes to 20% resolution (and ensures < 2MB) -> saves to 'photos-reduce'
    4. Copies full res -> 'photos-1_5_resolution'
    5. Moves source -> 'new-full-added/old'
    """
    if not os.path.exists(IMPORT_SOURCE_DIR):
        print(f"Directory '{IMPORT_SOURCE_DIR}' does not exist. Skipping import.")
        return

    # Create destination folders if they don't exist
    for d in [IMPORT_ARCHIVE_DIR, THUMB_DEST_DIR, FULL_DEST_DIR]:
        if not os.path.exists(d):
            os.makedirs(d)

    valid_exts = ('.jpg', '.jpeg', '.png', '.webp')
    files = [f for f in os.listdir(IMPORT_SOURCE_DIR) if f.lower().endswith(valid_exts)]

    if not files:
        print("No new images found in 'new-full-added'.")
        return

    print(f"Processing {len(files)} new images...")

    for filename in files:
        src_path = os.path.join(IMPORT_SOURCE_DIR, filename)
        thumb_path = os.path.join(THUMB_DEST_DIR, filename)
        full_dest_path = os.path.join(FULL_DEST_DIR, filename)
        archive_path = os.path.join(IMPORT_ARCHIVE_DIR, filename)

        try:
            # 1. PROCESS THUMBNAIL
            with Image.open(src_path) as img:
                # --- FIX: Apply EXIF rotation before resizing ---
                img = ImageOps.exif_transpose(img)
                
                # Calculate 20% dimensions
                new_width = int(img.width * 0.20)
                new_height = int(img.height * 0.20)
                
                # Resize using high-quality resampling
                img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Save and check file size constraint (< 2MB)
                quality = 85
                while True:
                    # Strip metadata (exif) on save to prevent double-rotation issues later
                    # and to save space.
                    img_resized.save(thumb_path, optimize=True, quality=quality)
                    
                    file_size_mb = os.path.getsize(thumb_path) / (1024 * 1024)
                    
                    if file_size_mb < MAX_THUMB_SIZE_MB or quality <= 10:
                        break
                    
                    # If still too big, reduce quality
                    quality -= 5
            
            # 2. COPY FULL RES
            shutil.copy2(src_path, full_dest_path)

            # 3. ARCHIVE SOURCE
            shutil.move(src_path, archive_path)
            
            print(f"  [Processed] {filename}")

        except Exception as e:
            print(f"  [Error] Failed to process {filename}: {e}")

    print("Import processing complete.\n")

def move_files():
    """Organizes files into subfolders based on images.json"""
    print("Starting organization based on JSON...")
    
    file_mappings = load_file_mappings(IMAGE_DATA_FILE)
    if not file_mappings:
        print("No mappings found. Exiting.")
        return

    for base_folder in TARGET_DIRECTORIES:
        if not os.path.exists(base_folder):
            print(f"Skipping {base_folder} (Not found)")
            continue
            
        print(f"Sorting folder: {base_folder}")
        
        for category, files in file_mappings.items():
            dest_dir = os.path.join(base_folder, category)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            for filename in files:
                src_path = os.path.join(base_folder, filename)
                dest_path = os.path.join(dest_dir, filename)

                # Move from root of folder to category subfolder
                if os.path.exists(src_path):
                    shutil.move(src_path, dest_path)
                elif os.path.exists(dest_path):
                    pass # Already moved
                else:
                    pass 

    print("Done! Files organized.")

if __name__ == "__main__":
    # 1. First, process any new raw images
    process_new_imports()
    
    # 2. Then, organize everything based on the JSON file
    move_files()