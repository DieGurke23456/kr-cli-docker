FROM alpine:3.16.0 
#USER root

#install npm
RUN apk add --update npm
ENV TERM xterm
ENV npm_config_loglevel warn
ENV npm_config_unsafe_perm true

#install firefox
RUN apk add --update firefox

#install xvfb
RUN apk add --update xvfb-run

#install katalon-recorder-cli
RUN npm i -g katalon-recorder-cli

#install python
RUN apk add --update python3 py3-pip
RUN apk add --update py-psutil
#RUN apk add --update py3-junit-xml
RUN pip3 install junit-xml
RUN mkdir /home/e2e
RUN mkdir /home/scripts/

RUN echo "node version: $(node -v) \n"\
   "npm version:     $(npm -v) \n"\
   "user:            $(whoami) \n"\
   "Firefox version: $(firefox --version) \n"\
   "python:          $(python3 --version) \n"\
   "kr-cli:          $(kr-cli -v) \n"

COPY scripts/commands.py /home/scripts/commands.py
ENTRYPOINT ["python3", "/home/scripts/commands.py"]
