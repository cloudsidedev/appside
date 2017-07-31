FROM frolvlad/alpine-glibc:alpine-3.6

LABEL Authors="Ivo Marino <ivo.marino@ttss.ch>, Luca Di Maio <luca.dimaio@ttss.ch>"
LABEL Description="AppFlow" Vendor="TTSS AG" Version="1.0"

# Install my Utils
RUN apk upgrade --no-cache && \
    apk add --no-cache git && \
    apk add --no-cache make && \
    apk add --no-cache curl && \
    apk add --no-cache bash && \
    apk add --no-cache openssh && \
    apk add --no-cache diffutils && \
    apk add --no-cache ansible
# Install Appflow
RUN git clone https://github.com/ttssdev/appflow /opt/appflow && \
    ln -s /opt/appflow/appflow /usr/local/bin/appflow

COPY run.sh /usr/local/bin/run.sh
COPY assh /usr/local/bin/assh

ENTRYPOINT ["run.sh"]
