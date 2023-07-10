import numpy as np

#230701
from pyray.rotation2.rotn_4d import rotate_abt_plane
from PIL import Image, ImageDraw
from copy import deepcopy
from pyray.shapes.fourd.tsrct_cube_graph import primitive_tsrct_open,\
    TsrctCubeTree, TsrctCube
from pyray.rotation import rotation, axis_rotation
from pyray.shapes.fourd.tesseract_graph import Face1
from pyray.rotation import rotate_matrix_to_another
from pyray.shapes.fourd.tsrct_cube_graph import MshObj
from pyray.shapes.fourd.tsrct_cube_graph import get_common_face


## Just an experiment to see if rotation is stable.
pt1 = np.array([1,0,0,.5])
pt2 = np.array([0,1,0.7,0])
pt3 = np.array([1,1,0,1])

pt4 = np.array([1,1,1,0])
pt5 = np.array([1,1,1,1])
scale = 100
shift = np.array([256, 256, 0, 0])

for i in range(41):
    im = Image.new("RGB", (1024, 1024), (256, 256, 256))
    draw = ImageDraw.Draw(im, 'RGBA')
    pts1 = rotate_abt_plane(np.array([deepcopy(pt4), deepcopy(pt5)]), 
                            pt1, pt2, pt3,
                            np.pi*i/20.0)
    pts1 = pts1 * scale + shift
    for pt in pts1:
        draw.ellipse((pt[0]-7, pt[1]-7, pt[0]+7, pt[1]+7),
                     fill = (255,0,0),
                     outline = (0,0,0))
        #draw.line((pt[0], pt[1], 256, 256),
        #    fill = (255,255,255), width = 7)
    im.save("Images//RotatingCube//im" +
                            str(i).rjust(4, '0') +
                            ".png")

# And yes, if we check for the determinant then the rotation stays stable.


# cd /Users/rohitpandey/Documents/github/pyray
# scene-xx: money shot. A cube turning all the way inside out.
for i in range(57):
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
    r=rotation(4, np.pi*17/60.0*14/10.0)
    tt.plot(draw, r, rgba=(100,100,100,40),
            shift=np.array([514, 595, 0, 0]),
            scale=105)
    tt.cube_map['0+00'].plot_perspective(draw, r, rgba=(255,0,0,40),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    tt.cube_map['00-0'].plot_perspective(draw, r, rgba=(255,255,0,40),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    tt.cube_map['000+'].plot_perspective(draw, r, rgba=(255,0,255,40),
                                         shift=np.array([514, 595, 0, 0]),
                                         scale=105)
    im.save("Images//RotatingCube//im" +
                            str(i).rjust(4, '0') +
                            ".png")


r=rotation(4, np.pi*17/60.0*14/10.0)
for i in range(15):
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tf = TsrctCubeTree()
    c0 = tf.cube_map['000-']
    c1 = tf.cube_map['00-0']
    c2 = tf.cube_map['0+00']
    f1 = get_common_face(c0.key, c1.key)
    fc1 = c0.faces[f1]
    ax1, ax2, ax3 = fc1.vertices[0], fc1.vertices[1], fc1.vertices[2]
    c1.rotate(ax1, ax2, ax3, -np.pi*i/28.0)
    c2.rotate(ax1, ax2, ax3, -np.pi*i/28.0)
    f2 = get_common_face(c1.key, c2.key)
    fc1 = c2.faces[f2]
    ax1, ax2, ax3 = fc1.vertices[0], fc1.vertices[1], fc1.vertices[2]
    c2.rotate(ax1, ax2, ax3, np.pi*i/28.0)
    c0.plot_perspective(draw, r, rgba=(255,255,255,40),
                        shift=np.array([514, 595, 0, 0]),
                        scale=105)
    c1.plot_perspective(draw, r, rgba=(255,255,0,40),
                        shift=np.array([514, 595, 0, 0]),
                        scale=105)
    c2.plot_perspective(draw, r, rgba=(255,0,0,40),
                        shift=np.array([514, 595, 0, 0]),
                        scale=105)
    im.save("Images//RotatingCube//im" +
                            str(i).rjust(4, '0') +
                            ".png")

#230702

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
