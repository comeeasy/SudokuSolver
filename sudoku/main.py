import cv2

from ai.model import EfficientNet
from ai.detector import Detector
from sudoku.sudoku import SudokuSolver, loc, play_sdk
from drawer import Drawer
from ocr import extract_sudoku_image


if __name__ == "__main__":
    model = EfficientNet()
    model.load(path="ai/weights/EfficientNet-epoch29-acc0.99.pt", device="cpu")
    sudoku_img, inv_info = extract_sudoku_image(path="images/sudoku2.jpeg")

    detector = Detector(model)
    sudoku_mat = detector.get_sudoku_mat(sudoku_img)

    sudokuSolver = SudokuSolver([])
    for row in range(9) :
        ithRow = sudoku_mat[row]
        # 스도쿠에 loc들을 삽입
        sudokuSolver.matrix.append([loc(row, column, ithRow[column]) for column in range(9)])
    solved_sudoku = play_sdk(sudokuSolver)
    solved_sudoku_mat = solved_sudoku.get_mat()
    
    drawer = Drawer()
    dst = drawer.draw(sudoku_mat, solved_sudoku_mat, sudoku_img, inv_info)

    cv2.imshow("result", dst)

    while True:
        k = cv2.waitKey(10)
        if 27 == k:
            break