FROM mcr.microsoft.com/azure-functions/python:4

USER root

RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && apt-get dist-upgrade -y

COPY requirements.txt /requirements.txt

EXPOSE 80

RUN pip3 install -r /requirements.txt