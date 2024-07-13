from stegano import lsb
import os


def xor_encrypt_decrypt(data, key):
    return "".join(
        chr(ord(char) ^ ord(key[i % len(key)])) for i, char in enumerate(data)
    )


def encode_message(image_path, message, key):
    encrypted_message = xor_encrypt_decrypt(message, key)
    secret = lsb.hide(image_path, encrypted_message)
    encoded_image_path = os.path.join(
        os.path.dirname(image_path), f"encoded_{os.path.basename(image_path)}"
    )
    secret.save(encoded_image_path)
    return encoded_image_path


def decode_message(image_path, key):
    encrypted_message = lsb.reveal(image_path)
    if encrypted_message:
        decrypted_message = xor_encrypt_decrypt(encrypted_message, key)
        return decrypted_message
    return None
