FROM python:3.10-buster 

ENV PYTHONUNBUFFERED=1

# Install necessary libraries including ffmpeg
RUN apt-get update -q && apt-get install -yq libpq-dev postgresql-client ffmpeg

WORKDIR /app 

COPY requirement.txt requirement.txt
RUN pip3 install -r requirement.txt

COPY . .
