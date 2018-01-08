FROM frolvlad/alpine-glibc:alpine-3.6

LABEL Authors="Ivo Marino <ivo.marino@ttss.ch>, Luca Di Maio <luca.dimaio@ttss.ch>"
LABEL Description="AppFlow" Vendor="TTSS AG" Version="1.0"

# Install my Utils
#RUN apk upgrade --no-cache && \
#    apk add --no-cache git make bash openssh-client ansible diffutils
# 9mb bash
# 2mb openssh-client
# <1mb make
# 88mb ansible'
#

# Install base packages and pip dependencies
RUN apk update && apk upgrade --no-cache && \
    apk add --no-cache git make bash openssh-client \
    diffutils python3 py3-pip gcc python3-dev linux-headers \
    musl-dev py3-cffi openssl-dev && \
    pip3 install --no-cache-dir certifi && \
    pip3 install --no-cache-dir ansible && \
    git clone https://github.com/ttssdev/appflow /opt/appflow && \
    pip3 install --no-cache-dir -r /opt/appflow/requirements.txt && \
    ln -s /opt/appflow/appflow.py /usr/local/bin/appflow && \
    apk del gcc python3-dev linux-headers musl-dev py3-cffi openssl-dev && \
    rm -rf /var/cache/apk/*

# RUN apk del git make bash openssh-client \
#     diffutils python3 py3-pip gcc python3-dev linux-headers \
#     musl-dev py3-cffi openssl-dev


COPY run.sh /usr/local/bin/run.sh
COPY assh /usr/local/bin/assh

ENTRYPOINT ["run.sh"]
