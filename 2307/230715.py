import numpy as np
from PIL import Image, ImageDraw
import pyray.shapes.fourd.tesseract_graph as tg
from pyray.rotation import rotation
from pyray.rotation import rotate_matrix_to_another
from pyray.shapes.twod.tst_sq_mesh import get_msh, rand_msh
from copy import deepcopy

# Dedicated to scene18 which is 4d->2d meshes.

def open_given_cube(tf, base_fc='+00+', i=0):
    tf.reset_vert_col()
    tf.dfs_flatten2(base_fc)
    tf.reset_vert_col()
    while tf.rot_st:
        tf.reset_vert_col()
        (u, rot) = tf.rot_st.pop()
        tf.vert_props[u].shift_and_simpl_rotate(tf.angle, *rot)
        #print("Rotated face: " + str(i))
    tf.mk_xy_set()
    print(len(tf.xy_set))


def plot_all_faces(tf, draw, r, persp=0, rgba=(10,31,190,80),
                    shift=np.array([514, 595, 0, 0]),scale=105):
    """
    The face colors here are consistent with
    230703 plot_colors method.
    """
    for kk in tf.face_map.keys():
        if kk[0] == '+':
            col = (255,255,0,10)
        elif kk[3] == '-':
            col = (255,0,0,10)
        elif kk[1] == '+':
            col = (255,0,255,10)
        else:
            col = rgba
        ff = tf.vert_props[kk]
        ff.plot_perspective(draw, r,
                                rgba=col,
                                e=persp,
                                c=-persp,
                                shift=shift,
                                scale=scale)


class MshObj():
    def __init__(self, tt, r, scale, shift, persp):
        self.tt = tt
        self.r = r
        self.scale = scale
        self.shift = shift
        self.persp = persp
    
    def plot(self, draw, rgba=(100,100,100,40)):
       plot_all_faces(self.tt, draw, self.r, shift=self.shift,
                    scale=self.scale, persp=self.persp)

##########

adjs = [rand_msh(i).adj for i in [3, 500, 200, 681]]
mos = []
j = 0
k = 0
im_no = 0
msh_posns = [(-12,12), (12,12), (12,-12),(-12,-12)]
r1 = np.eye(4)
for adj1 in adjs:
    msh_pos = msh_posns[j]
    r0=rotation(4, np.pi*17/60.0*14/10.0)
    rr1 = rotate_matrix_to_another(r0, r1, n=24)
    for i in range(25):
        scale=105-i*3.0
        im = Image.new("RGB", (1024, 1024), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        tf = tg.TsrctFcGraph(angle=np.pi/48*i, adj=adj1)
        tf.r = r0
        open_given_cube(tf, i=i, base_fc='00-+')
        plot_all_faces(tf, draw, tf.r, persp=5,shift=np.array([514, 595, 0, 0]),
                scale=scale, rgba=(100,100,100,40))
        print(str(im_no) + ":"+str(scale))
        for mo in mos:
            mo.plot(draw)
        im.save("Images//RotatingCube//im" +
                    str(im_no).rjust(4, '0') + ".png")
        im_no = im_no+1
        r0 = np.dot(rr1,r0)
    tf1 = deepcopy(tf)
    tf1.angle=np.pi/2; tf1.theta=np.pi/2
    mo1 = MshObj(tf, r1, 15,
                 np.array([514+i*msh_pos[0],
                           595+i*msh_pos[1], 0, 0]),
                           5+10*i)

    for k in range(10):
        scale1 = 105-24*3.0
        scale2 = 15
        shift1 = np.array([514, 595, 0, 0])
        shift2 = np.array([514+i*msh_pos[0],
                           595+i*msh_pos[1], 0, 0])
        shift = shift1+k/9*(shift2-shift1)
        scale = scale1+k/9*(scale2-scale1)
        im = Image.new("RGB", (1024, 1024), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        tf = tg.TsrctFcGraph(angle=np.pi/2, adj=adj1)
        tf.r = r0
        open_given_cube(tf, i=i, base_fc='00-+')
        plot_all_faces(tf, draw, tf.r, persp=5+10*i,shift=shift,
                scale=scale, rgba=(100,100,100,40))
        print(str(im_no) + ":"+str(scale))
        for mo in mos:
            mo.plot(draw)
        im.save("Images//RotatingCube//im" +
                    str(im_no).rjust(4, '0') + ".png")
        im_no = im_no+1
    mos.append(mo1)

    r0 = np.dot(rr1.T,r0)
    for i in range(25):
        scale2=105
        scale1=15
        scale = scale1+i/24*(scale2-scale1)
        shift2=np.array([514, 595, 0, 0])
        shift1=np.array([514+24*msh_pos[0],
                           595+24*msh_pos[1], 0, 0])
        shift=shift1+i/24*(shift2-shift1)
        im = Image.new("RGB", (1024, 1024), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        tf = tg.TsrctFcGraph(angle=np.pi/48*(24-i), adj=adj1)
        tf.r = r0
        open_given_cube(tf, i=i, base_fc='00-+')
        plot_all_faces(tf, draw, tf.r, persp=5,shift=shift,
                scale=scale, rgba=(100,100,100,40))
        for mo in mos:
            mo.plot(draw)
        im.save("Images//RotatingCube//im" +
                    str(im_no).rjust(4, '0') + ".png")
        print(str(im_no) + ":"+str(scale))
        im_no = im_no+1
        r0 = np.dot(rr1.T,r0)
    j = j+1

################

#scene-19
for i in range(49):
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tf = tg.TsrctFcGraph(angle=np.pi/24*i, adj=None)
    tf.draw = draw
    tf.r = rotation(4, np.pi*17/60.0*14/10.0)
    #tf.r = np.eye(4)
    open_given_cube(tf, i=i, base_fc='+00+')
    if i <= 12:
        scale = 105-i*2.7
    elif i <= 24:
        scale = 105-12*2.7+(i-12)*2.7
    else:
        scale = 105
    plot_all_faces(tf, tf.draw, tf.r, persp=5,shift=np.array([514, 595, 0, 0]),
            scale=scale, rgba=(100,100,100,40))
    #print(105-min(i,21)*2.7)
    im.save("Images//RotatingCube//im" +
                str(i).rjust(4, '0') + ".png")

