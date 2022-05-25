FROM python:3.7

ENV PYTHONPATH /usr/src/runtime

WORKDIR /usr/src

RUN apt-get update -y && \
        apt-get install -y \
            gcc \
            make \
            musl-dev \
            python-dev \
            g++

COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python setup.py sdist
RUN pip install dist/containerly-runtime-0.1.0.tar.gz

#
# Begin custom build
#

RUN python train.py
ENV MODEL_LOCATION /usr/src/model.joblib

#
# End custom build
#

ENTRYPOINT [ "containerly-runtime" ]
