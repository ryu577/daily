import numpy as np
from itertools import combinations
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.shapes.solid.open_cube import map_to_plot, plot_grid
import pyray.shapes.fourd.tesseract_graph as tg
from pyray.rotation import rotation
from pyray.shapes.fourd.open_tsrct import open_given_cube
from pyray.shapes.fourd.tesseract_graph import plot_all_faces2
from pyray.rotation import general_rotation
from pyray.rotation import rotate_matrix_to_another


def plot_all_faces3(tf, draw, r, kk1, pos=0, persp=0, rgba=(10,31,190,80),
                    shift=np.array([514, 595, 0, 0]),scale=105):
    """
    Plots all faces of a TeseractFaceGraph in perspective projection.
    """
    for kk in tf.face_map.keys():
        if kk[pos] == kk1:
            ff = tf.vert_props[kk]
            ff.plot_perspective(draw, r,
                                rgba=rgba,
                                e=persp,
                                c=-persp,
                                shift=shift,
                                scale=scale)


# Generate all edges of a 4-d cube.
for i in ['+', '-']:
    for j in ['+', '-']:
        for k in ['+', '-']:
            for u in combinations(np.arange(4),3):
                x = np.array(['0']*4)
                x[[ix for ix in u]] = [i, j, k]
                print(x)


def map_perspective(pt, r=np.eye(3),
                         shift = np.array([256,256,0]),
                         scale = 35, e=4, c=-4):
        rotated_face = np.transpose(np.dot(r, np.transpose(pt)))
        rot = rotated_face
        az = rot[len(rot)-1]
        for i in range(len(rot)-1):
            rot[i] = e*rot[i]/(az-c)
        rot = rot * scale + shift
        return rot


####################################
## 230805
# scene33
scl=105
shft= np.array([514, 595, 0, 0])
r1 = np.eye(4)
r1[:3,:3] = general_rotation(np.array([1,1,1]), np.pi/6)
r2 = rotation(4, np.pi*17/60.0*14/10.0)
rr1 = rotate_matrix_to_another(r1, r2,n=55)

for i in range(71):
    kk = '00++'
    pp = max(60-i, 5)
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tf = tg.TsrctFcGraph(angle=0.0, adj=None)
    tf.draw = draw
    #tf.r = rotation(4, np.pi*17/60.0*14/10.0)
    tf.r = r1
    open_given_cube(tf, i=i)
    plot_all_faces2(tf, tf.draw, tf.r, '', persp=pp,
                    shift=shft,
                    scale=scl, rgba=(100,100,100,40))
    font = ImageFont.truetype("Arial.ttf", 25)
    # draw.text((700,700), str(i), font=font)
    pt1 = np.array([1,1,1,1])
    pt2 = np.array([-1,1,1,1])
    pt1 = map_perspective(pt1, tf.r, shft, scl,e=pp,c=-pp)
    pt2 = map_perspective(pt2, tf.r, shft, scl,e=pp,c=-pp)
    # ff = tf.vert_props['0+0+']
    # ff.plot_perspective(draw, tf.r,
    #                             rgba=(255,255,0,40),
    #                             e=pp,
    #                             c=-pp,
    #                             shift=shft,
    #                             scale=scl)
    
    draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), 
                          fill=(255,0,0), width=3)
    plot_all_faces3(tf, draw, tf.r, '+', 1, persp=pp, rgba=(130, 91, 220, 50),
                    shift=shft, scale=scl)
    plot_all_faces3(tf, draw, tf.r, '+', 2, persp=pp, rgba=(20, 91, 228, 50),
                    shift=shft, scale=scl)
    ff = tf.vert_props['0++0']
    ff.plot_perspective(draw, tf.r,
                                rgba=(255,0,0,90),
                                e=pp,
                                c=-pp,
                                shift=shft,
                                scale=scl)
    im.save("Images//RotatingCube//im" +
                str(i).rjust(4, '0') + ".png")
    r1 = np.dot(rr1, r1)


# scene34
# Requires r1 from the previous scene.
r1 = np.eye(4)
r1[:3,:3] = general_rotation(np.array([1,1,1]), np.pi/6)
r2 = rotation(4, np.pi*17/60.0*14/10.0)
rr1 = rotate_matrix_to_another(r1, r2,n=55)
for i in range(71):
    r1 = np.dot(rr1, r1)
r2 = rotation(4, np.pi*17/60.0*14/10.0)
rr1 = rotate_matrix_to_another(r1, r2,n=24)

face_map = {'--00': 0, '-0-0': 1,
            '-00-': 2, '-00+': 3, 
            '-0+0': 4, '-+00': 5,
            '0--0': 6, '0-0-': 7, 
            '0-0+': 8, '0-+0': 9,
            '0+-0':10, '0+0-':11,
            '0+0+':12, '0++0':13,
            '00--':14, '00-+':15, 
            '00+-':16, '00++':17,
            '+-00':18, '+0-0':19,
            '+00-':20, '+00+':21,
            '+0+0':22,'++00':23}
faces = [k for k in face_map.keys()]

for i in range(24):
    kk = faces[i]
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tf = tg.TsrctFcGraph(angle=0.0, adj=None)
    tf.draw = draw
    tf.r = r1
    open_given_cube(tf, i=i)
    plot_all_faces2(tf, tf.draw, tf.r, kk, 
                    persp=5,shift=np.array([514, 595, 0, 0]),
            scale=105, rgba=(100,100,100,40), rgba2=(20,91,228,50))
    font = ImageFont.truetype("Arial.ttf", 55)
    draw.text((700,700), str(i+1), font=font)
    im.save("Images//RotatingCube//im" +
                str(i).rjust(4, '0') + ".png")
    r1 = np.dot(rr1, r1)


# scene35
ix = 0
shift = np.array([514, 595, 0, 0])
scale = 105
# Generate the end points of each edge.
for i in [1, -1]:
    for j in [1, -1]:
        for k in [1, -1]:
            for u in combinations(np.arange(4),3):
                im = Image.new("RGB", (1024, 1024), (0, 0, 0))
                draw = ImageDraw.Draw(im, 'RGBA')
                tf = tg.TsrctFcGraph(angle=0.0, adj=None)
                tf.draw = draw
                tf.r = rotation(4, np.pi*17/60.0*14/10.0)
                r = tf.r
                plot_all_faces2(tf, tf.draw, tf.r, '',
                                persp=5,shift=shift,
                                scale=scale, 
                                rgba=(100,100,100,40))
                x = np.array([0]*4)
                x[[ix for ix in u]] = [i, j, k]
                pt1 = np.copy(x)
                pt1[pt1 == 0] = 1
                pt1 = map_perspective(pt1, r, shift, scale, e=5,c=-5)
                pt2 = np.copy(x)
                pt2[pt2 == 0] = -1
                pt2 = map_perspective(pt2, r, shift, scale, e=5,c=-5)
                pts = np.array([pt1, pt2])
                draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), 
                          fill=(255,0,0), width=3)
                font = ImageFont.truetype("Arial.ttf", 75)
                draw.text((700,700), str(ix+1), font=font)
                im.save("Images//RotatingCube//im" +
                    str(ix).rjust(4, '0') + ".png")
                ix += 1


####################################
## 230805
# scene36
scl=105
shft= np.array([514, 595, 0, 0])
r1 = rotation(4, np.pi*17/60.0*14/10.0)
r2 = np.eye(4)
r2[:3,:3] = general_rotation(np.array([1,1,0]), np.pi/4)

rr1 = rotate_matrix_to_another(r1, r2,n=100)

for i in range(101):
    kk = '00++'
    pp = 5
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tf = tg.TsrctFcGraph(angle=0.0, adj=None)
    tf.draw = draw
    #tf.r = rotation(4, np.pi*17/60.0*14/10.0)
    tf.r = r1
    open_given_cube(tf, i=i)
    plot_all_faces2(tf, tf.draw, tf.r, '', persp=pp,
                    shift=shft,
                    scale=scl, rgba=(100,100,100,40))
    font = ImageFont.truetype("Arial.ttf", 25)
    # draw.text((700,700), str(i), font=font)
    pt1 = np.array([1,1,1,1])
    pt2 = np.array([1,1,1,-1])
    pt1 = map_perspective(pt1, tf.r, shft, scl,e=pp,c=-pp)
    pt2 = map_perspective(pt2, tf.r, shft, scl,e=pp,c=-pp)
    
    if i > 20:
        ff = tf.vert_props['0++0']
        ff.plot_perspective(draw, tf.r,
                                    rgba=(255,82,131,90),
                                    e=pp,
                                    c=-pp,
                                    shift=shft,
                                    scale=scl)
    if i> 40:
        ff = tf.vert_props['+0+0']
        ff.plot_perspective(draw, tf.r,
                                    rgba=(255,82,131,90),
                                    e=pp,
                                    c=-pp,
                                    shift=shft,
                                    scale=scl)
    if i > 56:
        ff = tf.vert_props['++00']
        ff.plot_perspective(draw, tf.r,
                                    rgba=(255,82,131,90),
                                    e=pp,
                                    c=-pp,
                                    shift=shft,
                                    scale=scl)
    draw.line((pt1[0], pt1[1], pt2[0], pt2[1]), 
                          fill=(255,0,0), width=3)
    im.save("Images//RotatingCube//im" +
                str(i).rjust(4, '0') + ".png")
    r1 = np.dot(rr1, r1)

