FROM php:7-alpine

LABEL Authors="Ivo Marino <ivo.marino@ttss.ch>, Luca Di Maio <luca.dimaio@ttss.ch>"
LABEL Description="AppFlow" Vendor="TTSS AG" Version="1.0"

RUN echo "===> Adding appflow user..."  && \
    adduser -D -u 1000 appflow && \
    \
    \
    echo "===> Installing sudo to emulate normal OS behavior..."  && \
    apk --update add sudo                                         && \
    \
    \
    echo "===> Adding Python runtime..."  && \
    apk --update add python py-pip openssl ca-certificates    && \
    apk --update add --virtual build-dependencies \
                python-dev libffi-dev openssl-dev build-base  && \
    pip install --upgrade pip cffi                            && \
    \
    \
    echo "===> Installing Ansible..."  && \
    pip install ansible                && \
    \
    \
    echo "===> Installing packages)..."  && \
    apk --update add openssh-client rsync git make bash && \
    \
    \
    echo "===> Removing package list..."  && \
    apk del build-dependencies            && \
    rm -rf /var/cache/apk/*               && \
    \
    \
    echo "===> Adding hosts for convenience..."  && \
    mkdir -p /etc/ansible                        && \
    echo 'localhost' > /etc/ansible/hosts        && \
    \
    \
    echo "===> Cloning AppFlow..."  && \
    git clone https://github.com/ttssdev/appflow /opt/appflow  && \
    ln -s /opt/appflow/appflow /usr/local/bin/appflow          && \
    chown -R appflow:appflow /opt/appflow

WORKDIR /home/appflow
ENV HOME=/home/appflow
USER appflow

# ENTRYPOINT ["run.sh"]
ENTRYPOINT ["appflow"]

# CMD ["appflow"]
# CMD [ "php", "./your-script.php" ]
# CMD [ "ansible-playbook", "--version" ]
