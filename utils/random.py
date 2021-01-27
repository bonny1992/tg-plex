import random
import string

def get_random_string(length):
    letters = string.ascii_lowercase + string.digits + string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str