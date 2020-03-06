FROM python:3.8-slim-buster
RUN apt-get update && apt-get upgrade -y
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
CMD ['python3', 'run.py']
