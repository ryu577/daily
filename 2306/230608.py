"""
Trying to see if applying a rotation matrix repeatedly to a point
keeps it in a circle.
"""
import numpy as np
from pyray.rotation import rotation, axis_rotation
from pyray.shapes.solid.open_cube_tst import tst_perspective
from PIL import Image, ImageDraw
from copy import deepcopy
from itertools import combinations
from pyray.shapes.solid.open_cube import Face

ii = 4
v = np.random.normal(size=ii)
modv = np.sqrt(np.sum(v**2))
v = v/modv
vs = [v]

r = rotation(ii, np.pi/8)

for i in range(7000):
    v = np.dot(r, v)
    vs.append(v)

vs = np.array(vs)

for i in range(40):
    r1 = rotation(ii, np.pi/2*i/10.0)
    vs1 = np.dot(vs, r1)
    im = Image.new("RGB", (512, 512), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    for v in vs1:
        vv1 = v*100+256
        draw.ellipse((vv1[0]-1,vv1[1]-1,vv1[0]+1,vv1[1]+1), 
                     fill=(120, 230, 91))
        vv_old = deepcopy(vv1)
    im.save("Images//RotatingCube//im" +
                    str(i).rjust(4, '0') +
                    ".png")

# 230610

#cd /Users/rohitpandey/Downloads/videos/open_tsrct/midjourney

# open method used to open different extension image file
im = Image.open(r"ryu576_Demonstrating_prespective_projection_with_a_cubical_tunn_b4457cf3-f6b1-4e98-bf23-a63a365b7668.png")

def make_persp_portal(im, r=np.eye(3)):
    draw = ImageDraw.Draw(im, 'RGBA')
    #778
    e = 6; c = -6; scale=60;
    for st in ['0+0','0-0','+00','-00']:
        f = Face(st)
        f.plot_perspective(draw, r, scale=scale,
                shift=np.array([514, 595, 0, 0]),
                rgba=(12, 90, 190, 90),
                wdh=1,e=e, c=c)
    #im.save("tst1.png")
    return im


#230611
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

# scene-7
# Might be misleading. The real scene-7 is in pyray/videos/flatten_4d_cube/make_scene6
for ii in range(6):
    im = Image.open(r"ryu576_Demonstrating_prespective_projection_with_a_cubical_tunn_b4457cf3-f6b1-4e98-bf23-a63a365b7668.png")
    im = dull_im(im, ii)
    im = make_persp_portal(im)
    im.save("tst" + str(ii) + ".png")


for ii in range(10):
    im = Image.open(r"ryu576_Demonstrating_prespective_projection_with_a_cubical_tunn_b4457cf3-f6b1-4e98-bf23-a63a365b7668.png")
    im = dull_im(im, 5)
    r = axis_rotation(np.array([0,0,0]), np.array([0,1,0]),
        					ii*2*np.pi/12)[:3,:3]
    im = make_persp_portal(im, r)
    im.save("tst" + str(ii) + ".png")

