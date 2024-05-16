# pip install PyCryptoDome
from Crypto.Cipher import AES as ___AES__
import base64
import hashlib
import pickle

__copyright__    = 'Copyright (C) 2024 JavaCommons Technologies'
__version__      = '0.0.0'
__license__      = 'MIT'
__author__       = 'JavaCommons Technologies'
__author_email__ = 'javacommmons@gmail.com'
__url__          = 'https://github.com/lang-library/py-aesrepeat'
__all__ = ['AES', 'AES128FromString', 'AES256FromString']

def AES128FromString(str):
    sha256 = hashlib.sha256(str.encode())
    digets = sha256.digest()
    upper16 = digets[0:16]
    lower16 = digets[16:]
    return AES(upper16, lower16)

def AES256FromString(str):
    sha384 = hashlib.sha384(str.encode())
    digets = sha384.digest()
    upper32 = digets[0:32]
    lower16 = digets[32:]
    return AES(upper32, lower16)

class AES:
    def __init__(self, key, iv):
        self.cipher = ___AES__.new(key, ___AES__.MODE_CBC, iv)
        self.decipher = ___AES__.new(key, ___AES__.MODE_CBC, iv)
    def encode_text(self, plain_text):
        data = plain_text.encode()
        block_size = ___AES__.block_size
        padding_size = block_size - (len(data) % block_size)
        padded_data = data + bytes([padding_size]) * padding_size
        encrypted_data = self.cipher.encrypt(padded_data)
        return base64.b64encode(encrypted_data).decode()
    def decode_text(self, base64_text):
        encrypted_data = base64.b64decode(base64_text.encode())
        decrypted_data = self.decipher.decrypt(encrypted_data)
        padding_size = decrypted_data[-1]
        unpadded_data = decrypted_data[:-padding_size]
        return unpadded_data.decode()
    def encode_bytes(self, data):
        block_size = ___AES__.block_size
        padding_size = block_size - (len(data) % block_size)
        padded_data = data + bytes([padding_size]) * padding_size
        encrypted_data = self.cipher.encrypt(padded_data)
        return base64.b64encode(encrypted_data).decode()
    def decode_bytes(self, base64_text):
        encrypted_data = base64.b64decode(base64_text.encode())
        decrypted_data = self.decipher.decrypt(encrypted_data)
        padding_size = decrypted_data[-1]
        unpadded_data = decrypted_data[:-padding_size]
        return unpadded_data
    def encode_pickle(self, x, protocol=3):
        data = pickle.dumps(x, protocol=protocol)
        block_size = ___AES__.block_size
        padding_size = block_size - (len(data) % block_size)
        padded_data = data + bytes([padding_size]) * padding_size
        encrypted_data = self.cipher.encrypt(padded_data)
        return base64.b64encode(encrypted_data).decode()
    def decode_pickle(self, base64_text):
        encrypted_data = base64.b64decode(base64_text.encode())
        decrypted_data = self.decipher.decrypt(encrypted_data)
        padding_size = decrypted_data[-1]
        unpadded_data = decrypted_data[:-padding_size]
        return pickle.loads(unpadded_data)
