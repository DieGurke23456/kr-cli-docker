# kr-cli/base:ubuntu18.04-12.0

Image with Ubuntu 18.04 and Node 12

```
node version:    v12.22.12
npm version:     8.10.0
yarn version:    1.22.18
debian version:  buster/sid
user:            root
git:             git version 2.17.1
firefox:         Mozilla Firefox 98.0.2
kr-cli:          1.1.0   
``` 



## How to use
### With gui
#### Allow local xhost connections 
```shell
[ -d ~/workspace ] || mkdir ~/workspace
xhost local:root
```
#### Run with gui
```shell
docker run -i --net host --rm -v $PWD:/home/e2e -w /home/e2e -e DISPLAY kr-cli/base:ubuntu18.04-12.0 "TEST.html" --report="REPORT_DIR"
```
### headless
#### create network for link
``` shell
docker network create NETWORK
```
#### start xvfb
``` shell
docker run -e DISPLAY=55 --name xvfb --net NETWORK metal3d/xvfb
```
#### run headless
```shell
docker run -i --net NETWORK --rm -v $PWD:/home/e2e -w /home/e2e -e DISPLAY=xvfb:55 --link xvfb kr-cli/base:ubuntu18.04-12.0 "TEST.html" --report="REPORT_PATH"

```


