import numpy as np
from pyray.rotation2.rotn_4d import rotate_abt_plane
from PIL import Image, ImageDraw
from copy import deepcopy
from pyray.shapes.fourd.tsrct_cube_graph import primitive_tsrct_open,\
    TsrctCubeTree, TsrctCube
from pyray.rotation import rotation, axis_rotation
from pyray.shapes.fourd.tesseract_graph import Face1
from pyray.rotation import rotate_matrix_to_another
from pyray.shapes.fourd.tsrct_cube_graph import get_common_face


#scene-13
def plot_colors(tt, draw, r, shift, scale, persp=5):
    tt.cube_map['+000'].plot_perspective(draw, r, rgba=(255,255,0,10),
                                         shift=shift,
                                         scale=scale, persp=persp)
    tt.cube_map['000-'].plot_perspective(draw, r, rgba=(255,0,0,10),
                                        shift=shift,
                                        scale=scale, persp=persp)
    tt.cube_map['0+00'].plot_perspective(draw, r, rgba=(255,0,255,10),
                                        shift=shift,
                                        scale=scale, persp=persp)

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
        plot_colors(self.tt, draw, self.r, self.shift,
                    self.scale, self.persp)

#scene-13
r1 = rotation(4, np.pi*17/60.0*14/10.0)
r2_3d = axis_rotation(np.array([0,0,0]),
                      np.array([1,1,1]),
                      2*np.pi/6)[:3,:3]
r2 = np.eye(4)
r2[:3,:3] = r2_3d
r3_3d = axis_rotation(np.array([0,0,0]),
                      np.array([0,0,1]),
                      2*np.pi/90)[:3,:3]
r3 = np.eye(4)
r3[:3,:3] = r3_3d
rr1 = rotate_matrix_to_another(r1, r2)

msh_posns = [(-12,12), (12,12), (12,-12),(-12,-12)]

adjs = [{
            '000-':['-000','+000','00-0','00+0'],
            '00-0':['0+00','000+'],
            '00+0':['0-00']
        }
        , {
            '000-': ['00-0','+000','0-00','-000','0+00','00+0'],
            '00-0': ['000+']
        }
        , {
            '000-':['00-0','00+0'],
            '00-0':['0+00','000+','+000','-000'],
            '00+0':['0-00']
        }
        , {
            '000-': ['00-0','0-00','00+0'],
            '00-0': ['000+','-000','+000','0+00']
        }
        ]
mos = []
j = 0
im_no = 0
for adj in adjs:
    msh_pos = msh_posns[j]
    for i in range(25):
        tt = TsrctCubeTree()
        tt.adj = adj
        tt.bfs('000-')
        tt.reset()
        tt.reset_vert_col()
        tt.theta = np.pi/48.0*i
        tt.dfs_flatten('000-')
        im = Image.new("RGB", (1024, 1024), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        r=rotation(4, np.pi*17/60.0*14/10.0)
        tt.plot(draw, r, rgba=(100,100,100,40),
                shift=np.array([514, 595, 0, 0]),
                scale=105)
        plot_colors(tt, draw, r, np.array([514, 595, 0, 0]), 105)
        for mo in mos:
            mo.r = np.dot(r3, mo.r)
            mo.plot(draw)
        im.save("Images//RotatingCube//im" +
                                str(i+j*50).rjust(4, '0') +
                                ".png")
        im_no += 1

    for i in range(25):
        im = Image.new("RGB", (1024, 1024), (0, 0, 0))
        draw = ImageDraw.Draw(im, 'RGBA')
        tt = TsrctCubeTree()
        tt.adj = adj
        tt.bfs('000-')
        tt.reset()
        tt.reset_vert_col()
        tt.theta = np.pi/48.0*(24-i)
        tt.dfs_flatten('000-')
        tt.plot(draw, r, rgba=(100,100,100,40),
                shift=np.array([514, 595, 0, 0]),
                scale=105)
        plot_colors(tt, draw, r, np.array([514, 595, 0, 0]), 105)
        tt1 = TsrctCubeTree()
        tt1.adj = adj
        tt1.bfs('000-')
        tt1.reset_vert_col()
        tt1.theta = np.pi/2
        tt1.dfs_flatten('000-')
        tt1.plot(draw, r1, rgba=(100,100,100,40),
                shift=np.array([514+i*msh_pos[0], 595+i*msh_pos[1], 0, 0]),
                scale=105*(25-i/1.4)/25, persp=(5+i*10))
        plot_colors(tt1, draw, r1, np.array([514+i*msh_pos[0], 595+i*msh_pos[1], 0, 0]), 
                    105*(25-i/1.4)/25, (5+i*10))
        r1 = np.dot(rr1, r1)
        for mo in mos:
            mo.r = np.dot(r3, mo.r)
            mo.plot(draw)
        im.save("Images//RotatingCube//im" +
                                str(i+j*50+25).rjust(4, '0') +
                                ".png")
        im_no += 1
    j = j+1
    mo1 = MshObj(tt1, r1, 105*(25-i/1.4)/25,
                 np.array([514+i*msh_pos[0],
                           595+i*msh_pos[1], 0, 0]),
                           5+10*i)
    mos.append(mo1)
    r1 = rotation(4, np.pi*17/60.0*14/10.0)


for k in range(25):
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tt = TsrctCubeTree()
    tt.adj = adj
    tt.bfs('000-')
    tt.reset()
    tt.reset_vert_col()
    tt.theta = np.pi/48.0*(0)
    tt.dfs_flatten('000-')
    tt.plot(draw, r, rgba=(100,100,100,40),
            shift=np.array([514, 595, 0, 0]),
            scale=105)
    plot_colors(tt, draw, r, np.array([514, 595, 0, 0]), 105)
    for mo in mos:
        mo.r = np.dot(r3, mo.r)
        mo.plot(draw)
    im.save("Images//RotatingCube//im" +
                                str(im_no+k).rjust(4, '0') +
                                ".png")

