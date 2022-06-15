FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY . .

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install django
RUN python3 -m pip install pillow
RUN python3 -m pip install django-crispy-forms
RUN python3 -m pip install django-markdownx
RUN python3 -m pip install django opencv-python
RUN python3 -m pip install django numpy
RUN python3 -m pip install torch==1.8.1
RUN python3 -m pip install torchvision==0.9.1
RUN python3 -m pip install whitenoise
RUN python3 -m pip install waitress


ENTRYPOINT ["waitress-serve", "--port=8080", "sudokusolver.wsgi:application"]
