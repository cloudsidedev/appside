FROM frolvlad/alpine-glibc:alpine-3.6

LABEL Authors="Ivo Marino <ivo.marino@ttss.ch>, Luca Di Maio <luca.dimaio@ttss.ch>"
LABEL Description="AppFlow" Vendor="TTSS AG" Version="1.0"

# Install my Utils
RUN apk upgrade --no-cache && \
    apk add --no-cache git make bash openssh-client ansible
# 9mb bash
# 2mb openssh-client
# <1mb make
# 88mb ansible'
#

# Install Appflow
RUN git clone https://github.com/ttssdev/appflow /opt/appflow && \
    rm -rf /opt/appflow/docs && \
    rm -rf /opt/appflow/containers && \
    rm -rf /opt/appflow/.git && \
    ln -s /opt/appflow/appflow /usr/local/bin/appflow

RUN apk del --purge git

COPY run.sh /usr/local/bin/run.sh
COPY assh /usr/local/bin/assh

ENTRYPOINT ["run.sh"]
