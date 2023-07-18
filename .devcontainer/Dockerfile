FROM ubuntu:latest

ENV DEV_PATH=/code/dev

RUN apt-get update
RUN apt-get install -y python3 && \
    apt-get install -y git && \
    apt-get install -y python3-pip && \
    apt-get install -y vim && \
    apt-get install -y libpq-dev

WORKDIR $DEV_PATH

RUN useradd -ms /bin/bash dev
RUN chown -R dev:dev $DEV_PATH
USER dev

# Install all the requirements
ADD requirements.txt ./../
RUN pip3 install -r ./../requirements.txt

CMD ["/bin/bash"]
