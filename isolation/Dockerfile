FROM ubuntu:13.10

RUN apt-get update
RUN apt-get install -y python-pip

# added before the full folder, so caching of pip installation
# isn't broke when cached of the full zombsole folder breaks
ADD requirements.txt /home/docker/requirements.txt
ADD isolator_requirements.txt /home/docker/isolator_requirements.txt

WORKDIR /home/docker
RUN pip install -r requirements.txt
RUN pip install -r isolator_requirements.txt

# now add the rest of the folder
ADD . /home/docker/zombsole/
WORKDIR /home/docker/zombsole

EXPOSE 8000
CMD python docker_isolation.py serve_players
