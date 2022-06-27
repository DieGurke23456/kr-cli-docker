set e+x

# build image with kr-cli dependencies
LOCAL_NAME=kr-cli/base:alpine3.16

echo "Building $LOCAL_NAME"
docker build -t $LOCAL_NAME . 
