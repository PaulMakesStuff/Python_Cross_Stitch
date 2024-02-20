import os
from PIL import Image
from DMC import DMC
from SVG import SVG
from gooey import Gooey, GooeyParser

def get_neighbours(pos, matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    width = 1
    for i in range(max(0, pos[0] - width), min(rows, pos[0] + width + 1)):
        for j in range(max(0, pos[1] - width), min(cols, pos[1] + width + 1)):
            if not (i == pos[0] and j == pos[1]):
                yield matrix[i][j]

@Gooey
def main():
    
    # a. process options
    parser = GooeyParser(description="Cross Stich Pattern Generator")

    parser.add_argument("input_file_name", metavar="Input File Name, need to be a jpg!", widget="FileChooser")
    parser.add_argument("num_colours", metavar="Number of Colours", type=int, help="Number of colours to use in the pattern")
    parser.add_argument("count", metavar="Stitch Count", type=int, help="Stitch count, number of stitches in x axis")

    args = parser.parse_args()

    input_file_name = args.input_file_name
    num_colours = args.num_colours
    count = args.count

    col_sym = SVG(False, True, True)
    blw_nsy = SVG(True, True, True)
    col_nsy = SVG(False, False, False)
    key = SVG(False, True, True)

    # b. open image
    im = Image.open(input_file_name)

    # c. resize image
    new_width = 1000
    pixelSize = int(new_width / int(count))
    new_height = int(new_width * im.size[1] / im.size[0])
    im = im.resize((new_width, new_height), Image.NEAREST)


    # 1. take the spaced out pixels
    # 2. convert these pixels to dmc colours
    d = DMC()
    dmc_spaced = [[d.get_dmc_rgb_triple(im.getpixel((x, y))) for x in range(0, im.size[0], pixelSize)] for y in
                  range(0, im.size[1], pixelSize)]

    # 3. create a new smaller image with these pixels
    dmc_image = Image.new('RGB', (len(dmc_spaced[0]), len(dmc_spaced)))
    dmc_image.putdata([value for row in dmc_spaced for value in row])

    # 4. quantise the image with the required number of colours
    # 5. a new image can then be created with row x column of palette indices
    dmc_image = dmc_image.convert('P', palette=Image.ADAPTIVE, colors=num_colours)
    x_count = dmc_image.size[0]
    y_count = dmc_image.size[1]
    svg_pattern = [[dmc_image.getpixel((x, y)) for x in range(x_count)] for y in range(y_count)]

    # 6. a new palette can then be created with the dmc 'objects'
    palette = dmc_image.getpalette()
    svg_palette = [d.get_colour_code_corrected((palette[i * 3], palette[i * 3 + 1], palette[i * 3 + 2])) for i in
                   range(num_colours)]

    # 7. do any extra required cleaning up, for example removing isolated pixels
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

    # 8. svgs can be produced of black/white, colour with symbols, colour only patterns.
    svg_cell_size = 10
    width = x_count * svg_cell_size
    height = y_count * svg_cell_size
    col_sym.prep_for_drawing(width, height)
    col_sym.mid_arrows(svg_cell_size, width, height)
    blw_nsy.prep_for_drawing(width, height)
    blw_nsy.mid_arrows(svg_cell_size, width, height)
    col_nsy.prep_for_drawing(width, height)
    x = y = svg_cell_size  # to allow drawing of midpoint arrows
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

    # 9. generate the key table
    size = 40
    key.prep_for_drawing(size * 13, size * len(svg_palette))
    x = y = 0
    for i in range(len(svg_palette)):
        key.add_key_colour(x, y, size, i, svg_palette[i])
        y += size

    # 10. save images
    parent_dir = os.curdir
    patterns_path = os.path.join(parent_dir, "patterns")
    pattern_dir = os.path.join(patterns_path, os.path.splitext(os.path.basename(input_file_name))[0])

    if not os.path.exists(pattern_dir):
        os.makedirs(pattern_dir)

    col_sym.save(os.path.join(pattern_dir, 'cross_stitch_pattern.svg'))
    blw_nsy.save(os.path.join(pattern_dir, 'black_white_pattern.svg'))
    col_nsy.save(os.path.join(pattern_dir, 'pixelated_image.svg'))
    key.save(os.path.join(pattern_dir, 'colours.svg'))

if __name__ == "__main__":
    main()

