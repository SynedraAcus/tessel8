#! /usr/bin/env python3
from tiling import generate_colors, validate_colors
from draw_block import draw_block

from argparse import ArgumentParser
from svglib.svglib import svg2rlg
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4


################################################################################
#
# Constants and config
#
################################################################################

parser = ArgumentParser('Generate game files')
parser.add_argument('--notiles', action='store_true',
                    help='Do not regenerate tiles.pdf')
parser.add_argument('--nofield', action='store_true',
                    help='Do not regenerate fields.pdf')
args = parser.parse_args()

shapes = [
    [  # Zs, also to be used for generating Ss by reverting rows
        [ 1,  1,  2,  2,  3,  3,  0, 0],
        [ 0,  1,  1,  2,  2,  3,  3, 0],
        [ 4,  4,  5,  5,  6,  6,  0, 0],
        [ 0,  4,  4,  5,  5,  6,  6, 0],
        [ 7,  7,  8,  8,  9,  9,  0, 0],
        [ 0,  7,  7,  8,  8,  9,  9, 0],
        [10, 10, 11, 11, 12, 12,  0, 0],
        [0,  10, 10, 11, 11, 12, 12, 0]
    ],
    [  # Is and Os
        [ 1,  1,  1,  1,  2,  2,  2,  2],
        [ 3,  3,  3,  3,  4,  4,  4,  4],
        [ 5,  5,  5,  5,  6,  6,  6,  6],
        [ 7,  7,  7,  7,  8,  8,  8,  8],
        [ 9,  9, 10, 10, 11, 11, 12, 12],
        [ 9,  9, 10, 10, 11, 11, 12, 12],
        [13, 13, 14, 14, 15, 15, 16, 16],
        [13, 13, 14, 14, 15, 15, 16, 16]
    ],
    [  # Ts
        [ 1,  1,  1,  2,  3,  3,  3,  4],
        [ 5,  1,  2,  2,  2,  3,  4,  4],
        [ 5,  5,  6,  7,  7,  7,  8,  4],
        [ 5,  9,  6,  6,  7,  8,  8,  8],
        [ 9,  9,  6,  0, 10, 11, 11, 11],
        [12,  9,  0, 10, 10, 10, 11, 15],
        [12, 12, 13, 14, 14, 14, 15, 15],
        [12, 13, 13, 13, 14,  0,  0, 15]
    ],
    [  # Js, invertable to Ls
        [ 1,  1,  2,  2,  3,  3,  4,  4],
        [ 1,  5,  2,  6,  3,  7,  4,  8],
        [ 1,  5,  2,  6,  3,  7,  4,  8],
        [ 5,  5,  6,  6,  7,  7,  8,  8],
        [ 9,  9, 10, 10, 11, 11, 12, 12],
        [ 9, 13, 10, 14, 11, 15, 12, 16],
        [ 9, 13, 10, 14, 11, 15, 12, 16],
        [13, 13, 14, 14, 15, 15, 16, 16]
    ]
    ]

#  Zs from Ss, Js from Ls
shapes.append([row[::-1] for row in shapes[0]])
shapes.append([row[::-1] for row in shapes[3]])



fields = [
          [[6, 6, 6, 6, 6, 6, 6],  # field (6), best so far
           [6, 6, 6, 0, 6, 6, 6],
           [6, 6, 0, 0, 0, 6, 6],
           [6, 0, 0, 0, 0, 0, 6],
           [6, 0, 0, 0, 0, 0, 6],
           [6, 0, 0, 0, 0, 0, 6],
           [6, 0, 0, 0, 0, 0, 6],
           [6, 6, 0, 0, 0, 6, 6],
           [6, 6, 6, 0, 6, 6, 6],
           [6, 6, 6, 6, 6, 6, 6]],

          [[6, 6, 6, 6, 6, 6, 6],  # Field (7)
           [6, 0, 6, 6, 6, 0, 6],
           [6, 0, 0, 0, 0, 0, 6],
           [6, 0, 0, 0, 0, 0, 6],
           [6, 0, 0, 0, 0, 0, 6],
           [6, 0, 0, 0, 0, 0, 6],
           [6, 0, 0, 0, 0, 0, 6],
           [6, 0, 0, 0, 0, 0, 6],
           [6, 0, 6, 6, 6, 0, 6],
           [6, 6, 6, 6, 6, 6, 6]],

          [[6, 6, 6, 6, 6, 6, 6],  # Field (8)
           [6, 6, 6, 6, 6, 0, 6],
           [6, 6, 6, 0, 0, 0, 6],
           [6, 0, 0, 0, 0, 0, 6],
           [6, 0, 0, 0, 0, 0, 6],
           [6, 0, 0, 0, 0, 0, 6],
           [6, 0, 0, 0, 0, 0, 6],
           [6, 0, 0, 0, 6, 6, 6],
           [6, 0, 6, 6, 6, 6, 6],
           [6, 6, 6, 6, 6, 6, 6]],

          [[6, 6, 6, 6, 6, 6, 6],  # Field (9)
           [6, 6, 6, 6, 6, 0, 6],
           [6, 6, 6, 0, 0, 0, 6],
           [6, 0, 0, 0, 0, 0, 6],
           [6, 0, 0, 0, 0, 0, 6],
           [6, 0, 0, 0, 0, 0, 6],
           [6, 0, 0, 0, 0, 0, 6],
           [6, 6, 6, 0, 0, 0, 6],
           [6, 6, 6, 6, 6, 0, 6],
           [6, 6, 6, 6, 6, 6, 6]],

        ]

white_assets = {0: svg2rlg('Field_bg.svg'),
                1: svg2rlg('1_white.svg'),
                2: svg2rlg('2_white.svg'),
                3: svg2rlg('3_white.svg'),
                4: svg2rlg('4_white.svg'),
                5: svg2rlg('5_white.svg'),
                6: svg2rlg('Closed_bg.svg')}
bg_assets = {0: svg2rlg('Field_bg.svg'),
             1: svg2rlg('1_bg.svg'),
             2: svg2rlg('2_bg.svg'),
             3: svg2rlg('3_bg.svg'),
             4: svg2rlg('4_bg.svg'),
             5: svg2rlg('5_bg.svg')}

################################################################################
#
# Actual generation: tiles, then fields
#
################################################################################

tilings = []
inverted_shapes = []
page_width, page_height = A4

if not args.notiles:
    tile_document = canvas.Canvas('tiles.pdf', bottomup=0,
                                  pagesize=A4)
    tile_document.setLineWidth(0.1 * cm)
    table_offset = (page_width / cm - 16) / 2
    for shape in shapes:
        tiling, inverted_tiling = generate_colors(shape)
        inverted_shape = [row[::-1] for row in shape]
        draw_block(tile_document, shape, tiling,
                   white_assets,
                   start_x=table_offset,
                   start_y=3,
                   tile_size=2)
        tile_document.showPage()
        tile_document.setLineWidth(0.1 * cm)
        draw_block(tile_document, inverted_shape, inverted_tiling,
                   bg_assets,
                   start_x=table_offset,
                   start_y=3,
                   tile_size=2)
        tile_document.showPage()
    tile_document.save()

if not args.nofield:
    field_document = canvas.Canvas('fields.pdf', bottomup=0,
                                   pagesize=A4)
    for field in fields:
        draw_block(field_document, field, field, white_assets,
                   start_x=(page_width / cm - 2 * len(field[0])) / 2,
                   start_y=(page_height / cm - 2 * len(field)) / 2,
                   tile_size=2)
        field_document.showPage()
    field_document.save()
