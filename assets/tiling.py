import random
from collections import defaultdict


def validate_colors(shapes, colors):
    """
    Return colors lists per tile

    Only used for testing generate_colors
    :return:
    """
    colors_count = defaultdict(list)
    for row_index, row in enumerate(shapes):
        for col_index, value in enumerate(row):
            colors_count[shapes[row_index][col_index]].append(colors[row_index][col_index])
    return colors_count

def generate_colors(shape):
    """
    Generates color maps for a given tiling
    """
    colors = {x: [1, 2, 3, 4, 5] for x in range(1, max(shape[-1])+1)}

    # Basic tiling
    cell_colors = [[0 for x in range(8)] for y in range(8)]
    for row_index, row in enumerate(shape):
        for col_index, value in enumerate(row):
            if value == 0:
                color = 0
            else:
                color = random.choice(colors[value])
                colors[value].remove(color)
                cell_colors[row_index][col_index] = color

    # Backside tiling, guaranteed to have 2 stones of same color in a row
    inverted_cell_colors = [row[::-1] for row in cell_colors]
    inverted_shapes = [row[::-1] for row in shape]
    tiles = defaultdict(list)
    for row_index, row in enumerate(inverted_shapes):
        for col_index, value in enumerate(row):
            if value:
                tiles[value].append((row_index, col_index))
    for tile in tiles:
        to_revert = random.choice(tiles[tile])
        neighbours = []
        for other in tiles[tile]:
            if abs(to_revert[0] - other[0]) + abs(to_revert[1] - other[1]) == 1:
                neighbours.append(other)
        neighbour = random.choice(neighbours)
        tmp = [inverted_cell_colors[x[0]][x[1]] for x in tiles[tile]]
        inverted_cell_colors[to_revert[0]][to_revert[1]] =\
            inverted_cell_colors[neighbour[0]][neighbour[1]]
    return cell_colors, inverted_cell_colors