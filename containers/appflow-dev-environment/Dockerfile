FROM php:7-fpm-alpine

MAINTAINER  Luca Di Maio <luca.dimaio@ttss.ch>

LABEL Description="Testing" Vendor="TTSS AG" Version="1.0"

# install extensions needed for Laravel
RUN apk update 

# Install nginx
RUN apk add --update nginx=1.10.1-r1 && \
    rm -rf /var/cache/apk/* && \
    mkdir /run/nginx && \
    chown -R nginx:www-data /var/lib/nginx

# Add the files
#ADD root /

# Expose the ports for nginx
EXPOSE 80 443
