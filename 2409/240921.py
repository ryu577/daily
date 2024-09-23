import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath
from pyray.rotation import general_rotation, planar_rotation
import pyray.grid as grd


im = Image.new("RGB", (1024, 1024), (1, 1, 1))
draw = ImageDraw.Draw(im, "RGBA")
n = 6
scl = 64
org = np.array([256, 512])
end1 = np.array([n, n])
gg = grd.Grid(end=end1,
              center=np.array([0, 0]),
              origin=org,
              rot=planar_rotation(0),
              scale=scl)
gg.draw(draw, width=3)


def drw(i, j, draw, txt=None):
    x_crd = org[0]+i*scl+scl/2
    y_crd = org[1]-scl*n+j*scl+scl/2
    if txt is None:
        draw.text((x_crd, y_crd), "(" + str(i) + "," + str(j) + ")")
    else:
        draw.text((x_crd, y_crd), txt)


# for i in range(n):
#     for j in range(n):
#         drw(i, j, draw)

def matr_chain_order(p, draw):
    n = len(p) - 1
    m = np.zeros(shape=((n+1), (n+1)))
    s = np.zeros(shape=((n+1), (n+1)))
    for l1 in range(2, n+1):
        for i in range(1, n-l1+1+1):
            j = i + l1 - 1
            m[i, j] = np.inf
            for k in range(i, j):
                q = m[i, k] + m[k+1, j] + p[i-1]*p[k]*p[j]
                if q < m[i, j]:
                    m[i, j] = q
                    s[i, j] = k
            drw(i, j, draw, str(m[i, j]))
    return m, s


def print_opt_paren(s, i, j):
    if i == j:
        print("A"+str(i)+".", end='')
    else:
        print("(", end='')
        print_opt_paren(s, i, int(s[i][j]))
        print_opt_paren(s, int(s[i][j]+1), j)
        print(")", end='')


p = [30, 35, 15, 5, 10, 20, 25]
mm, ss = matr_chain_order(p, draw)

im.save(".//" + "im" + str(0) + ".png")


ss = ss.astype(int)
print(mm)
print(ss)
print_opt_paren(ss, 1, 6)
