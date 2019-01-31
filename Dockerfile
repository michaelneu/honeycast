FROM debian:latest as certificate_generator

USER root
RUN apt-get update && apt-get install -y openssl make

ADD Makefile /
RUN make certificates

FROM python:3-slim

ADD . /app
WORKDIR /app

COPY --from=certificate_generator --chown=1000:1000 certificate.pem /app
COPY --from=certificate_generator --chown=1000:1000 key.pem /app

RUN pip3 install -r requirements.txt

EXPOSE 8008
EXPOSE 8009

RUN chown -R 1000:1000 .
USER 1000
RUN touch honeycast.log

CMD [ "bash", "entrypoint.sh" ]
