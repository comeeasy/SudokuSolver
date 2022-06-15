FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip
RUN apt install libjpeg8-dev zlib1g-dev
RUN pip install django
RUN pip install image
RUN pip install django-crispy-forms
RUN pip install django-markdownx
RUN pip install django opencv-python
RUN pip install django numpy
RUN pip install torch==1.8.1
RUN pip install torchvision==0.9.1
RUN pip install whitenoise
RUN pip install waitress


ENTRYPOINT ["waitress-serve", "--port=8080", "sudokusolver.wsgi:application"]
