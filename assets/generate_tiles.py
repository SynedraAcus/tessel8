#! /usr/bin/env python3
from tiling import generate_colors, validate_colors
from draw_block import draw_block

from svglib.svglib import svg2rlg
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

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

field = [[6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
         [6, 6, 6, 0, 0, 0, 0, 0, 0, 6, 6, 6],
         [6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6],
         [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6],
         [6, 0, 0, 0, 6, 6, 6, 6, 0, 0, 0, 6],
         [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6],
         [6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6],
         [6, 6, 6, 0, 0, 0, 0, 0, 0, 6, 6, 6],
         [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
         ]

field2 = [[6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
          [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6],
          [6, 0, 0, 0, 0, 6, 6, 0, 0, 0, 0, 6],
          [6, 0, 0, 0, 0, 6, 6, 0, 0, 0, 0, 6],
          [6, 0, 0, 0, 0, 6, 6, 0, 0, 0, 0, 6],
          [6, 0, 0, 0, 0, 6, 6, 0, 0, 0, 0, 6],
          [6, 0, 0, 0, 0, 6, 6, 0, 0, 0, 0, 6],
          [6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6],
          [6, 6, 6, 0, 0, 0, 0, 0, 0, 6, 6, 6],
          [6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6],
          [6, 0, 0, 0, 0, 6, 6, 0, 0, 0, 0, 6],
          [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]]
tilings = []
inverted_shapes = []


page_width = 21 #  A4 width in cm
asset_page = canvas.Canvas('test_out.pdf', bottomup=0)
asset_page.setLineWidth(0.1 * cm)

starts = [(1, 1), (10, 1), (1, 10), (10, 10)]
inverted_starts = [(12, 1), (3, 1), (12, 10), (3, 10)]

for shape in shapes:
    tilings.append(generate_colors(shape))
    inverted_shapes.append([row[::-1] for row in shape])

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

for shape_index, shape in enumerate(shapes):
    draw_block(asset_page, shape, tilings[shape_index][0],
               white_assets,
               start_x=starts[shape_index][0],
               start_y=starts[shape_index][1])
asset_page.showPage()
asset_page.setLineWidth(0.1 * cm)

for shape_index, shape in enumerate(inverted_shapes):
    draw_block(asset_page, shape, tilings[shape_index][1],
               bg_assets,
               start_x=inverted_starts[shape_index][0],
               start_y=inverted_starts[shape_index][1])
asset_page.showPage()
asset_page.setLineWidth(0.1 * cm)
draw_block(asset_page, field, field, white_assets,
           start_x=5,
           start_y=3)
draw_block(asset_page, field2, field2, white_assets,
           start_x=5,
           start_y=14)
asset_page.save()

quit()
