FROM python:3.11
ENV PYTHONUNBUFFERED=1
RUN apt update
RUN apt-get install python3-pip -y
RUN pip3 install Pillow
WORKDIR /app