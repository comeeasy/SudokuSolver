from io import BytesIO

import PIL
import cv2
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, ListView

from .libsudoku import sudoku
from .libsudoku.ai.detector import Detector
from .libsudoku.ai.model import ResNet34
from .libsudoku.drawer import Drawer
from .libsudoku.ocr import extract_sudoku_image
from .libsudoku.sudoku import SudokuSolver, loc, play_sdk
from .models import Image


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
def solveByPic(request, pk):
    img = Image.objects.get(pk=pk)

    pil = PIL.Image.open(img.sudoku_image)
    # pil.show()

    sudoku_img, inv_info = extract_sudoku_image(path=img.sudoku_image.path)
    sudoku_mat = detector.get_sudoku_mat(sudoku_img)

    for row in sudoku_mat:
        print(row)

    sudokuSolver = SudokuSolver([])
    for row in range(9):
        ithRow = sudoku_mat[row]
        # 스도쿠에 loc들을 삽입
        sudokuSolver.matrix.append([loc(row, column, ithRow[column]) for column in range(9)])
    solved_sudoku = play_sdk(sudokuSolver)
    solved_sudoku_mat = solved_sudoku.get_mat()

    drawer = Drawer()
    dst = drawer.draw(sudoku_mat, solved_sudoku_mat, sudoku_img, inv_info)
    dst = cv2.cvtColor(dst, cv2.COLOR_RGB2BGR)

    pil = PIL.Image.fromarray(dst)

    pil_io = BytesIO()
    pil.save(fp=pil_io, format='JPEG')
    new_pil = ContentFile(pil_io.getvalue())
    img.sudoku_image_result.save(name=f"result_{pk}.jpeg", content=new_pil)

    context = {
        "img": img,
    }

    return render(
        request,
        "sudoku/solved_by_picture.html",
        context
    )



class solveByPicCBV(CreateView):
    model = Image

    fields = ['sudoku_image']

    def get_success_url(self):
        return reverse("img_uploaded", kwargs={'pk': self.object.pk})

class PostListView(ListView):
    model = Image




