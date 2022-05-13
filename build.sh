set e+x

# build image with kr-cli dependencies
LOCAL_NAME=kr-cli/base:ubuntu16-8

echo "Building $LOCAL_NAME"
docker build -t $LOCAL_NAME . 
