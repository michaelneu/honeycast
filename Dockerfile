FROM python:3-slim

ADD . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 8008
EXPOSE 8009

USER 1000
CMD [ "python3", "honeycast/__init__.py" ]
