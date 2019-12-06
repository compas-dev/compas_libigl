from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

if not compas.IPY:
    from .planarize import planarize_quads


def planarize_quads_proxy(vertices, faces, kmax=500, maxdev=0.005):
    import numpy as np
    V1 = np.array(vertices, dtype=np.float64)
    F = np.array(faces, dtype=np.int32)
    V2 = planarize_quads(V1, F, kmax, maxdev)
    return V2.tolist()


__all__ = [_ for _ in dir() if not _.startswith('_')]
