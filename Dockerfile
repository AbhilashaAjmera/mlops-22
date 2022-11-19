FROM ubuntu:latest
COPY ./*.py/exp/
COPY ./requirements.txt/exp/requirements.txt
RUN pip3 install --no-cache-dir -r/exp/requirements.txt
WORKDIR /exp

