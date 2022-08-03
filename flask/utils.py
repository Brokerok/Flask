import random

from flask import make_response


def generate_password(chars, length):
    result = []
    for j in range(length):
        result.append(random.choice(chars))
    return "".join(result)


def render_list(list_of_objects):
    result = []
    for obj in list_of_objects:
        result.append(str(obj))

    response = make_response("\n".join(result))
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response
