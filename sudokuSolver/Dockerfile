FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY . .

RUN pip3 install django
RUN pip3 install django-crispy-forms
RUN pip3 install django-markdownx
RUN pip3 install django opencv-python
RUN pip3 install django numpy
RUN pip3 install Pillow
RUN pip3 install torch==1.8.1
RUN pip3 install torchvision==0.9.1
RUN pip3 install whitenoise
RUN pip3 install waitress


ENTRYPOINT ["waitress-serve", "--port=8080", "sudokusolver.wsgi:application"]
