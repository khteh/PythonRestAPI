#FROM python:latest
FROM khteh/ubuntu:latest
MAINTAINER Kok How, Teh <funcoolgeek@gmail.com>
WORKDIR /app
RUN apt update -y --fix-missing
RUN apt upgrade -y
ADD src src
ADD Pipfile .
ADD Pipfile.lock .
ADD pyproject.toml .
ADD poetry.lock .
#RUN pip install pipenv
RUN pipenv install
#RUN python3 -m venv .venv
#RUN pipenv install --system --deploy --ignore-pipfile
#RUN .venv/bin/pip3 install -p Pipfile
#RUN poetry config virtualenvs.create false
#RUN poetry install --no-interaction --no-ansi
RUN openssl req -new -newkey rsa:4096 -x509 -nodes -days 365 -keyout /tmp/server.key -out /tmp/server.crt -subj "/C=SG/ST=Singapore/L=Singapore /O=Kok How Pte. Ltd./OU=PythonRestAPI/CN=localhost/emailAddress=funcoolgeek@gmail.com" -passin pass:PythonRestAPI
EXPOSE 80 443
ENTRYPOINT ["hypercorn", "--config=/etc/hypercorn.toml", "--reload", "src.main:app"]
