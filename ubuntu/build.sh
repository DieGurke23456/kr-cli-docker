set e+x

# build image with kr-cli dependencies
LOCAL_NAME=kr-cli/base:ubuntu18.04-12.0

echo "Building $LOCAL_NAME"
docker build -t $LOCAL_NAME . 
