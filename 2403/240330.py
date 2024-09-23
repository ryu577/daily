import numpy as np
from ppbtree import Node, add, print_tree
from copy import deepcopy


class Node1():
    def __init__(self, key):
        self.key = key
        self.val = key
        self.left = None
        self.right = None


def find_1path(node, depth=0, max_dpth=5, path=[]):
    if depth > max_dpth:
        node.path = deepcopy(path)
        return
    if node is None:
        return
    path.append(depth)
    find_1path(node.left, depth+1, max_dpth, path)
    path.pop()
    find_1path(node.right, depth+1, max_dpth, path)


class Tree():
    def __init__(self, arr, mat):
        """
        The mat is a dynamic programming matrix.
        Comes from 240329.py isSubsetSum.
        """
        self.arr = arr
        self.mat = mat
        self.root = self.mk_tree(len(arr)-1, len(mat[0])-1)

    def mk_tree(self, ro, col):
        if col < 0 or ro < -1 or not self.mat[ro+1][col]:
            return
        node1 = Node1(1)
        node1.right = self.mk_tree(ro-1, col)
        node1.left = self.mk_tree(ro-1, col - self.arr[ro])
        return node1

## Continued in optimizn/ab_split.