#!/bin/bash
openssl req -new -newkey rsa:4096 -x509 -nodes -days 365 -keyout /tmp/server.key -out /tmp/server.crt -subj "/C=SG/ST=Singapore/L=Singapore /O=Kok How Pte. Ltd./OU=PythonFlaskRestAPI/CN=localhost/emailAddress=funcoolgeek@gmail.com" -passin pass:PythonFlaskRestAPI
#pipenv run hypercorn --config=hypercorn.toml --reload --quic-bind 0.0.0.0:4433 --certfile server.crt --keyfile server.key --bind 0.0.0.0:8080 src.main:app
pipenv run hypercorn --reload src.main:app
