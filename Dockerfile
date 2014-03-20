FROM ubuntu:13.10

RUN apt-get update
RUN apt-get install -y python-pip

ADD . /home/docker/zombsole/
WORKDIR /home/docker/zombsole

RUN pip install -r requirements.txt
RUN pip install -r isolator_requirements.txt

EXPOSE 8000
CMD python docker_isolation.py serve_players
