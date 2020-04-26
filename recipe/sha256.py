import os
import hashlib

HERE = os.path.dirname(__file__)
FILE = os.path.join(HERE, '../temp/compas_libigl-alpha-0.1.0.tar.gz')

with open(FILE, 'rb') as f:
    data = f.read()
    h = hashlib.sha256(data).hexdigest()

print(h)
