from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.lib.units import cm


def draw_block(canvas: canvas,
               shape: list,
               tiling: list,
               assets: dict,
               start_x=2, start_y=2, tile_size=1):
    print(shape, tiling)
    for row_index, row in enumerate(tiling):
        for col_index, value in enumerate(row):
            renderPDF.draw(assets[value],
                           canvas,
                           start_x * cm + col_index * tile_size * cm,
                           start_y * cm + row_index * tile_size * cm)
            if col_index < 7 and shape[row_index][col_index] != shape[row_index][col_index+1]:
                # Line to the right of current block
                canvas.line(start_x * cm + (col_index + 1) * tile_size * cm,
                            start_y * cm + row_index * tile_size * cm,
                            start_x * cm + (col_index + 1) * tile_size * cm,
                            start_y * cm + (row_index + 1) * tile_size * cm,
                            )
            if row_index < 7 and shape[row_index][col_index] != shape[row_index+1][col_index]:
                # Line to the bottom of current block
                canvas.line(start_x * cm + col_index * tile_size * cm,
                            start_y * cm + (row_index + 1) * tile_size * cm,
                            start_x * cm + (col_index + 1) * tile_size * cm,
                            start_y * cm + (row_index + 1) * tile_size * cm)