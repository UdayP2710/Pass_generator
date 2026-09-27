import string
import secrets


def generate_password(length):
    characters = string.ascii_letters + string.digits

    password = ""

    for i in range(length):
        character = secrets.choice(characters)
        password = password + character
    return password