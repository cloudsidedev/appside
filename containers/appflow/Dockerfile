FROM debian:stretch-slim

LABEL Authors="Ivo Marino <ivo.marino@ttss.ch>, Luca Di Maio <luca.dimaio@ttss.ch>"
LABEL Description="AppFlow" Vendor="TTSS AG" Version="1.0"

ENV DEBIAN_FRONTEND=noninteractive
ENV GOPATH=/usr/local/go

RUN useradd -ms /bin/bash appflow && \
    chown -R appflow:appflow /usr/local &&  \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install apt-utils -y && \
    apt-get install git -y && \
    apt-get install make -y && \
    apt-get install php7.0-cli -y && \
    apt-get install curl -y && \
    apt-get install locales -y && \
    apt-get install golang-1.8-go -y && \
    apt-get install golang-go -y && \
    apt-get install ansible -y && \
    update-locale LANG=C.UTF-8 LC_MESSAGES=POSIX && \
    locale-gen en_US.UTF-8 && \
    dpkg-reconfigure locales && \
    rm -rf /var/lib/apt/lists/* && \
    go get -u github.com/moul/advanced-ssh-config/cmd/assh && \
    git clone https://github.com/ttssdev/appflow /opt/appflow && \
    ln -s /opt/appflow/appflow /usr/local/bin/appflow && \
    chown -R appflow:appflow /opt/appflow

# export PATH=$PATH:/usr/local/go/bin

WORKDIR /home/appflow
ENV HOME=/home/appflow
USER appflow

ENTRYPOINT ["appflow"]
