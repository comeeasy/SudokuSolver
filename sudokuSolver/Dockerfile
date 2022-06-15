FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["waitress-serve", "--port=8080", "sudokusolver.wsgi:application"]
