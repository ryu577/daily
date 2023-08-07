import numpy as np
from scipy.stats import binom


def est_n(sla=.99, n=40, p=0.17):
    n1 = n
    sf = binom.sf(n-1, n1, p)
    while sf < sla:
        n1 += 1
        sf = binom.sf(n-1, n1, p)
    return n1


n = 40
n1 = est_n(n=n)
n2 = est_n(n=n, sla=.99, p=.8)
discnt_fctr = 1-(n1+(n2-n1)*.1)/n1
print(discnt_fctr)


##########################################
## Now some pyray stuff.

from pyray.rotation import rotation, axis_rotation
from pyray.shapes.solid.open_cube_tst import tst_perspective
from PIL import Image, ImageDraw
from copy import deepcopy
from itertools import combinations
from pyray.shapes.solid.open_cube import Face
from pyray.shapes.fourd.tsrct_cube_graph import primitive_tsrct_open,\
    TsrctCubeTree
from pyray.rotation2.rotn_4d import rotn_1
from pyray.rotation import rotate_matrix_to_another
from pyray.shapes.fourd.tsrct_cube_graph import MshObj


class MshObj():
    def __init__(self, tt, r, scale, shift, persp):
        self.tt = tt
        self.r = r
        self.scale = scale
        self.shift = shift
        self.persp = persp
    
    def plot(self, draw, rgba=(100,100,100,40)):
        self.tt.plot(draw, self.r, rgba=rgba,
            shift=self.shift,
            scale=self.scale,
            persp=self.persp)


r1 = rotation(4, np.pi*17/60.0*14/10.0)
r2_3d = axis_rotation(np.array([0,0,0]), 
                      np.array([1,1,1]),
                      2*np.pi/6)[:3,:3]
r2 = np.eye(4)
r2[:3,:3] = r2_3d
rr1 = rotate_matrix_to_another(r1, r2)
##### incomplete..
adjs = [{
        '000-':['-000','+000','00-0','00+0'],
        '00-0':['0+00','000+'],
        '00+0':['0-00']
        },
        {
            '000-': ['00-0','+000','0-00','-000','0+00','00+0'],
            '00-0': ['000+']
        }]
mos = []
for adj in adjs:
    for i in range(25):
        tt = TsrctCubeTree()
        tt.adj = adj
        tt.bfs('000-')
        tt.reset_vert_col()
        tt.theta = np.pi/48.0*i
        tt.dfs_flatten('000-')
        im = Image.new("RGB", (1024, 1024), (256, 256, 256))
        draw = ImageDraw.Draw(im, 'RGBA')
        r=rotation(4, np.pi*17/60.0*14/10.0)
        tt.plot(draw, r, rgba=(100,100,100,40),
                shift=np.array([514, 595, 0, 0]),
                scale=105)
        im.save("Images//RotatingCube//im" +
                            str(i).rjust(4, '0') +
                            ".png")
for i in range(25):
    tt = TsrctCubeTree()
    tt.adj = adj
    tt.bfs('000-')
    tt.reset_vert_col()
    tt.theta = np.pi/48.0*(24-i)
    r=rotation(4, np.pi*17/60.0*14/10.0)
    tt.plot(draw, r, rgba=(100,100,100,40),
            shift=np.array([514, 595, 0, 0]),
            scale=105)
    tt1 = TsrctCubeTree()
    tt1.adj = adj
    tt1.bfs('000-')
    tt1.reset_vert_col()
    tt1.theta = np.pi/2
    tt1.dfs_flatten('000-')
    tt1.plot(draw, r1, rgba=(100,100,100,40),
            shift=np.array([514-i*18, 595+i*18, 0, 0]),
            scale=105*(15-i/1.2)/15, persp=(5+i*10))
    r1 = np.dot(rr1, r1)
    for mo in mos:
        mo.plot(draw)
    im.save("Images//RotatingCube//im" +
                            str(i).rjust(4, '0') +
                            ".png")
mo1 = MshObj(tt1, r1, 105*(15-i/1.2)/15, np.array([514-i*18, 595+i*18, 0, 0]), 5+10*i)
mos.append(mo1)

