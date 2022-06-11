import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
import numpy as np
import cv2

from ..config import SUDOKU_GRID, SUDOKU_GRID_MARGIN, SUDOKU_GRID_WIDTH, THRESHOLD

class Detector:
    def __init__(self, model) -> None:
        self.model = model
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize((SUDOKU_GRID, SUDOKU_GRID))
        ])

    def get_sudoku_mat(self, sudoku_img):
        sudoku_img_gray = cv2.cvtColor(sudoku_img, cv2.COLOR_BGR2GRAY)

        # cv2.imshow("sudoku", sudoku_img_gray)
        # cv2.waitKey(0)

        sudoku_numbers = list()
        for y in range(9):
            sudoku_row = list()
            for x in range(9):
                # SUDOKU_GRID_WIDTH = SUDOKU_GRID + SUDOKU_GRID_MARGIN
                number_ori = sudoku_img_gray[SUDOKU_GRID_WIDTH*y+(SUDOKU_GRID_MARGIN//2) : SUDOKU_GRID_WIDTH*(y+1)-(SUDOKU_GRID_MARGIN//2),\
                                    SUDOKU_GRID_WIDTH*x+(SUDOKU_GRID_MARGIN//2) : SUDOKU_GRID_WIDTH*(x+1)-(SUDOKU_GRID_MARGIN//2)]
                number = np.reshape(number_ori, (SUDOKU_GRID, SUDOKU_GRID, 1))
                number_ori = number.copy()
                number = self.transform(number).unsqueeze_(0)

                # cv2.imshow("number", number_ori)
                # cv2.waitKey(10)

                # print(f"number shape: {number.shape}")
                with torch.no_grad():
                    predict = self.model(number)

                predict = F.softmax(predict)
                num = torch.argmax(predict, 1)

                confidence = predict[0][num]
                if confidence > THRESHOLD:
                    sudoku_row.append(num.item())
                    # print(f"{num.item()} num: {num}, conf: {predict[0][num]}")
                else:
                    # ask what this number is
                    cv2.imshow("number", number_ori)
                    num = int(input("What is this number?"))
                    sudoku_row.append(num)
                    print(f"{0} num: {num}, conf: {predict[0][num]}")


            sudoku_numbers.append(sudoku_row)
        
        return sudoku_numbers