FROM python:3.9.2-slim-buster
RUN apt-get update &&\
    apt-get upgrade --yes &&\
    apt-get install nginx gcc --yes
COPY src/requeriments.txt /tmp/requeriments.txt
RUN python3 -m pip install -r /tmp/requeriments.txt
RUN apt-get purge gcc --yes &&\
    apt-get autoremove --yes
RUN mkdir /opt/datachallenge
RUN mkdir /etc/datachallenge
WORKDIR /opt/datachallenge
COPY src/*.py /opt/datachallenge/
COPY src/aws.toml /etc/datachallenge/
COPY conf/nginx.conf /etc/nginx/sites-enabled/default
COPY  conf/timeout.conf /etc/nginx/conf.d/timeout.conf
RUN groupadd -g 1000 dcstone
RUN useradd -r -u 1000 -g dcstone dcstone
CMD nginx && \
    uwsgi --socket 127.0.0.1:3031 \
    --wsgi-file /opt/datachallenge/main.py \
    --callable app \
    --processes 4 --threads 2 \
    --stats 127.0.0.1:9191 --uid 1000 --gid 1000
