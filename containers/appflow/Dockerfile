FROM debian:stable

LABEL Authors="Ivo Marino <ivo.marino@ttss.ch>, Luca Di Maio <luca.dimaio@ttss.ch>"
LABEL Description="AppFlow" Vendor="TTSS AG" Version="1.0"

ENV DEBIAN_FRONTEND=noninteractive

RUN useradd -ms /bin/bash appflow && \
    chown -R appflow:appflow /usr/local &&  \
    apt-get update && \
    apt-get install gnupg2 -y && \
    echo "deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main" >> /etc/apt/sources.list && \
    echo "deb http://ftp.debian.org/debian jessie-backports main" >> /etc/apt/sources.list && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367 && \
    echo "deb http://packages.dotdeb.org jessie all" >> /etc/apt/sources.list && \
    apt-key adv --fetch-keys http://www.dotdeb.org/dotdeb.gpg && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install git -y && \
    apt-get install make -y && \
    apt-get install apt-utils -y && \
    apt-get install php7.0-cli -y && \
    apt-get install curl -y && \
    apt-get install supervisor -y && \
    apt-get install logrotate -y && \
    apt-get install locales -y && \
    apt-get install golang-1.7-go -y && \
    apt-get install ansible -y && \
    update-locale LANG=C.UTF-8 LC_MESSAGES=POSIX && \
    locale-gen en_US.UTF-8 && \
    dpkg-reconfigure locales && \
    rm -rf /var/lib/apt/lists/* && \
    git clone https://github.com/ttssdev/appflow /opt/appflow && \
    ln -s /opt/appflow/appflow /usr/local/bin/appflow && \
    chown -R appflow:appflow /opt/appflow

WORKDIR /home/appflow
ENV HOME=/home/appflow
USER appflow

ENTRYPOINT ["appflow"]
