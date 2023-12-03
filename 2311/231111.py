import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageMath


im = Image.new("RGB", (512, 512), (0, 0, 0))
draw = ImageDraw.Draw(im, 'RGBA')
