FROM python:3.11-slim

RUN apt-get update

WORKDIR /workspace

ENV XDG_RUNTIME_DIR=/tmp/runtime-root
RUN mkdir -p $XDG_RUNTIME_DIR

COPY requirements.txt /workspace/requirements.txt
RUN pip install -r requirements.txt

COPY . /workspace

CMD ["bash"]
