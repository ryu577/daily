import numpy as np
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
from pyray.shapes.fourd.open_tsrct import TsrctFcGraph2, TsrctFcGraph3


def plot_all_faces(tf, draw, r, persp=0, rgba=(10,31,190,80),
                    shift=np.array([514, 595, 0, 0]),scale=105):
    """
    The face colors here are consistent with
    230703 plot_colors method.
    """
    self = tf
    for kk in self.face_map.keys():
        if kk[0] == '+':
            col = (255,255,0,10)
        elif kk[3] == '-':
            col = (255,0,0,10)
        elif kk[1] == '+':
            col = (255,0,255,10)
        else:
            col = rgba
        ff = self.vert_props[kk]
        ff.plot_perspective(draw, r,
                                rgba=col,
                                e=persp,
                                c=-persp,
                                shift=shift,
                                scale=scale)


###############
## Failed experiment, rendered unnecessary by next section.
tf = TsrctFcGraph2(angle=0.0)
#tf.adj, tf.face_map = scope_graph(tf.adj, tf.face_map)
tf.bfs('+00+')
tf.reset_vert_col()
r=rotation(4, np.pi*17/60.0*14/10.0)
im = Image.new("RGB", (1024, 1024), (0, 0, 0))
draw = ImageDraw.Draw(im, 'RGBA')
tf.plot_all_faces(draw, r, persp=5,shift=np.array([514, 595, 0, 0]),
                                         scale=105, rgba=(100,100,100,40))
im.save("Images//RotatingCube//im" +
                    str(0).rjust(4, '0') +
                    ".png")
for i in range(22):
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tf.theta = np.pi/42.0*(i+1)
    for j in range(tf.max_depth):
        tf.reset_vert_col()
        tf.curr_d = j+1
        tf.dfs('+00+')
    if i < 63:
        tf.plot_all_faces(draw, r, persp=5,shift=np.array([514, 595, 0, 0]),
            scale=105-min(i,21)*2.7, rgba=(100,100,100,40))
        print(105-min(i,21)*2.7)
    else:
        tf.plot_all_faces(draw, r, persp=5,shift=np.array([514, 595, 0, 0]),
            scale=105-(21-min((i-64),21) )*2.7, rgba=(100,100,100,40))
        print(105-(21-min((i-64),21) )*2.7)
    tf.reset()
    im.save("Images//RotatingCube//im" +
                    str(i+1).rjust(4, '0') +
                    ".png")


import pyray.shapes.fourd.tesseract_graph as tg
from pyray.rotation import rotation

def open_given_cube(tf, base_fc='+00+', i=0):
    tf.reset_vert_col()
    tf.dfs_flatten2(base_fc)
    tf.reset_vert_col()
    while tf.rot_st:
        tf.reset_vert_col()
        (u, rot) = tf.rot_st.pop()
        tf.vert_props[u].shift_and_simpl_rotate(tf.angle, *rot)
        print("Rotated face: " + str(i))
    tf.mk_xy_set()
    print(len(tf.xy_set))


#scene-14
for i in range(13):
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tf = tg.TsrctFcGraph(angle=np.pi/24*i, adj=None)
    tf.draw = draw
    tf.r = rotation(4, np.pi*17/60.0*14/10.0)
    #tf.r = np.eye(4)
    open_given_cube(tf, w_persp=5, i=i, base_fc='+00+')
    plot_all_faces(tf, tf.draw, tf.r, persp=5,shift=np.array([514, 595, 0, 0]),
            scale=105-i*2.7, rgba=(100,100,100,40))
    #print(105-min(i,21)*2.7)
    im.save("Images//RotatingCube//im" +
                str(i).rjust(4, '0') + ".png")


#scene-15
for i in range(13):
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tf = tg.TsrctFcGraph(angle=np.pi/24*(i+12), adj=None)
    tf.draw = draw
    tf.r = rotation(4, np.pi*17/60.0*14/10.0)
    open_given_cube(tf, w_persp=5, i=i)
    plot_all_faces(tf, tf.draw, tf.r, persp=5,shift=np.array([514, 595, 0, 0]),
            scale=105-(12-i)*2.7, rgba=(100,100,100,40))
    print(105-min(i,21)*2.7)
    im.save("Images//RotatingCube//im" +
                str(i).rjust(4, '0') + ".png")


## Some scenes being added on 230715
#scene-16
for i in range(13):
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tf = tg.TsrctFcGraph(angle=np.pi/24*(i+24), adj=None)
    tf.draw = draw
    tf.r = rotation(4, np.pi*17/60.0*14/10.0)
    open_given_cube(tf, w_persp=5, i=i)
    plot_all_faces(tf, tf.draw, tf.r, persp=5,shift=np.array([514, 595, 0, 0]),
            scale=105, rgba=(100,100,100,40))
    print(105-min(i,21)*2.7)
    im.save("Images//RotatingCube//im" +
                str(i).rjust(4, '0') + ".png")


#scene-17
for i in range(13):
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tf = tg.TsrctFcGraph(angle=np.pi/24*(i+36), adj=None)
    tf.draw = draw
    tf.r = rotation(4, np.pi*17/60.0*14/10.0)
    open_given_cube(tf, w_persp=5, i=i)
    plot_all_faces(tf, tf.draw, tf.r, persp=5,shift=np.array([514, 595, 0, 0]),
            scale=105, rgba=(100,100,100,40))
    print(105-min(i,21)*2.7)
    im.save("Images//RotatingCube//im" +
                str(i).rjust(4, '0') + ".png")
