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


#from 230611
#tags, #img, #image, #pixel, #manipulation
# Looping through pixels: https://www.geeksforgeeks.org/how-to-manipulate-the-pixel-values-of-an-image-using-python/
def dull_im(im, ix=3):
    pixel_map = im.load()
    width, height = im.size
    dim = 1-0.2*ix
    for i in range(width):
        for j in range(height):
            r, g, b = im.getpixel((i, j))
            # Apply formula of grayscale:
            grayscale = (0.299*r + 0.587*g + 0.114*b)
            pixel_map[i, j] = (int(r*dim), int(g*dim), int(b*dim))
    #im.save("tst2.png")
    return im

def make_persp_portal(im, r=np.eye(3), scale=60):
    draw = ImageDraw.Draw(im, 'RGBA')
    #778
    e = 6; c = -6
    for st in ['0+0','0-0','+00','-00']:
        f = Face(st)
        f.plot_perspective(draw, r, scale=scale,
                shift=np.array([514, 595, 0, 0]),
                rgba=(12, 90, 190, 90),
                wdh=1,e=e, c=c)
    #im.save("tst1.png")
    return im

# scene-10
for ii in range(10):
    im = Image.open(r"ryu576_Demonstrating_prespective_projection_with_a_cubical_tunn_b4457cf3-f6b1-4e98-bf23-a63a365b7668.png")
    im = dull_im(im, 5)
    r = axis_rotation(np.array([0,0,0]), np.array([0,1,0]),
        					12*2*np.pi/12)[:3,:3]
    im = make_persp_portal(im, r, scale=60+ii*5)
    im.save("tst" + str(ii) + ".png")


# cd /Users/rohitpandey/Documents/github/pyray
# scene-11
for i in range(15):
    tt = TsrctCubeTree()
    tt.bfs('000-')
    tt.reset_vert_col()
    #tt.theta = np.pi/20.0*i
    tt.theta = 0.0
    tt.dfs_flatten('000-')
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    r=rotation(4, np.pi*17/60.0*i/10.0)
    tt.plot(draw, r, rgba=(100,100,100,40), shift=np.array([514, 595, 0, 0]),
            scale=105)
    im.save("Images//RotatingCube//im" +
                            str(i).rjust(4, '0') +
                            ".png")

# cd /Users/rohitpandey/Documents/github/pyray
# scene-12
for i in range(15):
    tt = TsrctCubeTree()
    tt.bfs('000-')
    tt.reset_vert_col()
    tt.theta = np.pi/28.0*i
    tt.dfs_flatten('000-')
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    r=rotation(4, np.pi*17/60.0*14/10.0)
    tt.plot(draw, r, rgba=(100,100,100,40),
            shift=np.array([514, 595, 0, 0]),
            scale=105)
    im.save("Images//RotatingCube//im" +
                            str(i).rjust(4, '0') +
                            ".png")


#230617
# scene-x
# All experimentation from here.
tt = TsrctCubeTree()
tt.bfs('000-')
tt.reset_vert_col()
tt.theta = np.pi/2.0
tt.dfs_flatten('000-')
r0=rotation(4, np.pi*17/60.0*14/10.0)
r1 = rotn_1(0)
rr1 = rotate_matrix_to_another(r0, r1)


for i in range(11):
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    r0 = np.dot(rr1, r0)
    tt.plot(draw, r0, rgba=(100,100,100,40), 
                shift=np.array([514, 595, 0, 0]),
                scale=105)
    im.save("Images//RotatingCube//im" +
                                str(i).rjust(4, '0') +
                                ".png")


for i in range(11):
    tt = TsrctCubeTree()
    tt.bfs('000-')
    tt.reset_vert_col()
    tt.theta = np.pi/2.0*(1-i/10.0)
    tt.dfs_flatten('000-')
    r1 = rotn_1(i)
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tt.plot(draw, r1, rgba=(100,100,100,40), 
                shift=np.array([514, 595, 0, 0]),
                scale=105)
    im.save("Images//RotatingCube//im" +
                                str(10+i).rjust(4, '0') +
                                ".png")


r1 = rotn_1(10)
r2_3d = axis_rotation(np.array([0,0,0]), np.array([1,1,1]),
                        2*np.pi/6)[:3,:3]
r2 = np.eye(4)
r2[:3,:3] = r2_3d
rr1 = rotate_matrix_to_another(r1, r2)


for i in range(11):
    tt = TsrctCubeTree()
    tt.adj = {
                '000-':['-000','+000','00-0','00+0'],
                '00-0':['0+00','000+'],
                '00+0':['0-00']
            }
    tt.bfs('000-')
    tt.reset_vert_col()
    tt.theta = min(np.pi/2.0*(i/10.0), np.pi/2)
    tt.dfs_flatten('000-')
    r1 = np.dot(rr1,r1)
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tt.plot(draw, r1, rgba=(100,100,100,40),
            shift=np.array([514, 595, 0, 0]),
            scale=105)
    im.save("Images//RotatingCube//im" +
            str(20+i).rjust(4, '0') +
            ".png")


r2_3d = axis_rotation(np.array([0,0,0]), np.array([0,1,1]),
                        -12*2*np.pi/12)[:3,:3]
r2 = np.eye(4)
r2[:3,:3] = r2_3d
rr1 = rotate_matrix_to_another(r1, r2)

for i in range(81):
    tt = TsrctCubeTree()
    tt.adj = {
                '000-':['-000','+000','00-0','00+0'],
                '00-0':['0+00','000+'],
                '00+0':['0-00']
            }
    tt.bfs('000-')
    tt.reset_vert_col()
    tt.theta = np.pi/2
    tt.dfs_flatten('000-')
    r1 = np.dot(rr1,r1)
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tt.plot(draw, r1, rgba=(100,100,100,40),
            shift=np.array([514, 595, 0, 0]),
            scale=105)
    im.save("Images//RotatingCube//im" +
            str(30+i).rjust(4, '0') +
            ".png")


#230618
#/Users/rohitpandey/Documents/github/pyray/pyray/shapes/fourd/tsrct_cube_graph.py


#pyray #rotation #scene #tesseract #4d #geometry
