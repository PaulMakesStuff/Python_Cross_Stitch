# algorithm
#
# a. process options
# b. open image
# c. resize image
#
# 1. take the spaced out pixels
# 2. convert these pixels to dmc colours
# 3. create a new smaller image with these pixels
# 4. quantise the image with the required number of colours
# 5. a new image can then be created with row x column of palette indices
# 6. a new palette can then be created with the dmc 'objects'
# 7. do any extra required cleaning up, for example removing isolated pixels
# 8. svgs can be produced of black/white, colour with symbols, colour only patterns.
# 9. generate the key table

import sys
from PIL import Image
from DMC import DMC
from SVG import SVG

def get_neighbours(pos, matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    width = 1
    for i in range(max(0, pos[0] - width), min(rows, pos[0] + width + 1)):
        for j in range(max(0, pos[1] - width), min(cols, pos[1] + width + 1)):
            if not (i == pos[0] and j == pos[1]):
                yield matrix[i][j]
    
# a

if(len(sys.argv)<3):
    print("function requires an input filename, number of colours, stitch count and mode")
    sys.exit(0)

input_file_name = sys.argv[1]       # input file name, has to be a jpg
num_colours = int(sys.argv[2])      # number of colours to use in the pattern
count = int(sys.argv[3])            # stitch count, number of stitches in x axis

# black_white, minor, symbols    
    
col_sym = SVG(False, True, True)
blw_nsy = SVG(True, True, True)
col_nsy = SVG(False, False, False)
key = SVG(False, True, True)

# b

im = Image.open(input_file_name)

# c

new_width  = 1000
pixelSize = int(new_width / int(count))
new_height = int(new_width * im.size[1] / im.size[0])
im = im.resize((new_width, new_height), Image.NEAREST)

# 1, 2

d = DMC()
dmc_spaced = [[d.get_dmc_rgb_triple(im.getpixel((x, y))) for x in range(0, im.size[0], pixelSize)] for y in range(0, im.size[1], pixelSize)]

# 3

dmc_image = Image.new('RGB', (len(dmc_spaced[0]), len(dmc_spaced))) #h, w
dmc_image.putdata([value for row in dmc_spaced for value in row])

# 4, 5

dmc_image = dmc_image.convert('P', palette=Image.ADAPTIVE, colors = num_colours)
x_count = dmc_image.size[0]
y_count = dmc_image.size[1]
svg_pattern = [[dmc_image.getpixel((x, y)) for x in range(x_count)] for y in range(y_count)]

# 6

palette = dmc_image.getpalette()
svg_palette = [d.get_colour_code_corrected((palette[i * 3], palette[i * 3 + 1], palette[i * 3 + 2])) for i in range(num_colours)]

# 7

if True:
    for x in range(0, x_count):
        for y in range(0, y_count):
            gen = get_neighbours([y, x], svg_pattern)
            neighbours = []
            for n in gen:
                neighbours += [n]
            if svg_pattern[y][x] not in neighbours:
                mode = max(neighbours, key=neighbours.count)
                svg_pattern[y][x] = mode

# 8

svg_cell_size = 10
width = x_count * svg_cell_size
height = y_count * svg_cell_size
col_sym.prep_for_drawing(width, height)
col_sym.mid_arrows(svg_cell_size, width, height)
blw_nsy.prep_for_drawing(width, height)
blw_nsy.mid_arrows(svg_cell_size, width, height)
col_nsy.prep_for_drawing(width, height)
x = y = svg_cell_size # to allow drawing of midpoint arrows
for row in svg_pattern:
    for colour_index in row:
        col_sym.add_rect(svg_palette, colour_index, x, y, svg_cell_size)
        blw_nsy.add_rect(svg_palette, colour_index, x, y, svg_cell_size)
        col_nsy.add_rect(svg_palette, colour_index, x, y, svg_cell_size)
        x += svg_cell_size
    y += svg_cell_size
    x = svg_cell_size
blw_nsy.major_gridlines(svg_cell_size, width, height)
col_sym.major_gridlines(svg_cell_size, width, height)

# 9

size = 40
key.prep_for_drawing(size * 13, size * len(svg_palette))
x = y = 0
for i in range(len(svg_palette)):
    key.add_key_colour(x, y, size, i, svg_palette[i])
    y += size

col_sym.save('col_sym.svg')
blw_nsy.save('blw_sym.svg')
col_nsy.save('col_nsy.svg')
key.save('key.svg')

