FROM ubuntu:13.10

RUN apt-get update
RUN apt-get install -y python-pip

# added before the full folder, so caching of pip installation
# isn't broke when cached of the full zombsole folder breaks
ADD requirements.txt /home/docker/requirements.txt
ADD isolation/requirements.txt /home/docker/isolation_requirements.txt

WORKDIR /home/docker
RUN pip install -r requirements.txt
RUN pip install -r isolation_requirements.txt

# now add the rest of the folder
ADD . /home/docker/zombsole/
WORKDIR /home/docker/zombsole

EXPOSE 8000
CMD PYTHONPATH=. isolation/players_server.py
