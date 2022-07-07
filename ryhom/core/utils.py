import random
import string


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
