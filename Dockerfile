FROM python:latest
MAINTAINER Kok How, Teh <funcoolgeek@gmail.com>
WORKDIR /app
ADD src src
ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
RUN openssl req -new -newkey rsa:4096 -x509 -nodes -days 365 -keyout server.key -out server.crt -subj "/C=SG/ST=Singapore/L=Singapore /O=Kok How Pte. Ltd./OU=PythonRestAPI/CN=localhost/emailAddress=funcoolgeek@gmail.com" -passin pass:PythonRestAPI
EXPOSE 8080 4433
ENTRYPOINT [ "hypercorn",  "--quic-bind", "0.0.0.0:4433", "--certfile", "server.crt", "--keyfile", "server.key", "--bind", "0.0.0.0:8080", "src.main:app" ]
