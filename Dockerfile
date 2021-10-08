FROM python:3.7.10-slim-buster
ARG DEBIAN_FRONTEND=noninteractive
# Install build dependencies
RUN apt-get update -y \
  && apt-get install --no-install-recommends -y build-essential \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
COPY . /bip85
WORKDIR /bip85
RUN pip install --no-cache-dir .
# Create an unprivileged user
RUN useradd --create-home --user-group user
USER user
ENTRYPOINT ["bip85-cli"]
