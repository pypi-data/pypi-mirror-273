from cogent3 import make_tree
from treetop import get_tree


def test_get_tree():
    assert make_tree("((b,c),a)").same_topology(get_tree())
