# Use a minimal Python image
FROM python:3.12-slim

ARG artifact_dir

WORKDIR /workspace
COPY ./${artifact_dir} /workspace/
RUN rm -rf /workspace/prov
RUN mkdir /workspace/prov

RUN apt update
RUN apt install -y git

# Find and install all requirements.txt files recursively
RUN find . -name "requirements.txt" -exec pip install -r {} \;

# RUN apt-get install -y graphviz graphviz-dev
# RUN pip install --upgrade pip
# RUN pip install pygraphviz

RUN git clone https://github.com/HPCI-Lab/yProvML.git
RUN cd yProvML; git switch development; pip install .; cd ..
