FROM python:3.8-alpine

ARG hash_value=45e3efcd090f93e416504403fbf1474a753873db
WORKDIR /
RUN apk update
RUN apk add git gcc musl-dev linux-headers
RUN echo "hello" 
RUN git clone https://github.com/gr0vity-dev/bnano-prom-exporter.git app

WORKDIR /app

# Automatically invalidate the cache by adding a date command
RUN git fetch --all
# 45e3efcd090f93e416504403fbf1474a753873db # total duration
RUN git checkout $hash_value 
# RUN git checkout 4c5c99e7ecadc04f00f3b851b81076399f2b9592 # duration
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "-m", "nano_prom_exporter" ]