import cv2
import numpy as np

from .config import SUDOKU_GRID_WIDTH


def extract_sudoku_image(path="images/sudoku2.jpeg"):
    img = cv2.imread(path)
    img_ori = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h, w = img.shape

    img = cv2.GaussianBlur(img, ksize=(15, 15), sigmaX=3, sigmaY=3)
    img = cv2.Canny(img, threshold1=0, threshold2=40)
    img = cv2.dilate(img, kernel=np.ones((5, 5)), iterations=2)

    # cv2.imshow("img", img)

    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    bound_rec_img = np.zeros_like(img_ori)
    selected_contours = list()
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < w * h / 3:
            continue

        selected_contours.append(cnt)

        x, y, w, h = cv2.boundingRect(cnt)
        bound_rec_list = [[x, y], [x, y + h], [x + w, y], [x + w, y + h]]
        cv2.rectangle(bound_rec_img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        epsilon = 0.02 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # Blue -> Green -> Red -> Yellow
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]

        approx = sorted(approx, key=lambda x: x[0][0])
        approx[:2] = sorted(approx[:2], key=lambda x: x[0][1])
        approx[2:] = sorted(approx[2:], key=lambda x: x[0][1])
        approx = np.array(approx)
        cv2.drawContours(bound_rec_img, approx, 0, (0, 255, 0), 5)

    # Perspective Transform
    M = cv2.getPerspectiveTransform(np.array(approx, dtype=np.float32), np.array(bound_rec_list, dtype=np.float32))
    inv_M = cv2.getPerspectiveTransform(np.array(bound_rec_list, dtype=np.float32), np.array(approx, dtype=np.float32))
    dst = cv2.warpPerspective(img_ori, M, (0, 0))

    # cv2.imshow("dst". dst)

    inv_info = {
        "xywh": (x, y, w, h),
        "img_transformed": dst,
        "inverse_mat": inv_M
    }

    sudoku = dst[y + 10:y + h - 10, x + 10:x + w - 10]
    sudoku = cv2.resize(sudoku, (SUDOKU_GRID_WIDTH * 9, SUDOKU_GRID_WIDTH * 9))

    # cv2.imshow("sudoku in function", sudoku)

    print(f"sudoku is extracted, shape of sudoku: {sudoku.shape}")

    return sudoku, inv_info


