FROM ubuntu:18.04

RUN apt-get update && \
  apt-get install -y apt-transport-https curl

RUN curl -sL https://deb.nodesource.com/setup_12.x -o nodesource_setup.sh
RUN bash nodesource_setup.sh
RUN apt-get install -y nodejs

# Install latest NPM and Yarn
RUN npm install -g npm@latest
RUN npm install -g yarn@latest

# install additional native dependencies build tools
RUN apt install -y build-essential

# install Git client
RUN apt-get install -y git
# install unzip utility to speed up Cypress unzips
# https://github.com/cypress-io/cypress/releases/tag/v3.8.0
RUN apt-get install -y unzip

# install Cypress dependencies (separate commands to avoid time outs)
RUN apt-get install -y \
    libgtk2.0-0
RUN apt-get install -y \
    libnotify-dev
RUN apt-get install -y \
    libgconf-2-4 \
    libnss3 \
    libxss1
RUN apt-get install -y \
    libasound2 \
    xvfb\
    wget

#firefox dependencies
RUN apt-get update && \
  apt-get install -y \
  bzip2 \
  # add codecs needed for video playback in firefox
  # https://github.com/cypress-io/cypress-docker-images/issues/150
  mplayer

# install Firefox browser
RUN wget --no-verbose -O /tmp/firefox.tar.bz2 https://download-installer.cdn.mozilla.net/pub/firefox/releases/98.0.2/linux-x86_64/en-US/firefox-98.0.2.tar.bz2 && \
  tar -C /opt -xjf /tmp/firefox.tar.bz2 && \
  rm /tmp/firefox.tar.bz2 && \
  ln -fs /opt/firefox/firefox /usr/bin/firefox

# a few environment variables to make NPM installs easier
# good colors for most applications
ENV TERM xterm
# avoid million NPM install messages
ENV npm_config_loglevel warn
# allow installing when the main user is root
ENV npm_config_unsafe_perm true


#install kr-cli
USER root

RUN apt-get install -qqy x11-apps
RUN npm i -g katalon-recorder-cli

#install python3
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get -y install python3.8
RUN apt-get -y install python3-pip
RUN apt-get -y install xvfb
RUN pip3 install psutil

# versions of local tools
RUN echo "node version: $(node -v) \n" \
  "npm version:     $(npm -v) \n" \
  "yarn version:    $(yarn -v) \n" \
  "debian version:  $(cat /etc/debian_version) \n" \
  "user:            $(whoami) \n" \
  "git:             $(git --version) \n" \
  "Firefox version: $(firefox --version) \n" \
  "python:          $(python3 --version) \n" \
  "kr-cli:          $(kr-cli -v) \n"
  
RUN mkdir /home/e2e
RUN mkdir /home/scripts/
COPY scripts/commands.py /home/scripts/commands.py

#ENTRYPOINT ["python3", "/home/scripts/commands.py"]
