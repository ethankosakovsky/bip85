FROM python:3.7.10-slim-buster
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y
# Install build dependencies
RUN apt-get install -y build-essential
COPY . /bip85
WORKDIR /bip85
RUN pip install .
# Create an unprivileged user
RUN useradd --create-home --user-group user
USER user
ENTRYPOINT ["bip85-cli"]
