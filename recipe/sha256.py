import hashlib
from pathlib import Path

FILE = Path(__file__).parent / "pybind11-2.10.4.tar.gz"

with open(FILE, "rb") as f:
    data = f.read()
    h = hashlib.sha256(data).hexdigest()

print(h)
