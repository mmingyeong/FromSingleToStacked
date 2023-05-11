FROM ubuntu:latest

MAINTAINER Mingyeong Yang, mingyeong@khu.ac.kr
LABEL org.opencontainers.image.source https://github.com/mmingyeong/FromSingleToStacked

COPY . fromsingletostacked

RUN echo "Acquire::Check-Valid-Until \"false\";\nAcquire::Check-Date \"false\";" | cat > /etc/apt/apt.conf.d/10no--check-valid-until
RUN apt-get -y update
RUN apt-get upgrade -y 

