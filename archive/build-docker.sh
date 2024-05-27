ARCH=""
MCL_URl=""
uname -a | grep -q "aarch64"
if [ $? -eq 0 ]; then
    ARCH="arm64v8/"
    MCL_URl="https://github.com/iTXTech/mcl-installer/releases/download/ae9f946/mcl-installer-ae9f946-linux-arm-musl"
fi
sudo docker build --build-arg ARCH=$ARCH -t qqrobot .
