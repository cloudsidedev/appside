FROM golang:1.8.3-stretch

LABEL Authors="Ivo Marino <ivo.marino@ttss.ch>, Luca Di Maio <luca.dimaio@ttss.ch>"
LABEL Description="AppFlow" Vendor="TTSS AG" Version="1.0"

ENV DEBIAN_FRONTEND=noninteractive
ENV GOPATH=/opt/go

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
    apt-get install ansible -y && \
    update-locale LANG=C.UTF-8 LC_MESSAGES=POSIX && \
    locale-gen en_US.UTF-8 && \
    dpkg-reconfigure locales && \
    rm -rf /var/lib/apt/lists/* && \
    go get -u github.com/moul/advanced-ssh-config/cmd/assh && \
    ln -s /opt/go/bin/assh /usr/local/bin/assh && \
    git clone https://github.com/ttssdev/appflow /opt/appflow && \
    ln -s /opt/appflow/appflow /usr/local/bin/appflow && \
    chown -R appflow:appflow /opt/appflow && \
    mkdir -p /home/appflow/tmp/.ssh/cm && \
    chown -R appflow:appflow /home/appflow/tmp && \
    echo 'alias ssh="assh wrapper ssh"' >> /home/appflow/.bashrc

WORKDIR /home/appflow
ENV HOME=/home/appflow
ENV PATH=$PATH:/opt/go/bin
USER appflow

ENTRYPOINT ["appflow"]
