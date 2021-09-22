FROM python:latest
MAINTAINER Kok How, Teh <funcoolgeek@gmail.com>
WORKDIR /app
ADD cert.pem cert.pem
ADD ca-bundle.crt ca-bundle.crt
ADD src src
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080 4433
ENTRYPOINT [ "hypercorn",  "--quic-bind", "0.0.0.0:4433", "--certfile", "cert.pem", "--keyfile", "key.pem", "--bind", "0.0.0.0:8080", "src.main:app" ]
