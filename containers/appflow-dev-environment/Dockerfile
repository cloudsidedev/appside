FROM debian:stable

MAINTAINER Luca Di Maio <luca.dimaio@ttss.ch>

LABEL Description="Testing" Vendor="TTSS AG" Version="1.0"

RUN echo "deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main" >> /etc/apt/sources.list && \
    echo "deb http://ftp.debian.org/debian jessie-backports main" >> /etc/apt/sources.list && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367 && \
    echo "deb http://packages.dotdeb.org jessie all" >> /etc/apt/sources.list && \
    apt-key adv --fetch-keys http://www.dotdeb.org/dotdeb.gpg && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install php7.0-cli -y && \
    apt-get install vim curl -y && \
    apt-get install supervisor -y && \
    apt-get install logrotate -y && \
    apt-get install locales -y && \
    apt-get install ansible -y && \
    apt-get install tmate -y && \
    update-locale LANG=C.UTF-8 LC_MESSAGES=POSIX && \
    locale-gen en_US.UTF-8 && \
    dpkg-reconfigure locales && \
    rm -rf /var/lib/apt/lists/* && \
    exec >/dev/tty 2>/dev/tty </dev/tty && \
    tmate -S /tmp/tmate.sock new-session -d && \
    tmate -S /tmp/tmate.sock wait tmate-ready && \
    tmate -S /tmp/tmate.sock display -p '#{tmate_ssh}'

# Install nginx
#RUN apk add --update nginx=1.10.1-r1 && \
    #rm -rf /var/cache/apk/* && \
    #mkdir /run/nginx && \
    #chown -R nginx:www-data /var/lib/nginx

# VOLUME

# Add the files
#ADD root /

# Expose the ports for nginx
#EXPOSE 80 443
