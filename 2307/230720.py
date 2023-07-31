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


###########

for i in range(21):
    r = general_rotation(np.array([1,1,1]), np.pi/6)
    im = Image.new("RGB", (1024, 1024), (0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')
    gr = oc.GraphCube(survive_ros=incl_lst[4])
    #gr = oc.GraphCube(survive_ros={0, 1, 2, 3, 6})
    gr.angle = -np.pi*(20-i)/40.0
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
        if face_key == '0-0':
            shift = np.array([700,512-0*2,0])
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

