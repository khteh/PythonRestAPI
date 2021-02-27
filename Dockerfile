FROM python:latest
MAINTAINER Kok How, Teh <funcoolgeek@gmail.com>
WORKDIR /app
ADD src src
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 80 443
ENTRYPOINT ["python", "-m"]
CMD ["src.main"]