"""
TreeTOP

Rapid and statistically robust reconstruction of maximum-likelihood phylogenetic trees.
"""

from cogent3 import make_tree

__version__ = "2024.5.13.dev1"


def get_tree():
    return make_tree("(a,(b,c))")
