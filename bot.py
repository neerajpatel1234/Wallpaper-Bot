import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import random

def select_single_image(prompt="Select the special image"):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title=prompt, filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
    if not file_path:
        messagebox.showerror("Error", "No image selected.")
        return None
    return Image.open(file_path)

def select_multiple_images(prompt="Select 14 other images"):
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title=prompt, filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
    if len(file_paths) != 14:
        messagebox.showerror("Error", "Please select exactly 14 images.")
        return None
    return [Image.open(path) for path in file_paths]

def crop_to_square(img):
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    return img.crop((left, top, left + min_dim, top + min_dim))

def create_image_grid(images, rows=5, cols=3, gap=10):
    img_size = 300
    processed_images = [
        crop_to_square(img).resize((img_size, img_size))
        for img in images
    ]

    total_width = cols * img_size + (cols - 1) * gap
    total_height = rows * img_size + (rows - 1) * gap
    canvas = Image.new('RGB', (total_width, total_height), color='black')

    for idx, img in enumerate(processed_images):
        row, col = divmod(idx, cols)
        x = col * (img_size + gap)
        y = row * (img_size + gap)
        canvas.paste(img, (x, y))

    return canvas

def main():
    # Step 1: Get the special image
    special_img = select_single_image("Select the image for the center of the second-to-last row")
    if special_img is None:
        return

    # Step 2: Get the remaining 14 images
    all_imgs = select_multiple_images("Select 14 other images")
    if all_imgs is None:
        return

    # Step 3: Prepare final image list
    insert_index = 10  # row 4, col 2 in 0-based indexing (3*3 + 1)

    # Separate the spot for special image
    imgs_before = all_imgs[:insert_index]
    imgs_after = all_imgs[insert_index:]
    shuffled_imgs = imgs_before + imgs_after
    random.shuffle(shuffled_imgs)

    # Insert special image into the correct spot
    final_imgs = shuffled_imgs[:insert_index] + [special_img] + shuffled_imgs[insert_index:]

    # Step 4: Build and display grid
    output = create_image_grid(final_imgs)
    output.show()
    output.save("image_grid_special_shuffled.jpg")

if __name__ == "__main__":
    main()
