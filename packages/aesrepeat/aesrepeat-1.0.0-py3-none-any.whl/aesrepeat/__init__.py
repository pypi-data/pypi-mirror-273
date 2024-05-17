from aesrepeat.internal import *
import base64
import pickle

__copyright__    = 'Copyright (C) 2024 JavaCommons Technologies'
__version__      = '1.0.0'
__license__      = 'MIT'
__author__       = 'JavaCommons Technologies'
__author_email__ = 'javacommmons@gmail.com'
__url__          = 'https://github.com/lang-library/py-aesrepeat'
__all__ = ['AES128', 'AES256']

class AES128:
    def __init__(self, password_list = []):
        self.password_list = password_list
        self.reverse_password_list = list(reversed(self.password_list))
    def encode_bytes(self, data):
        for p in self.password_list:
            aes = AES128FromString(p)
            data = aes.encode_bytes(data)
        return base64.b64encode(data).decode()
    def decode_bytes(self, base64_text):
        data = base64.b64decode(base64_text.encode())
        for p in self.reverse_password_list:
            aes = AES128FromString(p)
            data = aes.decode_bytes(data)
        return data
    def encode_text(self, plain_text):
        data = plain_text.encode()
        return self.encode_bytes(data)
    def decode_text(self, base64_text):
        data = self.decode_bytes(base64_text)
        return data.decode()
    def encode_pickle(self, x, protocol=3):
        data = pickle.dumps(x, protocol=protocol)
        return self.encode_bytes(data)
    def decode_pickle(self, base64_text):
        data = self.decode_bytes(base64_text)
        return pickle.loads(data)
 
class AES256:
    def __init__(self, password_list = []):
        self.password_list = password_list
        self.reverse_password_list = list(reversed(self.password_list))
    def encode_bytes(self, data):
        for p in self.password_list:
            aes = AES256FromString(p)
            data = aes.encode_bytes(data)
        return base64.b64encode(data).decode()
    def decode_bytes(self, base64_text):
        data = base64.b64decode(base64_text.encode())
        for p in self.reverse_password_list:
            aes = AES256FromString(p)
            data = aes.decode_bytes(data)
        return data
    def encode_text(self, plain_text):
        data = plain_text.encode()
        return self.encode_bytes(data)
    def decode_text(self, base64_text):
        data = self.decode_bytes(base64_text)
        return data.decode()
    def encode_pickle(self, x, protocol=3):
        data = pickle.dumps(x, protocol=protocol)
        return self.encode_bytes(data)
    def decode_pickle(self, base64_text):
        data = self.decode_bytes(base64_text)
        return pickle.loads(data)
 