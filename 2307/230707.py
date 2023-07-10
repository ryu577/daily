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


r2 = rotn_1(i=6.5)
r1 = rotation(4, np.pi*17/60.0*14/10.0)
#rr2 = rotate_matrix_to_another(r1, r2, n=15)
r2_3d = axis_rotation(np.array([0,0,0]),
                      np.array([1,2,1]),
                      np.pi/14)[:3,:3]
rr2 = np.eye(4)
rr2[1:4,1:4] = r2_3d

# cd /Users/rohitpandey/Documents/github/pyray
# scene-11_1
for i in range(18):
    tt = TsrctCubeTree()
    tt.bfs('000-')
    tt.reset_vert_col()
    #tt.theta = np.pi/20.0*i
    tt.theta = 0.0
    tt.dfs_flatten('000-')
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tt.plot(draw, r1, rgba=(100,100,100,40), shift=np.array([514, 595, 0, 0]),
            scale=105)
    tt.cube_map['+000'].plot_perspective(draw, r1, rgba=(255,255,0,10),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    im.save("Images//RotatingCube//im" +
                            str(i).rjust(4, '0') +
                            ".png")
    r1 = np.dot(rr2, r1)


# scene-11_2
# Remove the images from previous scene and then run this one.
r1 = rotation(4, np.pi*17/60.0*14/10.0)
for i in range(29-18):
    tt = TsrctCubeTree()
    tt.bfs('000-')
    tt.reset_vert_col()
    #tt.theta = np.pi/20.0*i
    tt.theta = 0.0
    tt.dfs_flatten('000-')
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tt.plot(draw, r1, rgba=(100,100,100,40), shift=np.array([514, 595, 0, 0]),
            scale=105)
    tt.cube_map['+000'].plot_perspective(draw, r1, rgba=(255,255,0,10),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    im.save("Images//RotatingCube//im" +
                            str(i).rjust(4, '0') +
                            ".png")
    r1 = np.dot(rr2, r1)


# scene-11_3
r1 = rotation(4, np.pi*17/60.0*14/10.0)
for i in range(2):
    tt = TsrctCubeTree()
    tt.bfs('000-')
    tt.reset_vert_col()
    #tt.theta = np.pi/20.0*i
    tt.theta = 0.0
    tt.dfs_flatten('000-')
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tt.plot(draw, r1, rgba=(100,100,100,40), shift=np.array([514, 595, 0, 0]),
            scale=105)
    tt.cube_map['+000'].plot_perspective(draw, r1, rgba=(255,255,0,10),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    tt.cube_map['000-'].plot_perspective(draw, r1, rgba=(255,0,0,10),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    if i > 0:
        tt.cube_map['0+00'].plot_perspective(draw, r1, rgba=(255,0,255,10),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    im.save("Images//RotatingCube//im" +
                            str(i).rjust(4, '0') +
                            ".png")


# scene-12: money shot. A cube turning all the way inside out.
r=rotation(4, np.pi*17/60.0*14/10.0)
for i in range(15):
    print("#############")
    tt = TsrctCubeTree(free_rot=True)
    tt.adj = {
            '000-': ['00-0','+000','0-00','-000','0+00','00+0'],
            '00-0': ['000+']
        }
    tt.bfs('000-')
    tt.reset()
    tt.reset_vert_col()
    tt.theta = np.pi/28.0*i
    #tt.cube_map['0+00'].rot_sign = 1
    tt.dfs_flatten('000-')
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tt.plot(draw, r, rgba=(100,100,100,40),
            shift=np.array([514, 595, 0, 0]),
            scale=105)
    tt.cube_map['+000'].plot_perspective(draw, r1, rgba=(255,255,0,10),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    tt.cube_map['000-'].plot_perspective(draw, r1, rgba=(255,0,0,10),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    tt.cube_map['0+00'].plot_perspective(draw, r1, rgba=(255,0,255,10),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    im.save("Images//RotatingCube//im" +
                            str(i).rjust(4, '0') +
                            ".png")


# scene-12_1: money shot. A cube turning all the way inside out.
r=rotation(4, np.pi*17/60.0*14/10.0)
for i in range(14, 29):
    print("#############")
    tt = TsrctCubeTree(free_rot=True)
    tt.adj = {
            '000-': ['00-0','+000','0-00','-000','0+00','00+0'],
            '00-0': ['000+']
        }
    tt.bfs('000-')
    tt.reset()
    tt.reset_vert_col()
    tt.theta = np.pi/28.0*i
    #tt.cube_map['0+00'].rot_sign = 1
    tt.dfs_flatten('000-')
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tt.plot(draw, r, rgba=(100,100,100,40),
            shift=np.array([514, 595, 0, 0]),
            scale=105)
    tt.cube_map['+000'].plot_perspective(draw, r1, rgba=(255,255,0,10),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    tt.cube_map['000-'].plot_perspective(draw, r1, rgba=(255,0,0,10),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    tt.cube_map['0+00'].plot_perspective(draw, r1, rgba=(255,0,255,10),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    im.save("Images//RotatingCube//im" +
                            str(i-14).rjust(4, '0') +
                            ".png")


# scene-12_2: money shot. A cube turning all the way inside out.
r=rotation(4, np.pi*17/60.0*14/10.0)
for i in range(28, 43):
    print("#############")
    tt = TsrctCubeTree(free_rot=True)
    tt.adj = {
            '000-': ['00-0','+000','0-00','-000','0+00','00+0'],
            '00-0': ['000+']
        }
    tt.bfs('000-')
    tt.reset()
    tt.reset_vert_col()
    tt.theta = np.pi/28.0*i
    #tt.cube_map['0+00'].rot_sign = 1
    tt.dfs_flatten('000-')
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tt.plot(draw, r, rgba=(100,100,100,40),
            shift=np.array([514, 595, 0, 0]),
            scale=105)
    tt.cube_map['+000'].plot_perspective(draw, r1, rgba=(255,255,0,10),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    tt.cube_map['000-'].plot_perspective(draw, r1, rgba=(255,0,0,10),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    tt.cube_map['0+00'].plot_perspective(draw, r1, rgba=(255,0,255,10),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    im.save("Images//RotatingCube//im" +
                            str(i-28).rjust(4, '0') +
                            ".png")


# scene-12_3: money shot. A cube turning all the way inside out.
r=rotation(4, np.pi*17/60.0*14/10.0)
for i in range(42, 57):
    print("#############")
    tt = TsrctCubeTree(free_rot=True)
    tt.adj = {
            '000-': ['00-0','+000','0-00','-000','0+00','00+0'],
            '00-0': ['000+']
        }
    tt.bfs('000-')
    tt.reset()
    tt.reset_vert_col()
    tt.theta = np.pi/28.0*i
    #tt.cube_map['0+00'].rot_sign = 1
    tt.dfs_flatten('000-')
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tt.plot(draw, r, rgba=(100,100,100,40),
            shift=np.array([514, 595, 0, 0]),
            scale=105)
    tt.cube_map['+000'].plot_perspective(draw, r1, rgba=(255,255,0,10),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    tt.cube_map['000-'].plot_perspective(draw, r1, rgba=(255,0,0,10),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    tt.cube_map['0+00'].plot_perspective(draw, r1, rgba=(255,0,255,10),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    im.save("Images//RotatingCube//im" +
                            str(i-42).rjust(4, '0') +
                            ".png")


###############
# scene-yy: See 230709 instead.
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

###############
tf = TsrctFcGraph3(angle=0.0)
#tf.adj, tf.face_map = scope_graph(tf.adj, tf.face_map)
tf.bfs('+00+')
tf.reset()
r=rotation(4, np.pi*17/60.0*14/10.0)
im = Image.new("RGB", (1024, 1024), (0, 0, 0))
draw = ImageDraw.Draw(im, 'RGBA')
tf.plot(draw, r, persp=5,shift=np.array([514, 595, 0, 0]),
                                         scale=105)
im.save("Images//RotatingCube//im" +
                    str(0).rjust(4, '0') +
                    ".png")
for i in range(91):
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tf.theta = np.pi/42.0*(i+1)
    for j in range(tf.max_depth):
        tf.reset()
        tf.curr_d = j+1
        tf.dfs('+00+')
    if i < 63:
        tf.plot(draw, r, persp=5,shift=np.array([514, 595, 0, 0]),
            scale=105-min(i,26)*2.7)
    else:
        tf.plot(draw, r, persp=5,shift=np.array([514, 595, 0, 0]),
            scale=105-(26+max((i-64),-26))*2.7)
    tf.reset()
    im.save("Images//RotatingCube//im" +
                    str(i+1).rjust(4, '0') +
                    ".png")

##################
## Failed experiment. Didn't work.
r=rotation(4, np.pi*17/60.0*14/10.0)
for i in range(15):
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tf = TsrctFcGraph3(angle=np.pi/28.0*i)
    tf.theta = np.pi/28.0*i
    tf.angle = np.pi/28.0*i
    tf.bfs('+00+')
    tf.reset()
    tf.dfs('+00+')
    tf.plot(draw, r, persp=5)
    im.save("Images//RotatingCube//im" +
                    str(i).rjust(4, '0') +
                    ".png")


