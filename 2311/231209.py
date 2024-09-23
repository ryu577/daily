import numpy as np
from collections import defaultdict


class Node():
    def __init__(self, key=0, color="white"):
        self.key = key
        self.color = color
        self.d = 0
        self.pi = Node(0)
        self.f = 0
    #def __hash__(self):
    #    return self.key


nodes = [Node(0), Node(1), Node(2)]

graph = {nodes[0]: [nodes[1], nodes[2]], nodes[1]: [], nodes[2]: []}


def dfs(graph, u):
    u.color = "grey"
    for v in graph[u]:
        if v.color == "white":
            dfs(graph, v)
    u.color = "black"
    print(u.key)


dfs(graph, nodes[0])
