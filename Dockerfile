FROM debian:latest as certificate_generator

USER root
RUN apt-get update && apt-get install -y openssl make

ADD Makefile /
RUN make certificates

FROM python:3-slim

ADD . /app
WORKDIR /app

COPY --from=certificate_generator certificate.pem /app
COPY --from=certificate_generator key.pem /app

RUN pip3 install -r requirements.txt

EXPOSE 8008
EXPOSE 8009

USER 1000
CMD [ "python3", "app.py", "--no-zeroconf" ]
