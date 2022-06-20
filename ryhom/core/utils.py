import random
import string


def random_string_generator(size=10, chars=True, ints=True):
    """
    A random string generator. This generator will contain letters
    and numbers, or only letters or only numbers depending on the
    condition of the parameters. This random string will be
    added at the end of some URL slugs.

    For example, when "chars & ints == True"...

    'ryhom.com/indoor-gardening-beginner-guide-53nhzw3bcm'
    """

    characters = string.ascii_lowercase
    integers = string.digits

    if chars and ints:
        random_includes = characters + integers
    elif chars:
        random_includes = characters
    else:
        random_includes = integers

    return ''.join(random.choice(random_includes) for _ in range(size))
