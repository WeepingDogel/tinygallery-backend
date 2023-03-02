# syntax=docker/dockerfile:1

FROM ubuntu:23.04

WORKDIR /opt/tinyGalleryBackend
COPY . .

# Change this mirror you needed.
RUN sed -i 's@//.*archive.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list
RUN apt update && apt install -y nginx python3-pip
# Change this mirror you neeeded.
RUN pip install -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN cp -fv ./configForDocker/nginx.conf /etc/nginx/nginx.conf
RUN chmod +x ./configForDocker/start.sh

CMD [ "./configForDocker/start.sh" ]

EXPOSE 18880 8755
