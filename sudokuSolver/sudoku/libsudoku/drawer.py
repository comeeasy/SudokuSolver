import cv2
import numpy as np

from .config import SUDOKU_GRID, SUDOKU_GRID_MARGIN, SUDOKU_GRID_WIDTH


class Drawer:
    def __init__(self) -> None:
        self.number_names = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        self.number_imgs = [
            cv2.resize(
                cv2.imread(
                    f"/Users/joono/Desktop/joono/SudokuSolver/sudokuSolver/sudoku/libsudoku/images/numbers2/{number_name}.png",
                    cv2.IMREAD_UNCHANGED),
                (SUDOKU_GRID, SUDOKU_GRID))
            for number_name in self.number_names]

    def _get_drawed_sudoku(self, sudoku_mat, solved_sudoku_mat, sudoku_img):
        # draw result
        for y in range(9):
            for x in range(9):
                if sudoku_mat[y][x] == 0:
                    solution_number = solved_sudoku_mat[y][x]

                    sudoku_grid = sudoku_img[
                                  SUDOKU_GRID_WIDTH * y + (SUDOKU_GRID_MARGIN // 2): SUDOKU_GRID_WIDTH * (y + 1) - (
                                              SUDOKU_GRID_MARGIN // 2), \
                                  SUDOKU_GRID_WIDTH * x + (SUDOKU_GRID_MARGIN // 2): SUDOKU_GRID_WIDTH * (x + 1) - (
                                              SUDOKU_GRID_MARGIN // 2)]
                    number_img = self.number_imgs[solution_number - 1][..., :3]
                    alpha = np.uint8(self.number_imgs[solution_number - 1][..., 3] / 255)

                    for i in range(3):
                        number_img[..., i] = cv2.multiply(number_img[..., i], alpha)
                        sudoku_grid[..., i] = cv2.multiply(sudoku_grid[..., i], 1 - alpha)

                    sudoku_img[SUDOKU_GRID_WIDTH * y + (SUDOKU_GRID_MARGIN // 2): SUDOKU_GRID_WIDTH * (y + 1) - (
                                SUDOKU_GRID_MARGIN // 2), \
                    SUDOKU_GRID_WIDTH * x + (SUDOKU_GRID_MARGIN // 2): SUDOKU_GRID_WIDTH * (x + 1) - (
                                SUDOKU_GRID_MARGIN // 2)] \
                        = cv2.add(sudoku_grid, number_img)

        return sudoku_img

    def draw(self, sudoku_mat, solved_sudoku_mat, sudoku_img, inv_info):
        img_transformed = inv_info["img_transformed"]
        x, y, w, h = inv_info["xywh"]
        inv_M = inv_info["inverse_mat"]

        drawed_sudoku = self._get_drawed_sudoku(sudoku_mat, solved_sudoku_mat, sudoku_img)
        drawed_sudoku = cv2.resize(drawed_sudoku, (w, h))

        img_transformed[y:y + h, x:x + w] = drawed_sudoku
        dst = cv2.warpPerspective(img_transformed, inv_M, (0, 0))

        return dst