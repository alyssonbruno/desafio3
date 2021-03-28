FROM python:3.7
RUN apt-get update &&\
    apt-get upgrade --yes &&\
    apt-get autoremove --yes
COPY src/requeriments.txt /tmp/requeriments.txt
RUN python -m pip install -r /tmp/requeriments.txt
RUN mkdir /opt/datachallenge
WORKDIR /opt/datachallenge
COPY src/*.py /opt/datachallenge/
CMD python /opt/datachallenge/main.py