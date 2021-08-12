FROM python:3.8-slim-buster
RUN mkdir /site
COPY backend/requirements.txt /site
WORKDIR /site
RUN pip3 install -r requirements.txt

COPY . /site

CMD gunicorn wsgi:app -w 1 -b 0.0.0.0:80 --capture-output --log-level debug