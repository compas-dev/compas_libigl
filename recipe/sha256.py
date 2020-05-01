import os
import hashlib

# HERE = os.path.dirname(__file__)
# FILE = os.path.join(HERE, '/Users/vanmelet/Downloads/pybind11-2.5.0.tar.gz')
# FILE = '/Users/vanmelet/Downloads/pybind11-2.5.0.tar.gz'
# FILE = '/Users/vanmelet/Downloads/libigl-2.2.0.tar.gz'
FILE = '/Users/vanmelet/Downloads/compas_libigl-0.1.2.tar.gz'

with open(FILE, 'rb') as f:
    data = f.read()
    h = hashlib.sha256(data).hexdigest()

print(h)
