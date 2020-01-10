FROM python:3.7

ENV APP_PATH=/player

RUN mkdir $APP_PATH
WORKDIR $APP_PATH

RUN apt-get update && apt-get install -y alsa-utils
RUN pip3 install pygame

# TODO: create app user so it doesn't run as root
COPY . $APP_PATH
COPY conf /etc

CMD ["/usr/bin/env", "python", "src/player.py"]
