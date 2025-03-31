"""COMPAS libigl integration package"""

try:
    from ._libigl import add, __doc__
except ImportError as e:
    raise ImportError("Could not import the required dependencies to run compas_libigl: {}".format(e))

__all__ = ['add']
