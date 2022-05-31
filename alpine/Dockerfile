
FROM alpine:3.16.0 
USER root

RUN apk add --update npm
RUN apk add --update firefox
RUN apk add --update xvfb-run
RUN npm i -g katalon-recorder-cli

ENV TERM xterm
ENV npm_config_loglevel warn
ENV npm_config_unsafe_perm true
RUN mkdir /home/e2e
RUN mkdir /home/scripts/

# RUN apt-get update && \
#   apt-get install -y apt-transport-https curl
# 
# RUN curl -sL https://deb.nodesource.com/setup_12.x -o nodesource_setup.sh
# RUN bash nodesource_setup.sh
# RUN apt-get install -y nodejs
# 
# # Install latest NPM and Yarn
# RUN npm install -g npm@latest
# RUN npm install -g yarn@latest
# 

# # install additional native dependencies build tools
# RUN apt install -y build-essential
# 
# # a few environment variables to make NPM installs easier
# # good colors for most applications
# ENV TERM xterm
# # avoid million NPM install messages
# ENV npm_config_loglevel warn
# # allow installing when the main user is root
# ENV npm_config_unsafe_perm true
# 
# 
# #install kr-cli
# USER root
# 
# RUN apt-get install -qqy x11-apps
# RUN npm i -g katalon-recorder-cli
# 
# #install python3
# RUN apt-get install -y software-properties-common
# RUN add-apt-repository -y ppa:deadsnakes/ppa
# RUN apt-get update
# RUN apt-get -y install python3.8
# RUN apt-get -y install python3-pip
# RUN apt-get -y install xvfb
# RUN pip3 install psutil
# 
# # versions of local tools
# RUN echo "node version: $(node -v) \n" \
#   "npm version:     $(npm -v) \n" \
#   "yarn version:    $(yarn -v) \n" \
#   "debian version:  $(cat /etc/debian_version) \n" \
#   "user:            $(whoami) \n" \
#   "git:             $(git --version) \n" \
#   "Firefox version: $(firefox --version) \n" \
#   "python:          $(python3 --version) \n" \
#   "kr-cli:          $(kr-cli -v) \n"
#   
# RUN mkdir /home/e2e
# RUN mkdir /home/scripts/
# COPY scripts/commands.py /home/scripts/commands.py

#ENTRYPOINT ["python3", "/home/scripts/commands.py"]
