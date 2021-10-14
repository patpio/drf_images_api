import os

import PIL
from PIL import Image
from django.conf import settings


def create_thumbnail(image, height):
    img = Image.open(image.url)
    h_percent = (height / float(img.size[1]))
    width = int((float(img.size[0]) * float(h_percent)))
    img = img.resize((width, height), PIL.Image.LANCZOS)

    path = settings.MEDIA_ROOT + 'resized_images'
    os.makedirs(path, exist_ok=True)

    filename = image.name.replace(' ', '_')
    new_filename = os.path.splitext(filename)[0] + '_' + str(height) + os.path.splitext(filename)[1]
    file_path = path + os.path.sep + new_filename
    img.save(file_path)
    return new_filename
