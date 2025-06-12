import os
from PIL import Image

# Folder with input images
input_folder = "../screenshots"

# Overlay image (must be RGBA)
overlay_path = "data/eye-transp.png"

# Load the overlay RGBA image once
overlay_img = Image.open(overlay_path).convert("RGBA")
overlay_size = overlay_img.size

# Output naming prefix
merged_prefix = "dejavu_"

# Loop through files in the folder
for filename in os.listdir(input_folder):
    # Only process files that are images (optional filter)
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        
        # Skip already merged files
        if filename.startswith(merged_prefix):
            continue

        # Build full input file path
        input_path = os.path.join(input_folder, filename)

        # Open the input image and convert to RGBA to support alpha composition
        with Image.open(input_path).convert("RGBA") as input_img:
            print(f"Processing: {filename} | Original size: {input_img.size}")

            # Resize input image to match the overlay size
            resized_input = input_img.resize(overlay_size, Image.Resampling.LANCZOS)

            # Merge overlay on top of resized input image
            merged_img = resized_input.copy()
            merged_img.paste(overlay_img, (0, 0), overlay_img)

            # Save the merged image back to the same folder with a new name
            merged_filename = merged_prefix + filename
            merged_path = os.path.join(input_folder, merged_filename)

            merged_img.save(merged_path, format="PNG", compress_level=0)
            print(f"Saved merged image: {merged_filename}")
            os.remove(input_path)

print("All images processed!")
