import hashlib
import base64


def encode_password(password):
    encode_pass = base64.b64encode(password)
    return encode_pass


def create_hash_password(password):
    h = hashlib.md5(password.encode())
    return h.hexdigest()