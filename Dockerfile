FROM python:3.5-slim
MAINTAINER Kevin Tarvin <ktarvin@motionpoint.com>

ENV INSTALL_PATH /mpscanner
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN pip install --editable .

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "mpscanner.app:create_app()"
