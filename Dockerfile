FROM python:3.8.12-slim-bullseye

MAINTAINER Mingyeong Yang, mingyeong@khu.ac.kr
LABEL org.opencontainers.image.source https://github.com/mmingyeong/FromSingleToStacked

COPY . fromsingletostacked

RUN apt-get -y update
RUN apt-get -y install build-essential libbz2-dev
