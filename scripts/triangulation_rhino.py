import os
import json
import compas_rhino
from compas_rhino.geometry import RhinoCurve

HERE = os.path.dirname(__file__)
DATA = os.path.join(HERE, '../data')
FILE = os.path.join(DATA, 'rhino1.json')

# boundary
guids = compas_rhino.select_curves()
curve = RhinoCurve.from_guid(guids[0])
points = [list(point) for point in curve.points]
boundary = points

# segments
guids = compas_rhino.select_curves()
curve = RhinoCurve.from_guid(guids[0])
points = curve.divide(10, over_space=True)
segments = points

# hole
guids = compas_rhino.select_curves()
curve = RhinoCurve.from_guid(guids[0])
points = curve.divide(10, over_space=True)
hole = points

data = {
    "boundary": boundary,
    "segments": segments,
    "hole": hole
}

with open(FILE, 'w') as f:
    json.dump(data, f)
