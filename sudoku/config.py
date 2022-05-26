import logging

THRESHOLD = 0.9
SUDOKU_GRID = 100
SUDOKU_GRID_MARGIN = 30
SUDOKU_GRID_WIDTH = SUDOKU_GRID + SUDOKU_GRID_MARGIN

logging.info(f"""\
    THRESHOLD           : {THRESHOLD},
    SUDOKU_GRID         : {SUDOKU_GRID},
    SUDOKU_GRID_MARGIN  : {SUDOKU_GRID_MARGIN},
    SUDOKU_GRID_WIDTH   : {SUDOKU_GRID_WIDTH}
""")