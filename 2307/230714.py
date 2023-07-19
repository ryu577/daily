import numpy as np
import pyray.shapes.fourd.tesseract_graph as tg
from itertools import combinations
from collections import defaultdict
import os
import json
import pyray.shapes.twod.square_mesh as sm
from pyray.shapes.twod.tst_sq_mesh import get_msh, rand_msh
from copy import deepcopy
from collections import defaultdict


# Check that an adjacency list is a valid mesh.
def is_valid_mesh(adj):
    tf = tg.TsrctFcGraph(angle=np.pi/2, adj=adj)
    tf.dfs_flatten2('00-+')
    tf.reset_vert_col()
    tf.actually_flatten()
    tf.mk_xy_set()
    if len(tf.xy_set) == 24:
        return True
    return False



def get_faces_at_edge(ed='0++-'):
    i = 0
    fcs = []
    for ch in ed:
        fc1 = list(ed)
        if ch != '0':
            fc1[i] = '0'
            fcs.append(''.join(fc1))
        i = i+1
    return fcs


def get_tsrct_edges():
    edges = []
    for j in ['+','-']:
        for k in ['+','-']:
            for l in ['+','-']:
                signs = [j,k,l]
                for i in range(4):
                    edge = ['0','0','0','0']
                    u = 0
                    for ix in range(len(edge)):
                        if ix != i:
                            edge[ix] = signs[u]
                            u = u+1
                    edges.append(''.join(edge))
    return sorted(edges)


def make_adj_symm(adj):
    adj2 = adj.copy()
    for k in adj.keys():
        for kk in adj[k]:
            if kk not in adj:
                adj2[kk] = [k]
            elif k not in adj[kk]:
                #print("Fixing " + k + "," + kk)
                adj2[kk].append(k)
    return adj2


def edge_lst_to_adj(edge_lst):
    adj = defaultdict(list)
    for ed in edge_lst:
        adj[ed[0]].append(ed[1])
    adj = make_adj_symm(adj)
    for k in adj.keys():
        adj[k] = sorted(adj[k])
    return adj


# Version-1 for generating adj lists.
# superceded by version-2.
ixx = 0
edges = get_tsrct_edges()
for k in combinations(np.arange(3), 2):
    edge_lst = []
    for ed in edges:
        faces = get_faces_at_edge(ed)
        edge_lst.append([faces[k[0]], faces[k[1]]])
    for comb in combinations(np.arange(32),23):
        if ixx > 20000:
            tru_edge_lst = [edge_lst[i] for i in comb]
            adj = edge_lst_to_adj(tru_edge_lst)
            if is_valid_mesh(adj):
                print(ixx)
        ixx += 1
        if ixx > 40000:
            break


# Version-2
ixx = 0
edges = get_tsrct_edges()
for comb in combinations(np.arange(32),23):
    scpd_edges = [edges[i] for i in comb]
    face_lst = [get_faces_at_edge[ed] for ed in scpd_edges]
    # Note that this is wrong because each physical edge can have
    # different combinations of faces.
    for k in range(3):
        kk = [i for i in range(3) if i!=k]
        edge_lst = []
        for ll in range(23):
            edge_lst.append([face_lst[ll][kk[0]], face_lst[ll][kk[1]]])
        adj = edge_lst_to_adj(edge_lst)

#Looks like this was a false lead.
#3^23 term is 9 billion.
# Back to just making the video, I guess. 
# At least I managed to tighten the upper bound
# to 10^16.

## Adding more scenes to 230709 for continuity.