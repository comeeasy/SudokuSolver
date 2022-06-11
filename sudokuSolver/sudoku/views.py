import cv2
import numpy as np
from django.shortcuts import render
from .libsudoku import sudoku
from .libsudoku.ai.model import ResNet34
from .libsudoku.ai.detector import Detector
from .libsudoku.drawer import Drawer

from PIL import Image


# Create your views here.
def solveByType(request):

    if request.method == "GET":
        return render(
            request,
            "sudoku/solve_by_type.html",
        )
    elif request.method == "POST":
        mat = []
        for k, v in request.POST.dict().items():
            if k.startswith('n'):
                if v == '':
                    mat.append(0)
                else:
                    mat.append(int(v))

        sdk_mat = []
        for i in range(9):
            _ = []
            for j in range(9):
                _.append(sudoku.loc(i, j, mat[9*i + j]))
            sdk_mat.append(_)

        sdk = sudoku.SudokuSolver(sdk_mat)
        result = sudoku.play_sdk(sdk)

        context = {f"n{i+1}{j+1}": result.matrix[i][j] for i in range(9) for j in range(9)}
        return render(
            request,
            "sudoku/solved_by_type.html",
            context
        )



model = ResNet34()
model.load(path="/Users/joono/Desktop/joono/SudokuSolver/sudokuSolver/sudoku/libsudoku/ai/weights/ResNet34-epoch58-acc99.65.pt", device='cpu')
detector = Detector(model)
drawer = Drawer()
def solveByPic(request):
    if request.method == "GET":
        return render(
            request,
            "sudoku/solve_by_picture.html",
        )
    elif request.method == "POST":
        print(request.POST)
        print(request.FILES['img'])

        img = Image.open(request.FILES['img'])
        cv_img = np.array(img)
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
        print(img)
        img.show()

        context = {
            "img": img
        }

        return render(
            request,
            "sudoku/solved_by_picture.html",
            context,
        )

def posts(request):
    return render(
        request,
        "sudoku/posts.html"
    )
