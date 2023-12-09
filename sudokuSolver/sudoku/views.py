import os
from io import BytesIO

import PIL.Image
import cv2
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

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
model.load(path=os.path.join(settings.STATIC_ROOT, 'weights', 'ResNet34-epoch58-acc99.65.pt'), device='cpu')
detector = Detector(model)
drawer = Drawer()
def solveByPic(request, pk):
    print(request)

    img = Image.objects.get(pk=pk)

    print(request.POST)

    pil = PIL.Image.open(img.sudoku_image)

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
    img.user = request.user
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

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("img_uploaded", kwargs={'pk': self.object.pk})

    # def post(self, request, *args, **kwargs):
    #     print(request.POST)
    #     print(args, kwargs)
    #     return HttpResponse("Hello")


from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

class PostListView(LoginRequiredMixin, ListView):
    model = Image
    login_url = 'frontpage/login/'  # 로그인 페이지 URL 설정
    redirect_field_name = 'redirect_to'

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def handle_no_permission(self):
        return render(self.request, 'frontpage/login.html', {'form': AuthenticationForm})






