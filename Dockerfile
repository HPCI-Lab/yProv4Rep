FROM python:3.12-slim

ARG artifact_dir

WORKDIR /workspace
COPY ./${artifact_dir} /workspace/
RUN rm -rf /workspace/prov
RUN mkdir /workspace/prov

RUN apt update
RUN apt install -y git

RUN find . -name "requirements.txt" -exec pip install -r {} \;

RUN pip install yprov4ml

