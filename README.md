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

## Before using 
```shell
[ -d ~/workspace ] || mkdir ~/workspace
xhost local:root
```

## How to use
```shell
docker run -i --net=host --rm -v $PWD:/home/e2e -w /home/e2e -e DISPLAY kr-cli/base:ubuntu18.04-12.0 "TEST.html" --report="REPORT_DIR"
```

