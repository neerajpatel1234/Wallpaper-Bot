import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def select_image(title="Select an Image"):
    file_path = filedialog.askopenfilename(title=title, filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    return file_path if file_path else None

def crop_to_square(image_path):
    image = Image.open(image_path)
    width, height = image.size
    if width == height:
        return image
    
    crop_size = min(width, height)
    left = (width - crop_size) / 2
    top = (height - crop_size) / 2
    right = (width + crop_size) / 2
    bottom = (height + crop_size) / 2
    
    return image.crop((left, top, right, bottom))

def create_wallpaper_grid():
    root = tk.Tk()
    root.withdraw()
    
    # Select grid size (rows & cols)
    rows = 5  # Change as needed
    cols = 3  # Change as needed
    
    # Select featured image
    featured_image_path = select_image("Select Featured Image")
    if not featured_image_path:
        print("No featured image selected.")
        return
    
    # Select remaining images
    remaining_images_paths = filedialog.askopenfilenames(title="Select Remaining Images", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    
    if not remaining_images_paths:
        print("No remaining images selected.")
        return
    
    # Ensure featured image is not in remaining images
    remaining_images_paths = [img for img in remaining_images_paths if img != featured_image_path]
    
    # Resize and crop images to square
    images = [crop_to_square(featured_image_path)]
    for img_path in remaining_images_paths:
        images.append(crop_to_square(img_path))
    
    # Ensure enough images to fill the grid
    while len(images) < rows * cols:
        images.append(images[len(images) % len(images)])
    
    images = images[:rows * cols]  # Trim extra images
    
    # Select gap size
    gap_size = 10  # Change as needed
    
    # Create final grid canvas
    grid_size = 1080 // cols
    final_image = Image.new("RGB", (1080, 1920), "white")
    
    # Arrange images in grid
    index = 0
    for r in range(rows):
        for c in range(cols):
            img = images[index].resize((grid_size - gap_size, grid_size - gap_size))
            final_image.paste(img, (c * grid_size + gap_size // 2, r * grid_size + gap_size // 2))
            index += 1
    
    # Export final image
    export_path = os.path.join(os.getcwd(), "wallpaper_grid.jpg")
    final_image.save(export_path, "JPEG")
    print(f"Wallpaper grid saved at {export_path}")

if __name__ == "__main__":
    create_wallpaper_grid()
