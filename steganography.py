from stegano import lsb
import os


def encode_message(image_path, message):
    secret = lsb.hide(image_path, message)
    encoded_image_path = os.path.join(
        os.path.dirname(image_path), f"encoded_{os.path.basename(image_path)}"
    )
    secret.save(encoded_image_path)
    return encoded_image_path


def decode_message(image_path):
    secret = lsb.reveal(image_path)
    return secret
