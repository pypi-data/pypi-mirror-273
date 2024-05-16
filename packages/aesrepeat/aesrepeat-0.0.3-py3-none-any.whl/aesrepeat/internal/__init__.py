# pip install PyCryptoDome
from Crypto.Cipher import AES as __AES__
from Crypto.Util.Padding import pad, unpad
import hashlib

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
        self.cipher = __AES__.new(key, __AES__.MODE_CBC, iv)
        self.decipher = __AES__.new(key, __AES__.MODE_CBC, iv)
    def encode_bytes(self, data):
        return self.cipher.encrypt(pad(data, __AES__.block_size))
    def decode_bytes(self, encrypted_data):
        return unpad(self.decipher.decrypt(encrypted_data), __AES__.block_size)
