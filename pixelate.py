#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
from PIL import Image
from DMC import DMC
from SVG import SVG
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert image to cross stitch pattern')
    parser.add_argument('image', help='Image to convert')
    parser.add_argument(
        '-c', '--colors', help='Number of colors for the chart (default: 10)', type=int, default=10)
    parser.add_argument(
        '-s', '--stitches', help='Number of stitches in X axis (default: 100)', type=int, default=100)
    parser.add_argument(
        '-o', '--output', help='Output directory for files (default: current directory)', type=str)
    return parser.parse_args()


def remove_transparency(im, bg_colour=(255, 255, 255)):
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        background = Image.new('RGB', im.size, (255, 255, 255))
        background.paste(im, mask=im.split()[3])
        return background
    else:
        return im


def resize_image(im, new_width=1000):
    new_height = int(new_width * im.size[1] / im.size[0])
    return im.resize((new_width, new_height), Image.NEAREST)


def get_dmc_image(im, d, args, new_width=1000):
    pixelSize = int(new_width / args.stitches)
    dmc_colors = [[d.get_dmc_rgb_triple(im.getpixel((x, y))) for x in range(
        0, im.size[0], pixelSize)] for y in range(0, im.size[1], pixelSize)]
    dmc_image = Image.new('RGB', (len(dmc_colors[0]), len(dmc_colors)))
    dmc_image.putdata([value for row in dmc_colors for value in row])
    return dmc_image.convert('P', palette=Image.ADAPTIVE, colors=args.colors)


def get_neighbours(pos, matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    width = 1
    for i in range(max(0, pos[0] - width), min(rows, pos[0] + width + 1)):
        for j in range(max(0, pos[1] - width), min(cols, pos[1] + width + 1)):
            if not (i == pos[0] and j == pos[1]):
                yield matrix[i][j]


def clean_svg_pattern(im, pattern):
    for x in range(0, im.size[0]):
        for y in range(0, im.size[1]):
            gen = get_neighbours([y, x], pattern)
            neighbours = []
            for n in gen:
                neighbours += [n]
            if pattern[y][x] not in neighbours:
                mode = max(neighbours, key=neighbours.count)
                pattern[y][x] = mode
    return pattern


def get_svg_data(im, d, args):
    svg_pattern = [
        [im.getpixel((x, y)) for x in range(im.size[0])] for y in range(im.size[1])
    ]
    palette = im.getpalette()
    svg_palette = [
        d.get_colour_code_corrected((palette[i * 3], palette[i * 3 + 1], palette[i * 3 + 2])) for i in range(args.colors)
    ]
    return (clean_svg_pattern(im, svg_pattern), svg_palette)


def prep_svg(im, pattern, palette, svg_cell_size=10, size=40):
    col_sym = SVG(False, True, True)
    blw_nsy = SVG(True, True, True)
    col_nsy = SVG(False, False, False)
    key = SVG(False, True, True)
    width = im.size[0] * svg_cell_size
    height = im.size[1] * svg_cell_size
    col_sym.prep_for_drawing(width, height)
    col_sym.mid_arrows(svg_cell_size, width, height)
    blw_nsy.prep_for_drawing(width, height)
    blw_nsy.mid_arrows(svg_cell_size, width, height)
    col_nsy.prep_for_drawing(width, height)
    x = y = svg_cell_size  # to allow drawing of midpoint arrows
    for row in pattern:
        for color_index in row:
            col_sym.add_rect(palette, color_index, x, y, svg_cell_size)
            blw_nsy.add_rect(palette, color_index, x, y, svg_cell_size)
            col_nsy.add_rect(palette, color_index, x, y, svg_cell_size)
            x += svg_cell_size
        y += svg_cell_size
        x = svg_cell_size
    blw_nsy.major_gridlines(svg_cell_size, width, height)
    col_sym.major_gridlines(svg_cell_size, width, height)
    key.prep_for_drawing(size * 13, size * len(palette))
    x = y = 0
    for i in range(len(palette)):
        key.add_key_colour(x, y, size, i, palette[i])
        y += size
    return (col_sym, blw_nsy, col_nsy, key)


def save_svg(im, pattern, palette, args):
    col_sym, blw_nsy, col_nsy, key = prep_svg(im, pattern, palette)
    base_filename = Path(args.image).stem
    if args.output:
        if not os.path.exists(args.output):
            os.makedirs(args.output)
        base_filename = os.path.join(args.output, base_filename)
    col_sym.save('%s_col_sym.svg' % base_filename)
    blw_nsy.save('%s_blw_sym.svg' % base_filename)
    col_nsy.save('%s_col_nsy.svg' % base_filename)
    key.save('%s_key.svg' % base_filename)


def main():
    args = parse_args()
    # open image
    im = Image.open(args.image)
    # remove alpha channel
    im = remove_transparency(im)
    # resize
    im = resize_image(im)
    # get image in DMC colors
    d = DMC()
    im = get_dmc_image(im, d, args)
    # get SVG pattern and palette
    pattern, palette = get_svg_data(im, d, args)
    # prep and save SVG
    save_svg(im, pattern, palette, args)


if __name__ == '__main__':
    main()
