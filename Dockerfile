FROM python:3.4
MAINTAINER William Silversmith
# This image contains private keys, make sure the image is not pushed to docker hub or any public repo.
## INSTALL gsutil
# Prepare the image.
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y -qq --no-install-recommends \
    apt-utils \
    curl \
    git \
    openssh-client \
    python-openssl \
    python \
    python-pip \
    python-dev \
    python-numpy \
    python-setuptools \
    libboost-all-dev \
    liblzma-dev \
    libgmp-dev \
    screen \
    software-properties-common \
    unzip \
    vim \
    wget \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install setuptools Cython wheel numpy 

RUN mkdir /.ssh
ADD ./ /ingest-client
RUN cd /ingest-client && pip install -e .
RUN pip install pyasn1 --upgrade

RUN mkdir $HOME/.intern

CMD boss-ingest --force --manual-complete --job-id $INGEST_JOB_ID /config/docker.json

