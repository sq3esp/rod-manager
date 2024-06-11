# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir /certs
RUN cp requirements.txt /certs/requirements.txt

# copy project
COPY . .

#RUN mkdir /certs
#RUN cd /certs
#RUN openssl req -subj "/C=CA/ST=QC/O=Company Inc/CN=localhost" -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
