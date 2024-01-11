import string
import random
import datetime


def generate_random_id(length):
    letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return "".join(random.choice(letters) for _ in range(length))


def current_timestamp_int_milliseconds():
    return int(datetime.datetime.now().timestamp() * 1000)
