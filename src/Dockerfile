FROM python:latest
MAINTAINER Kok How, Teh <funcoolgeek@gmail.com>
WORKDIR /app
ADD . .
RUN pip install -r requirements.txt
EXPOSE 80 443
ENTRYPOINT ["python"]
CMD ["main.py"]