#! /usr/bin/env python3
from tiling import generate_colors, validate_colors
from draw_block import draw_block

from svglib.svglib import svg2rlg
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4


################################################################################
#
# Constants and config
#
################################################################################

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

# TODO: invert shapes[0] and shapes[3]
field = [[6, 6, 6, 6, 6, 6, 6, 6, 6],
         [6, 6, 6, 0, 0, 0, 6, 6, 6],
         [6, 6, 0, 0, 0, 0, 0, 6, 6],
         [6, 0, 0, 0, 0, 0, 0, 0, 6],
         [6, 0, 0, 0, 6, 0, 0, 0, 6],
         [6, 0, 0, 0, 6, 0, 0, 0, 6],
         [6, 0, 0, 0, 6, 0, 0, 0, 6],
         [6, 0, 0, 0, 6, 0, 0, 0, 6],
         [6, 0, 0, 0, 0, 0, 0, 0, 6],
         [6, 6, 0, 0, 0, 0, 0, 6, 6],
         [6, 6, 6, 0, 0, 0, 6, 6, 6],
         [6, 6, 6, 6, 6, 6, 6, 6, 6]]


field2 = [[6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
          [6, 6, 6, 0, 0, 0, 0, 0, 6, 6],
          [6, 6, 0, 0, 0, 0, 0, 0, 0, 6],
          [6, 6, 0, 0, 0, 0, 0, 0, 0, 6],
          [6, 0, 0, 0, 0, 0, 0, 0, 0, 6],
          [6, 0, 0, 0, 6, 6, 6, 6, 0, 6],
          [6, 0, 0, 6, 6, 6, 6, 6, 6, 6],
          [6, 0, 0, 6, 6, 6, 6, 6, 6, 6],
          [6, 0, 0, 0, 6, 6, 6, 6, 0, 6],
          [6, 0, 0, 0, 0, 0, 0, 0, 0, 6],
          [6, 6, 0, 0, 0, 0, 0, 0, 0, 6],
          [6, 6, 0, 0, 0, 0, 0, 0, 0, 6],
          [6, 6, 6, 0, 0, 0, 0, 0, 6, 6],
          [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]]

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
#
#
################################################################################

tilings = []
inverted_shapes = []


asset_page = canvas.Canvas('test_out.pdf', bottomup=0,
                           pagesize=A4)
page_width, page_height = A4
asset_page.setLineWidth(0.1 * cm)
table_offset = (page_width / cm - 16) / 2

for shape in shapes:
    tiling, inverted_tiling = generate_colors(shape)
    inverted_shape = [row[::-1] for row in shape]
    draw_block(asset_page, shape, tiling,
               white_assets,
               start_x=table_offset,
               start_y=3,
               tile_size=2)
    asset_page.showPage()
    asset_page.setLineWidth(0.1 * cm)
    draw_block(asset_page, inverted_shape, inverted_tiling,
               bg_assets,
               start_x=table_offset,
               start_y=3,
               tile_size=2)
    asset_page.showPage()

# TODO: move fields to a separate document
draw_block(asset_page, field, field, white_assets,
           start_x=(page_width / cm - 2 * len(field[0])) / 2,
           start_y=(page_height / cm - 2 * len(field)) / 2,
           tile_size=2)
asset_page.showPage()
draw_block(asset_page, field2, field2, white_assets,
           start_x=(page_width / cm - 2 * len(field2[0])) / 2,
           start_y=(page_height / cm - 2 * len(field2)) / 2,
           tile_size=2)
asset_page.save()
