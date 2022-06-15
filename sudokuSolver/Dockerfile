FROM python:3.7

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip
RUN pip install django
RUN pip install pillow
RUN pip install django-crispy-forms
RUN pip install django-markdownx
RUN pip install django opencv-python
RUN pip install django numpy
RUN pip install torch
RUN pip install torchvision
RUN pip install whitenoise
RUN pip install waitress


ENTRYPOINT ["waitress-serve", "--port=8080", "sudokusolver.wsgi:application"]
