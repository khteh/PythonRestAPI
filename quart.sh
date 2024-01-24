#!/bin/bash
openssl req -new -newkey rsa:4096 -x509 -nodes -days 365 -keyout server.key -out server.crt -subj "/C=SG/ST=Singapore/L=Singapore /O=Kok How Pte. Ltd./OU=PythonFlaskRestAPI/CN=localhost/emailAddress=funcoolgeek@gmail.com" -passin pass:PythonFlaskRestAPI
pipenv run hypercorn --reload --quic-bind localhost:4433 --certfile server.crt --keyfile server.key --bind 0.0.0.0:8080 src.main:app
