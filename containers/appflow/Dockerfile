FROM golang:1.8.3-stretch

LABEL Authors="Ivo Marino <ivo.marino@ttss.ch>, Luca Di Maio <luca.dimaio@ttss.ch>"
LABEL Description="AppFlow" Vendor="TTSS AG" Version="1.0"

ENV DEBIAN_FRONTEND=noninteractive
ENV GOPATH=/opt/go

# apt-get update && \
# apt-get install gnupg2 -y && \
# echo "deb http://ppa.launchpad.net/ansible/ansible/ubuntu xenial main" >> /etc/apt/sources.list && \
# echo "deb http://ftp.debian.org/debian jessie-backports main" >> /etc/apt/sources.list && \
# apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367 && \
# echo "deb http://packages.dotdeb.org jessie all" >> /etc/apt/sources.list && \
# apt-key adv --fetch-keys http://www.dotdeb.org/dotdeb.gpg && \
# go get -u github.com/moul/advanced-ssh-config/cmd/assh && \
# apt-get install golang-go -y && \

# 1  go get -u github.com/moul/advanced-ssh-config/cmd/assh
#  2  unset GOPATH
#  3  go get -u github.com/moul/advanced-ssh-config/cmd/assh
#  4  ssh-add -L
#  5  export PATH=$PATH:~/go/bin
#  6  assh
#  7  assh config list
#  8  assh -v -v vm-01.stage.viu.ch
#  9  ssh -v -v vm-01.stage.viu.ch
# 10  mkdir -p ~/tmp/.ssh/cm
# 11  assh -v -v vm-01.stage.viu.ch
# 12  ssh -v -v vm-01.stage.viu.ch
# 13  alias ssh="assh wrapper ssh"
# 14  ssh -v -v vm-01.stage.viu.ch
# 15  ls /usr/local/bin/assh
# 16  touch /usr/local/bin/assh
# 17  rm /usr/local/bin/assh
# 18  ln -s go/bin/assh /usr/local/bin/assh
# 19  ssh -v -v vm-01.stage.viu.ch
# 20  /usr/local/bin/assh
# 21  /usr/local/bin/
# 22  ssh -v -v vm-01.stage.viu.ch
# 23  ls go/
# 24  history

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
    git clone https://github.com/ttssdev/appflow /opt/appflow && \
    ln -s /opt/appflow/appflow /usr/local/bin/appflow && \
    chown -R appflow:appflow /opt/appflow

# export PATH=$PATH:/usr/local/go/bin

WORKDIR /home/appflow
ENV HOME=/home/appflow
USER appflow

ENTRYPOINT ["appflow"]
