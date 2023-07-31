import numpy as np
from pyray.shapes.fourd.open_tsrct import TsrctFcGraph2
from pyray.rotation import rotation
from pyray.shapes.fourd.tsrct_cube_graph import primitive_tsrct_open,\
    TsrctCubeTree, open_tsrct_proper
import pyray.shapes.solid.open_cube as oc
from pyray.rotation2.rotn_4d import get_common_verts
from pyray.shapes.solid.open_cube import map_to_plot, plot_grid
from pyray.rotation import general_rotation, yzrotation, xyrotation
from PIL import Image, ImageDraw
import numpy as np
from copy import deepcopy
from pyray.color import colorFromAngle2
from pyray.shapes.solid.polyhedron import render_solid_planes
from itertools import combinations
from pyray.shapes.solid.open_cube import GraphCube
import pyray.shapes.fourd.tesseract_graph as tg
from pyray.rotation import rotation
from PIL import Image, ImageDraw, ImageFont, ImageMath

## Cube with hsl
trees = \
[
    [('-00','00+'),('00+','+00'),('00+','0-0'),('0-0','00-'),('00-','0+0')],
    [('-00','00+'),('00+','0-0'),('0-0','+00'),('0-0','00-'),('00-','0+0')],
    [('-00','00+'),('00+','0-0'),('0-0','00-'),('00-','+00'),('00-','0+0')],
    [('-00','00+'),('00+','0-0'),('0-0','00-'),('00-','0+0'),('0+0','+00')],
    [('00+','0-0'),('0-0','-00'),('0-0','00-'),('00-','0+0'),('00-','+00')],
    [('00+','0-0'),('0-0','+00'),('0-0','-00'),('0-0','00-'),('00-','0+0')],
    #[('-00','00+'),('00+','0-0'),('0-0','00-'),('00-','0+0'),('0+0','+00')],
    [('00+','-00'),('-00','0-0'),('0-0','00-'),('0-0','+00'),('00-','0+0')],
    [('-00','00+'),('00+','0-0'),('0-0','+00'),('+00','00-'),('00-','0+0')],
    [('-00','00+'),('00+','0-0'),('0-0','00-'),('00-','+00'),('+00','0+0')],
    [('-00','00+'),('00+','0-0'),('0-0','+00'),('+00','00-'),('+00','0+0')],
    [('0+0','00-'),('00-','0-0'),('0-0','+00'),('+00','00+'),('00+','-00')]
 ]

gr = oc.GraphCube(survive_ros={0, 1, 2, 3, 6})
incl_lst = []
for i in range(len(trees)):
    tree = trees[i]
    j = 0
    surv = set()
    for ed in tree:
        if ed in gr.edg_dict:
            surv.add(gr.edg_dict[ed])
        elif ed in gr.rev_edg_dict:
            surv.add(gr.rev_edg_dict[ed])
        else:
            break
    incl_lst.append(surv)


for i in range(21):
    r = general_rotation(np.array([1,1,1]), np.pi/6)
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    gr = oc.GraphCube(survive_ros=incl_lst[4])
    #gr = oc.GraphCube(survive_ros={0, 1, 2, 3, 6})
    gr.angle = -np.pi*(0)/40.0
    #gr.angle = 0
    gr.dfs_flatten('0+0')
    gr.reset_vert_col()
    faces = []
    face_keys = []
    for kk in gr.vert_props.keys():
        faces.append(gr.vert_props[kk].vertices[[0,2,3,1]])
        face_keys.append(kk)
    scale = 105
    h = 153
    s = 120
    planes = faces
    for ix in range(len(planes)):
        plane = planes[ix]
        face_key = face_keys[ix]
        if face_key in {'0-0', '00+'}:
            shift = np.array([700-i*3,512-i*2,0])
        else:
            shift = np.array([700,512,0])
        plane1 = np.array(plane)
        plane1 = np.dot(plane1,r)
        #plane1 = orient_face(plane1)
        plane_center = sum(plane1)/len(plane1)
        cross_pdt = np.cross(plane1[0]-plane1[1], plane1[0]-plane1[2])
        cross_pdt = cross_pdt/np.sqrt(sum(cross_pdt**2))
        face_angle = abs(np.dot(cross_pdt, np.array([0,0,1.0])))
        plane1 = plane1*scale+shift[:3]
        rgba = colorFromAngle2(face_angle,h=h,s=s,maxx=1.0)
        rgba1 = rgba + (200,)
        poly = [(i[0], i[1]) for i in plane1]
        draw.polygon(poly, fill=rgba1)
        for idx in range(len(plane1)):
            draw.line((plane1[idx][0],plane1[idx][1],
                plane1[(idx+1)%len(plane1)][0],plane1[(idx+1)%len(plane1)][1]), 
                fill = rgba, width = 5)
    im.save("Images//RotatingCube//im" +
                str(i).rjust(4, '0') +
                ".png")


def plot_hsl(gr, draw, r, h=153, s=120,
             shift=np.array([700,512,0]),
             scale=105):
    faces = []
    face_keys = []
    for kk in gr.vert_props.keys():
        faces.append(gr.vert_props[kk].vertices[[0,2,3,1]])
        face_keys.append(kk)
    planes = faces
    for ix in range(len(planes)):
        plane = planes[ix]
        plane1 = np.array(plane)
        plane1 = np.dot(plane1,r)
        cross_pdt = np.cross(plane1[0]-plane1[1], plane1[0]-plane1[2])
        cross_pdt = cross_pdt/np.sqrt(sum(cross_pdt**2))
        cross_pdt = np.dot(cross_pdt, r)
        face_angle = abs(np.dot(cross_pdt, np.array([0,0,1.0])))
        plane1 = plane1*scale+shift[:3]
        rgba = colorFromAngle2(face_angle,h=h,s=s,maxx=1.0)
        rgba1 = rgba + (200,)
        poly = [(i[0], i[1]) for i in plane1]
        draw.polygon(poly, fill=rgba1)
        for idx in range(len(plane1)):
            draw.line((plane1[idx][0],plane1[idx][1],
                plane1[(idx+1)%len(plane1)][0],plane1[(idx+1)%len(plane1)][1]), 
                fill = rgba, width = 5)


##########################
## All the spanning trees for 3d->2d meshes.

mshs = []
survs = []
ixs = {11, 18, 23, 56, 60}
lst = np.arange(12)
ix = 0
r = general_rotation(np.array([1,1,1]), np.pi/6)
for combo in combinations(lst, 5):
    survive = set(combo)
    gr = GraphCube(survive, -np.pi/2)
    gr.dfs('0+0')
    if len(gr.black_verts) == 6:
        print(combo)
        im = Image.new("RGB", (512, 512), (0,0,0))
        draw = ImageDraw.Draw(im,'RGBA')
        gr.r = r
        gr.reset_vert_col()
        gr.dfs_flatten('0+0')
        gr.draw = draw
        gr.reset_vert_col()
        gr.dfs_plot_2('0+0')
        if ix in ixs:
            survs.append(survive)
            mshs.append(deepcopy(gr.adj))
            im.save("Images//RotatingCube//im" + str(ix) + ".png")
        ix += 1
print(ix)


## On visual inspection, meshes 11, 18, 23, 56 and 60 are the same.
# open the cube while highlighting the cuts.
for i in range(20):
    im = Image.new("RGB", (1024, 1024), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')
    gr = GraphCube(survive, -np.pi/38*i)
    gr.angle = -np.pi/38*i
    gr.adj = mshs[2]
    surv = survs[2]
    p = 0.0
    line_dat = []
    for j in range(12):
        if j not in surv:
            edge = gr.edges[j]
            f1 = gr.vert_props[edge[0]]
            f2 = gr.vert_props[edge[1]]
            v1 = get_common_verts(f1.vertices, f2.vertices)
            #rotated_verts = np.transpose(np.dot(r, np.transpose(v1)))
            rotated_verts = np.dot(v1, r)
            x, y = map_to_plot(rotated_verts[0][0], rotated_verts[0][1], scale=105, shift=(700,512))
            x1, y1 = map_to_plot(rotated_verts[1][0], rotated_verts[1][1], scale=105, shift=(700,512))
            x_mid = (x+x1)/2
            y_mid = (y+y1)/2
            xx = p*x_mid+(1-p)*x
            xx1 = p*x_mid+(1-p)*x1
            yy = p*y_mid+(1-p)*y
            yy1 = p*y_mid+(1-p)*y1
            #draw.line((xx, yy, xx1, yy1), fill=(120, 120, 0), width=10)
            line_dat.append((xx, yy, xx1, yy1))
    gr.dfs_flatten('0+0')
    gr.reset_vert_col()
    gr.r = r
    gr.draw = draw
    #gr.dfs_plot_2('0+0')
    plot_hsl(gr, draw, r)
    for ll in line_dat:
        draw.line(ll, fill=(120, 10, 90, 220), width=5)
    im.save("Images//RotatingCube//im" + str(i) + ".png")


def drw_lines(gr, surv, r, shift=(700,512), scale=105, p=0):
    line_dat = []
    for j in range(12):
        if j not in surv:
            edge = gr.edges[j]
            f1 = gr.vert_props[edge[0]]
            f2 = gr.vert_props[edge[1]]
            v1 = get_common_verts(f1.vertices, f2.vertices)
            rotated_verts = np.dot(v1, r)
            shift = (shift[0], shift[1])
            x, y = map_to_plot(rotated_verts[0][0], rotated_verts[0][1], scale=scale, shift=shift)
            x1, y1 = map_to_plot(rotated_verts[1][0], rotated_verts[1][1], scale=scale, shift=shift)
            x_mid = (x+x1)/2
            y_mid = (y+y1)/2
            xx = p*x_mid+(1-p)*x
            xx1 = p*x_mid+(1-p)*x1
            yy = p*y_mid+(1-p)*y
            yy1 = p*y_mid+(1-p)*y1
            line_dat.append((xx, yy, xx1, yy1))
    return line_dat


r = general_rotation(np.array([1,1,1]), np.pi/6)
#r = np.eye(3)
rr1 = general_rotation(np.array([1,0,1]), np.pi/12)
for i in range(25):
    im = Image.new("RGB", (1024, 1024), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')
    gr = GraphCube(survive, -np.pi/2)
    gr.angle = -np.pi/2
    gr.adj = mshs[2]
    gr.r = r
    gr.dfs_flatten('0+0')
    gr.reset_vert_col()
    gr.draw = draw
    #gr.dfs_plot_2('0+0')
    plot_hsl(gr, draw, r)
    r = np.dot(rr1, r)
    im.save("Images//RotatingCube//im" + str(i) + ".png")

####################
## Now the actual scenes.
# scene-26
r = general_rotation(np.array([1,1,1]), np.pi/6)
rr1 = general_rotation(np.array([1,0,1]), np.pi/12)
for i in range(25):
    im = Image.new("RGB", (1024, 1024), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')
    gr = GraphCube(survive, 0)
    #gr.angle = -np.pi/2
    gr.adj = mshs[2]
    gr.r = r
    gr.dfs_flatten('0+0')
    gr.reset_vert_col()
    gr.draw = draw
    #gr.dfs_plot_2('0+0')
    plot_hsl(gr, draw, r, shift=np.array([700-i*8, 512+i*8, 0]),
             scale=105*(1-i/70))
    plot_hsl(gr, draw, r, shift=np.array([700+i*8, 512-i*8, 0]),
             scale=105*(1-i/70))
    r = np.dot(rr1, r)
    im.save("Images//RotatingCube//im" + str(i) + ".png")


# scene-27: First cube gets its cuts.
shift1 = np.array([508,704,0])
shift2 = np.array([892,320,0])
shifts = [shift1, shift2]
scale = 69.0
ixs = [2, 3]

for i in range(25):
    gr1 = GraphCube(survive, 0)
    gr2 = GraphCube(survive, 0)
    grs = [gr1, gr2]
    im = Image.new("RGB", (1024, 1024), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')
    for j in range(2):
        msh = mshs[ixs[j]]
        surv = survs[ixs[j]]
        gr.__init__(surv, 0)
        shift = shifts[j]
        gr = grs[j]
        gr.adj = msh
        gr.r = r
        plot_hsl(gr, draw, r, shift=shift,
             scale=scale)
        line_dat = drw_lines(gr, surv, r, shift, scale, p=1-i/24)
        for ll in line_dat:
            if j < 1:
                draw.line(ll, fill=(120, 10, 90, 220), width=5)
    im.save("Images//RotatingCube//im" + str(i) + ".png")



# scene-28: Second cube gets its cuts.
shift1 = np.array([508,704,0])
shift2 = np.array([892,320,0])
shifts = [shift1, shift2]
scale = 69.0
ixs = [2, 3]

for i in range(25):
    gr1 = GraphCube(survive, 0)
    gr2 = GraphCube(survive, 0)
    grs = [gr1, gr2]
    im = Image.new("RGB", (1024, 1024), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')
    for j in range(2):
        msh = mshs[ixs[j]]
        surv = survs[ixs[j]]
        gr.__init__(surv, 0)
        shift = shifts[j]
        gr = grs[j]
        gr.adj = msh
        gr.r = r
        plot_hsl(gr, draw, r, shift=shift,
             scale=scale)
        if j == 0:
            p=0
        else:
            p=1-i/24
        line_dat = drw_lines(gr, surv, r, shift, scale, p=p)
        for ll in line_dat:
            draw.line(ll, fill=(120, 10, 90, 220), width=5)
    im.save("Images//RotatingCube//im" + str(i) + ".png")



# scene-29: First cube opening up.
shift1 = np.array([508,704,0])
shift2 = np.array([892,320,0])
shifts = [shift1, shift2]
scale = 69.0
ixs = [2, 3]

for i in range(25):
    gr1 = GraphCube(survive, 0)
    gr2 = GraphCube(survive, 0)
    grs = [gr1, gr2]
    im = Image.new("RGB", (1024, 1024), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')
    for j in range(2):
        msh = mshs[ixs[j]]
        surv = survs[ixs[j]]
        gr = grs[j]
        gr.__init__(surv, -np.pi*i/48)
        gr.adj = msh
        gr.angle = -np.pi*i/48.0
        shift = shifts[j]
        gr.r = r
        line_dat = drw_lines(gr, surv, r, shift, scale)
        if j == 0:
            gr.dfs_flatten('0+0')
            gr.reset_vert_col()
        plot_hsl(gr, draw, r, shift=shift,
             scale=scale)
        for ll in line_dat:
            draw.line(ll, fill=(120, 10, 90, 220), width=5)
    im.save("Images//RotatingCube//im" + str(i) + ".png")


# scene-30: Second cube opening up.
shift1 = np.array([508,704,0])
shift2 = np.array([892,320,0])
shifts = [shift1, shift2]
scale = 69.0
ixs = [2, 3]

for i in range(25):
    gr1 = GraphCube(survive, 0)
    gr2 = GraphCube(survive, 0)
    grs = [gr1, gr2]
    im = Image.new("RGB", (1024, 1024), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')
    for j in range(2):
        msh = mshs[ixs[j]]
        surv = survs[ixs[j]]
        gr = grs[j]
        gr.__init__(surv, -np.pi*i/48)
        gr.adj = msh
        if j == 0:
            gr.angle = -np.pi/2
        else:
            gr.angle = -np.pi*i/48.0
        shift = shifts[j]
        gr.r = r
        line_dat = drw_lines(gr, surv, r, shift, scale)
        gr.dfs_flatten('0+0')
        gr.reset_vert_col()
        plot_hsl(gr, draw, r, shift=shift,
             scale=scale)
        for ll in line_dat:
            draw.line(ll, fill=(120, 10, 90, 220), width=5)
    im.save("Images//RotatingCube//im" + str(i) + ".png")



# scene-31: Second mesh rotating.
shift1 = np.array([508,704,0])
shift2 = np.array([892,320,0])
shifts = [shift1, shift2]
scale = 69.0
ixs = [2, 3]
r = general_rotation(np.array([1,1,1]), np.pi/6)
r0 = general_rotation(np.array([1,1,1]), np.pi/6)
rr1 = general_rotation(np.array([1,0,1]), np.pi/12)

for i in range(13):
    gr1 = GraphCube(survive, 0)
    gr2 = GraphCube(survive, 0)
    grs = [gr1, gr2]
    im = Image.new("RGB", (1024, 1024), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')
    for j in range(2):
        msh = mshs[ixs[j]]
        surv = survs[ixs[j]]
        gr = grs[j]
        gr.__init__(surv, -np.pi*i/48)
        gr.adj = msh
        gr.angle = -np.pi/2
        shift = shifts[j]
        line_dat = drw_lines(gr, surv, r, shift, scale)
        gr.dfs_flatten('0+0')
        gr.reset_vert_col()
        if j == 0:
            plot_hsl(gr, draw, r, shift=shift,
                scale=scale)
        else:
            plot_hsl(gr, draw, r0, shift=shift,
                scale=scale)
    r = np.dot(rr1, r)
    im.save("Images//RotatingCube//im" + str(i) + ".png")


# scene-32: Bring the two meshes together.

scale = 69.0
ixs = [2, 3]
r = general_rotation(np.array([1,1,1]), np.pi/6)
r0 = general_rotation(np.array([1,1,1]), np.pi/6)
rr1 = general_rotation(np.array([1,0,1]), np.pi)
r = np.dot(rr1, r)

for i in range(12):
    shift1 = np.array([508+i*12,704-i*8,0])
    shift2 = np.array([892-i*12,320+i*8,0])
    shifts = [shift1, shift2]
    gr1 = GraphCube(survive, 0)
    gr2 = GraphCube(survive, 0)
    grs = [gr1, gr2]
    im = Image.new("RGB", (1024, 1024), (0,0,0))
    draw = ImageDraw.Draw(im,'RGBA')
    for j in range(2):
        msh = mshs[ixs[j]]
        surv = survs[ixs[j]]
        gr = grs[j]
        gr.__init__(surv, -np.pi*i/48)
        gr.adj = msh
        gr.angle = -np.pi/2
        shift = shifts[j]
        line_dat = drw_lines(gr, surv, r, shift, scale)
        gr.dfs_flatten('0+0')
        gr.reset_vert_col()
        if j == 0:
            plot_hsl(gr, draw, r, shift=shift,
                scale=scale)
        else:
            plot_hsl(gr, draw, r0, shift=shift,
                scale=scale)
    im.save("Images//RotatingCube//im" + str(i) + ".png")


# Now preparing the count the properties of the Tesseract.

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

def plot_all_faces2(tf, draw, r, kk1, persp=0, rgba=(10,31,190,80),
                    shift=np.array([514, 595, 0, 0]),scale=105):
    """
    The face colors here are consistent with
    230703 plot_colors method.
    """
    self = tf
    for kk in self.face_map.keys():
        if kk == kk1:
            col = (255,255,0,10)
        else:
            col = rgba
        ff = self.vert_props[kk]
        ff.plot_perspective(draw, r,
                                rgba=col,
                                e=persp,
                                c=-persp,
                                shift=shift,
                                scale=scale)


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


for i in range(8):
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    tf = tg.TsrctFcGraph(angle=0.0, adj=None)
    tf.draw = draw
    tf.r = rotation(4, np.pi*17/60.0*14/10.0)
    open_given_cube(tf, i=i)
    plot_all_faces(tf, tf.draw, tf.r, persp=5,shift=np.array([514, 595, 0, 0]),
            scale=105, rgba=(100,100,100,40))
    print(105-min(i,21)*2.7)
    im.save("Images//RotatingCube//im" +
                str(i).rjust(4, '0') + ".png")

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
    tf.r = rotation(4, np.pi*17/60.0*14/10.0)
    open_given_cube(tf, i=i)
    plot_all_faces2(tf, tf.draw, tf.r, kk, persp=5,shift=np.array([514, 595, 0, 0]),
            scale=105, rgba=(100,100,100,40))
    font = ImageFont.truetype("Arial.ttf", 14)
    draw.text((700,700), str(i), font=font)
    im.save("Images//RotatingCube//im" +
                str(i).rjust(4, '0') + ".png")


