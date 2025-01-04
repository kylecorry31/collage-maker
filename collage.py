from PIL import Image
import math
import uuid

output_size = (300, 300)
quality = 95
files = []

if len(files) == 0:
    print('No images to create a collage.')
    exit()

images = [Image.open(file) for file in files]
rows = math.ceil(math.sqrt(len(images)))
cols = math.ceil(len(images) / rows)
image_size = output_size[0] // cols, output_size[1] // rows
print(f'Rows: {rows}, Columns: {cols}')

collage = Image.new('RGBA', (output_size[0], output_size[1]), (0, 0, 0, 0))

for i, image in enumerate(images):
    x = (i % cols) * output_size[0] // cols
    y = (i // cols) * output_size[1] // rows
    scale = max(image.size[0] / image_size[0], image.size[1] / image_size[1])
    thumbnail = image.resize((int(image.size[0] / scale), int(image.size[1] / scale)))
    x += (image_size[0] - thumbnail.size[0]) // 2
    y += (image_size[1] - thumbnail.size[1]) // 2
    collage.paste(thumbnail, (x, y))

filename = f'collage_{uuid.uuid4()}.webp'
collage.save(filename, 'WEBP', quality=quality)
print(f'Collage saved as {filename}')

