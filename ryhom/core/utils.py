import random
import string
import uuid
from io import BytesIO

from django.core.files import File
from PIL import Image


def random_string_generator(size=10, chars=True, ints=True):
    """
    A random string generator. This generator will contain letters
    and numbers, or only letters or only numbers depending on the
    condition of the parameters. This random string will be
    added at the end of some URL slugs.

    For example, when "chars & ints == True"...

    'ryhom.com/post/53nhzw3bcm'
    """

    lowercase_letters = string.ascii_lowercase
    integers = string.digits

    if chars and ints:
        random_includes = lowercase_letters + integers
    elif chars and not ints:
        random_includes = lowercase_letters
    else:
        random_includes = integers

    return ''.join(random.choice(random_includes) for _ in range(size))


def resize_optimize_image(uploaded_image, desired_width, desired_height):
    img = Image.open(uploaded_image)
    (current_w, current_h) = img.size # current size (width, height)

    if not img.mode == 'RGB':
        img = img.convert('RGB')

    if current_w or current_h > desired_width or desired_height:
        new_size = (desired_width, desired_height) # new size
        img.thumbnail(new_size, Image.ANTIALIAS)

    random_name = f'{uuid.uuid4()}.jpeg'

    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=98, optimize=True)

    new_image = File(img_io, name=random_name)

    return new_image
