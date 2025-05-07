from PIL import Image, ImageDraw, ImageFont
import math
import uuid

output_size = (1000, 1000)
quality = 100
label_size = 0.03  # % of the output size
label_color = "black"
base_path = (
    "/var/home/kyle/Documents/development/Trail-Sense-Artwork/survival_guide/processed/"
)
draw_labels = True
use_numeric_labels = True
trim_space = True
background_color = (255, 255, 255, 255)
files = [
    f"{base_path}/poison_ivy.webp",
    f"{base_path}/stinging_nettle.webp"
]
labels = []

if len(files) == 0:
    print("No images to create a collage.")
    exit()

images = [Image.open(file) for file in files]
cols = math.ceil(math.sqrt(len(images)))
rows = math.ceil(len(images) / cols)
image_size = output_size[0] // cols, output_size[1] // rows
print(f"Rows: {rows}, Columns: {cols}")

collage = Image.new("RGBA", (output_size[0], output_size[1]), (0, 0, 0, 0))
draw = ImageDraw.Draw(collage)

# Optional: Set a font for the numbers
font_size = int(output_size[0] * label_size)  # Font size is 5% of the output width
try:
    font = ImageFont.truetype("OpenSans-Regular.ttf", font_size)
except IOError:
    font = ImageFont.load_default()

current_y = 0  # Track the current y-coordinate for placing rows
for row in range(rows):
    max_row_height = 0  # Track the maximum height of images in the current row
    for col in range(cols):
        i = row * cols + col
        if i >= len(images):
            break

        image = images[i]
        scale = max(image.size[0] / image_size[0], image.size[1] / image_size[1])

        new_size = (
            int(image.size[0] / scale),
            int(image.size[1] / scale),
        )

        if image.size[0] == image.size[1] and image_size[0] == image_size[1]:
            new_size = image_size

        thumbnail = image.resize(new_size)
        x = col * output_size[0] // cols + (image_size[0] - thumbnail.size[0]) // 2
        y = current_y + (image_size[1] - thumbnail.size[1]) // 2
        collage.paste(thumbnail, (x, y))

        # Add the label in the top-left corner of the image
        if draw_labels:
            label_position = (x + font_size / 2, y + font_size / 2)
            label = str(i + 1) if use_numeric_labels else labels[i]
            draw.text(label_position, label, fill=label_color, font=font)

        max_row_height = max(max_row_height, thumbnail.size[1])

    current_y += max_row_height  # Move to the next row based on the tallest image

# Trim surrounding space if the option is enabled
if trim_space:
    bbox = collage.getbbox()
    if bbox:
        collage = collage.crop(bbox)

# Replace transparent pixels with the background color
if background_color:
    background = Image.new("RGBA", collage.size, background_color)
    collage = Image.alpha_composite(background, collage)

filename = f"collage_{uuid.uuid4()}.webp"
collage.save(filename, "WEBP", quality=quality)
print(f"Collage saved as {filename}")
