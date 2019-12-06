from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

if not compas.IPY:
    from .planarize import planarize_quads


def planarize_quads_proxy(vertices, faces, kmax, maxdev):
    import numpy as np
    V1 = np.array(vertices, dtype=np.float64)
    F1 = np.array(faces, dtype=np.int32)
    V2 = planarize_quads(V1, F1, 500, 0.005)
    return V2.tolist()


__all__ = [_ for _ in dir() if not _.startswith('_')]
